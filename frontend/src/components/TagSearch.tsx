import React, { useState, useEffect, useContext, useMemo, useCallback } from 'react';
import '../css/TagSearch.css';
import AuthContext from './context/AuthContext';
import { getSavedCoursesRequest } from '../api/apiRequests';
import { useQuery } from '@tanstack/react-query';

interface TagSearchProps {
  courses: any[];
  onFilterChange: (filteredCourses: any[]) => void;
}

interface TagGroups {
  activityType: string[];
  programGoal: string[];
  difficultyLevel: string[];
  requiredEquipment: string[];
}

const TagSearch: React.FC<TagSearchProps> = React.memo(({ courses, onFilterChange }) => {
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [searchText, setSearchText] = useState<string>('');
  const [showSavedOnly, setShowSavedOnly] = useState<boolean>(false);
  const [tagGroups, setTagGroups] = useState<TagGroups>({
    activityType: [],
    programGoal: [],
    difficultyLevel: [],
    requiredEquipment: []
  });

  const authData = useContext(AuthContext);

  // Получаем сохраненные тренировки
  const { data: savedCourses = [], isLoading: savedCoursesLoading, refetch: refetchSavedCourses } = useQuery({
    queryKey: ['savedCourses'],
    queryFn: () => getSavedCoursesRequest(authData.access_token),
    enabled: !!authData.access_token && showSavedOnly,
    refetchOnWindowFocus: true, // Обновляем при фокусе окна
    retry: 1,
    staleTime: 0, // Данные всегда считаются устаревшими
    gcTime: 1000 * 60 * 5, // Кеш на 5 минут
  });

  // Автоматически отключаем фильтр сохраненных, если нет токена
  React.useEffect(() => {
    if (!authData.access_token && showSavedOnly) {
      setShowSavedOnly(false);
    }
  }, [authData.access_token, showSavedOnly]);

  // Рефетчим данные при включении фильтра сохраненных
  React.useEffect(() => {
    if (showSavedOnly && authData.access_token) {
      refetchSavedCourses();
    }
  }, [showSavedOnly, authData.access_token, refetchSavedCourses]);

  // Добавляем слушатель фокуса для обновления данных при возврате на страницу
  React.useEffect(() => {
    const handleFocus = () => {
      if (showSavedOnly && authData.access_token) {
        refetchSavedCourses();
      }
    };

    window.addEventListener('focus', handleFocus);
    return () => window.removeEventListener('focus', handleFocus);
  }, [showSavedOnly, authData.access_token, refetchSavedCourses]);

  // Мемоизируем сохраненные ID курсов для оптимизации
  const savedCourseIds = useMemo(() => {
    return savedCourses.map((course: any) => course.id);
  }, [savedCourses]);

  // Мемоизируем функцию обработки клика по тегу
  const handleTagClick = useCallback((tag: string) => {
    setSelectedTags(prev => 
      prev.includes(tag) 
        ? prev.filter(t => t !== tag)
        : [...prev, tag]
    );
  }, []);

  // Мемоизируем функцию очистки всех фильтров
  const clearAllTags = useCallback(() => {
    setSelectedTags([]);
    setSearchText('');
    setShowSavedOnly(false);
  }, []);

  // Мемоизируем функцию очистки поиска
  const clearSearchText = useCallback(() => {
    setSearchText('');
  }, []);

  // Собираем теги по группам из Activity Type, Program Goal, Difficulty Level, Required Equipment
  useEffect(() => {
    const activityTypes = new Set<string>();
    const programGoals = new Set<string>();
    const difficultyLevels = new Set<string>();
    const requiredEquipment = new Set<string>();
    
    courses.forEach(course => {
      // Activity Type
      if (course["Activity Type"]) {
        activityTypes.add(course["Activity Type"]);
      }
      
      // Program Goal
      if (course["Program Goal"] && Array.isArray(course["Program Goal"])) {
        course["Program Goal"].forEach((goal: string) => {
          if (goal.trim()) {
            programGoals.add(goal.trim());
          }
        });
      }
      
      // Difficulty Level
      if (course["Difficulty Level"]) {
        const difficultyLevel = course["Difficulty Level"].toLowerCase().split(/[,(]/)[0].trim();
        difficultyLevels.add(difficultyLevel);
      }
      
      // Required Equipment
      if (course["Required Equipment"] && Array.isArray(course["Required Equipment"])) {
        course["Required Equipment"].forEach((equipment: string) => {
          const equipmentName = equipment.split(/[,(]/)[0].trim();
          if (equipmentName) {
            requiredEquipment.add(equipmentName);
          }
        });
      }
    });
    
    setTagGroups({
      activityType: Array.from(activityTypes).sort(),
      programGoal: Array.from(programGoals).sort(),
      difficultyLevel: Array.from(difficultyLevels).sort(),
      requiredEquipment: Array.from(requiredEquipment).sort()
    });
  }, [courses]);

  // Фильтрация курсов по выбранным тегам, текстовому поиску и фильтру сохраненных
  const filteredCourses = useMemo(() => {
    let filtered = courses;

    // Фильтрация по сохраненным тренировкам
    if (showSavedOnly && !savedCoursesLoading) {
      filtered = filtered.filter(course => savedCourseIds.includes(course.id));
    }

    // Фильтрация по тексту (регистронезависимый поиск по названию курса)
    if (searchText.trim()) {
      filtered = filtered.filter(course => {
        const courseTitle = course["Course Title"] || '';
        return courseTitle.toLowerCase().includes(searchText.toLowerCase());
      });
    }

    // Фильтрация по тегам
    if (selectedTags.length > 0) {
      filtered = filtered.filter(course => {
        return selectedTags.every(tag => {
          // Проверяем Activity Type
          if (course["Activity Type"] === tag) return true;
          
          // Проверяем Program Goal
          if (course["Program Goal"] && Array.isArray(course["Program Goal"])) {
            if (course["Program Goal"].includes(tag)) return true;
          }
          
          // Проверяем Difficulty Level
          if (course["Difficulty Level"]) {
            const difficultyLevel = course["Difficulty Level"].toLowerCase().split(/[,(]/)[0].trim();
            if (difficultyLevel === tag) return true;
          }
          
          // Проверяем Required Equipment
          if (course["Required Equipment"] && Array.isArray(course["Required Equipment"])) {
            return course["Required Equipment"].some((equipment: string) => {
              const equipmentName = equipment.split(/[,(]/)[0].trim();
              return equipmentName === tag;
            });
          }
          
          return false;
        });
      });
    }

    return filtered;
  }, [selectedTags, searchText, showSavedOnly, courses, savedCourseIds, savedCoursesLoading]);

  // Уведомляем родительский компонент об изменениях
  useEffect(() => {
    onFilterChange(filteredCourses);
  }, [filteredCourses, onFilterChange]);

  const renderTagGroup = (title: string, tags: string[]) => (
    <div className="tag-search__group">
      <h4 className="tag-search__group-title">{title}</h4>
      <div className="tag-search__group-tags">
        {tags.map((tag: string) => (
          <button
            key={tag}
            onClick={() => handleTagClick(tag)}
            className={`tag-search__tag ${selectedTags.includes(tag) ? 'tag-search__tag--selected' : ''}`}
          >
            {tag}
          </button>
        ))}
      </div>
    </div>
  );

  return (
    <div className="tag-search">
      <div className="tag-search__header">
        <h3>Filter trainings</h3>
        {(selectedTags.length > 0 || searchText.trim() || showSavedOnly) && (
          <button onClick={clearAllTags} className="tag-search__clear">
            Clear all
          </button>
        )}
      </div>
      
      <div className="tag-search__text-search">
        <input
          type="text"
          placeholder="Search by training name..."
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
          className="tag-search__input"
        />
        {searchText && (
          <button onClick={clearSearchText} className="tag-search__clear-text">
            ×
          </button>
        )}
      </div>

      {/* Checkbox для фильтрации сохраненных тренировок */}
      <div className="tag-search__saved-filter">
        <label className="tag-search__checkbox-label">
          <input
            type="checkbox"
            checked={showSavedOnly}
            onChange={(e) => setShowSavedOnly(e.target.checked)}
            className="tag-search__checkbox"
          />
          <span className="tag-search__checkbox-text">Show saved trainings only</span>
        </label>
      </div>
      
      <div className="tag-search__groups">
        {tagGroups.activityType.length > 0 && renderTagGroup("Activity Type", tagGroups.activityType)}
        {tagGroups.programGoal.length > 0 && renderTagGroup("Program Goal", tagGroups.programGoal)}
        {tagGroups.difficultyLevel.length > 0 && renderTagGroup("Difficulty Level", tagGroups.difficultyLevel)}
        {tagGroups.requiredEquipment.length > 0 && renderTagGroup("Required Equipment", tagGroups.requiredEquipment)}
      </div>
      
      {selectedTags.length > 0 && (
        <div className="tag-search__selected">
          <span>Selected tags: </span>
          {selectedTags.map((tag: string) => (
            <span key={tag} className="tag-search__selected-tag">
              {tag}
              <button 
                onClick={() => handleTagClick(tag)}
                className="tag-search__remove"
              >
                ×
              </button>
            </span>
          ))}
        </div>
      )}
    </div>
  );
});

export default TagSearch; 