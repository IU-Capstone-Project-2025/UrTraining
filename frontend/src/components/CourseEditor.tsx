import { useState, useRef, useEffect } from 'react';
import '../css/Course.css';
import Metadata from './Metadata';
import star from '../assets/star.svg';

interface Exercise {
  exercise: string;
  repeats: string;
  sets: string;
  duration: string;
  rest: string;
  description: string;
}

interface StepData {
    [key: string]: any;
}

interface DataProps {
  savedData: StepData;
  setSavedData: React.Dispatch<React.SetStateAction<StepData>>;
  onBack: () => void;
  onSubmit: () => void;
}

type ExerciseField = keyof Exercise;
type EditableField = ExerciseField | 'title';

const TrainingEditor: React.FC<DataProps> = ({ savedData, setSavedData, onBack, onSubmit }) => {

  const [editing, setEditing] = useState<{
    dayIndex: number | null;
    exerciseIndex: number | null;
    field: EditableField | null;
  }>({
    dayIndex: null,
    exerciseIndex: null,
    field: null
  });

  const scrollRef = useRef<HTMLDivElement>(null);

  // Horizontal scroll
  useEffect(() => {
    const scrollElement = scrollRef.current;
    if (!scrollElement) return;

    const onWheel = (e: WheelEvent) => {
      e.preventDefault();
      scrollElement.scrollLeft += e.deltaY * 4;
    };

    scrollElement.addEventListener('wheel', onWheel, { passive: false });
    return () => scrollElement.removeEventListener('wheel', onWheel);
  }, []);

  const startEditing = (
    dayIndex: number,
    exerciseIndex: number | null,
    field: EditableField
  ) => {
    setEditing({ dayIndex, exerciseIndex, field });
  };

  const stopEditing = () => {
    setEditing({ dayIndex: null, exerciseIndex: null, field: null });
  };

  // Функции для управления структурой
  const addTrainingDay = () => {
    setSavedData((prev: any) => ({
      ...prev,
      training_plan: [
        ...prev.training_plan,
        {
          title: `Day ${prev.training_plan.length + 1}`,
          exercises: [{
            Exercise: "Exercise",
            Reps: "-",
            Sets: "-",
            Duration: "-",
            Rest: "-",
            Description: "-"
          }]
        }
      ]
    }));
  };

  const addExercise = (dayIndex: number) => {
    setSavedData((prev: any) => {
      const updatedPlan = [...prev.training_plan];
      updatedPlan[dayIndex].exercises.push({
        exercise: "Exercise",
        repeats: "-",
        sets: "-",
        duration: "-",
        rest: "-",
        description: "-"
      });
      return { ...prev, training_plan: updatedPlan };
    });
  };

  const handleChange = (value: string, dayIndex: number, exerciseIndex: number | null, field: EditableField) => {
    const updatedPlan = [...savedData.training_plan];
    if (exerciseIndex !== null) {
      updatedPlan[dayIndex].exercises[exerciseIndex][field] = value;
    } else {
      updatedPlan[dayIndex].title = value;
    }
    setSavedData({ ...savedData, training_plan: updatedPlan });
  };

  const handleDayTitleChange = (dayIndex: number, title: string) => {
    setSavedData((prev: any) => {
      const updatedPlan = [...prev.training_plan];
      updatedPlan[dayIndex].title = title;
      return { ...prev, training_plan: updatedPlan };
    });
  };

  return (
    <div className="course basic-page" onDoubleClick={stopEditing}>
      <div className="course__container">
        <h2 className="step-title">Step 2: Course Plan</h2>
        <div className='course__info'>
          <div className='course__info__title'>
            <div className='course__info__text'>
              <input
                type="text"
                value={savedData.course_title}
                placeholder='Title...'
                onChange={(e) => setSavedData((prev: any) => ({
                  ...prev,
                  course_title: e.target.value
                }))}
                className="course-title-input"
              />
            </div>
          </div>
        </div>

        {/* Редактор структуры тренировки */}
        <div className='course__structure'>
          <div className='course__structure__header'>
            <h3>Course Structure</h3>
            <button onClick={addTrainingDay} className="btn-basic-white">
              Add new day
            </button>
          </div>

          <div className='course__structure__container' ref={scrollRef}>
            {savedData.training_plan.map((day: any, dayIndex: number) => (
              <div key={dayIndex} className="course__structure__session">
                <div className="course__session__table">
                  {editing.dayIndex === dayIndex && editing.exerciseIndex === null ? (
                    <input
                      type="text"
                      value={day.title}
                      onChange={(e) => handleChange(e.target.value, dayIndex, null, 'title')}
                      className="edit-input"
                      autoFocus
                      onBlur={stopEditing}
                    />
                  ) : (
                    <h2
                      onClick={() => startEditing(dayIndex, null, 'title')}
                      className="editable-title"
                    >
                      {day.title}
                    </h2>
                  )}

                  <div className="course__table__header">
                    {["Exercise", "Reps", "Sets", "Duration", "Rest", "Description"].map((h) => (
                      <div key={h} className="course__table__cell">{h}</div>
                    ))}
                  </div>

                  <div className="course__table__body">
                    {day.exercises.map((exercise: any, exIndex: number) => (
                      <div key={exIndex} className="course__table__row">
                        {(Object.keys(exercise) as ExerciseField[]).map((field) => (
                          <div key={field} className="course__table__cell">
                            {editing.dayIndex === dayIndex &&
                              editing.exerciseIndex === exIndex &&
                              editing.field === field ? (
                              <input
                                type="text"
                                value={String(exercise[field])}
                                onChange={(e) => handleChange(e.target.value, dayIndex, exIndex, field)}
                                className="edit-input"
                                autoFocus
                                onBlur={stopEditing}
                              />
                            ) : (
                              <span
                                onClick={() => startEditing(dayIndex, exIndex, field)}
                                className="editable-field"
                              >
                                {String(exercise[field])}
                              </span>
                            )}
                          </div>
                        ))}
                      </div>
                    ))}
                    <button
                      onClick={() => addExercise(dayIndex)}
                      className="btn-basic-white"
                    >
                      Add exercise
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>


        </div>

        {/* Кнопка сохранения */}
        <div className="editor-actions">
          <div className="button-row">
                <button className="btn-basic-black" onClick={onBack}>Back</button>
                <button className="btn-basic-black" onClick={onSubmit}>Save the course</button>
            </div>
        </div>
      </div>
    </div>
  );
};

export default TrainingEditor;