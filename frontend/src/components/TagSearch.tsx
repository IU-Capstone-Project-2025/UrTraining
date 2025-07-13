import React, { useState, useEffect } from 'react';
import '../css/TagSearch.css';

interface TagSearchProps {
  courses: any[];
  onFilterChange: (filteredCourses: any[]) => void;
}

interface TagGroups {
  activityType: string[];
  difficultyLevel: string[];
  requiredEquipment: string[];
}

const TagSearch: React.FC<TagSearchProps> = ({ courses, onFilterChange }) => {
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [searchText, setSearchText] = useState<string>('');
  const [tagGroups, setTagGroups] = useState<TagGroups>({
    activityType: [],
    difficultyLevel: [],
    requiredEquipment: []
  });

  // Собираем теги по группам из Activity Type, Difficulty Level, Required Equipment
  useEffect(() => {
    const activityTypes = new Set<string>();
    const difficultyLevels = new Set<string>();
    const requiredEquipment = new Set<string>();
    
    courses.forEach(course => {
      // Activity Type
      if (course["Activity Type"]) {
        activityTypes.add(course["Activity Type"]);
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
      difficultyLevel: Array.from(difficultyLevels).sort(),
      requiredEquipment: Array.from(requiredEquipment).sort()
    });
  }, [courses]);

  // Фильтрация курсов по выбранным тегам и текстовому поиску
  useEffect(() => {
    let filteredCourses = courses;

    // Фильтрация по тексту (регистронезависимый поиск по названию курса)
    if (searchText.trim()) {
      filteredCourses = filteredCourses.filter(course => {
        const courseTitle = course["Course Title"] || '';
        return courseTitle.toLowerCase().includes(searchText.toLowerCase());
      });
    }

    // Фильтрация по тегам
    if (selectedTags.length > 0) {
      filteredCourses = filteredCourses.filter(course => {
        return selectedTags.every(tag => {
          // Проверяем Activity Type
          if (course["Activity Type"] === tag) return true;
          
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

    onFilterChange(filteredCourses);
  }, [selectedTags, searchText, courses, onFilterChange]);

  const handleTagClick = (tag: string) => {
    setSelectedTags(prev => 
      prev.includes(tag) 
        ? prev.filter(t => t !== tag)
        : [...prev, tag]
    );
  };

  const clearAllTags = () => {
    setSelectedTags([]);
    setSearchText('');
  };

  const clearSearchText = () => {
    setSearchText('');
  };

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
        {(selectedTags.length > 0 || searchText.trim()) && (
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
      
      <div className="tag-search__groups">
        {tagGroups.activityType.length > 0 && renderTagGroup("Activity Type", tagGroups.activityType)}
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
};

export default TagSearch; 