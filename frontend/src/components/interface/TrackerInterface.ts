export interface TrainingExercise {
    exercise: string
    repeats: string
    sets: string
    duration: string
    rest: string
    description: string
}

export interface TrainingDay {
    title: string
    exercises: TrainingExercise[]
}

export interface TrackerProp {
    date: string
    index: number
    course_id: string
}

export interface GeneratedTrackerProp {
    date: string
    index: number
}

export interface TrackerWithDataProp {
    course_id: string
    course_title: string
    training_index: number
    training_day: TrainingDay
}