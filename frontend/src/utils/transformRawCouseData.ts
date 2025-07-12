import trainer from '../assets/kanye.jpg'

interface Badge {
  badge_text: string;
  badge_color: string;
}

interface Exercise {
  exercise: string;
  repeats: string;
  sets: string;
  duration: string;
  rest: string;
  description: string;
}

interface TrainingDay {
  title: string;
  exercises: Exercise[];
}

interface CoachData {
  username: string;
  id: number;
  profile_picture: string;
  rating: number;
  reviews: number;
}

interface TrainingData {
  header_badges: {
    training_type: Badge[];
    training_info: Badge[];
    training_equipment: Badge[];
  };
  course_info: {
    title: string;
    author: string;
    description: string;
    rating: number;
    reviews: number;
  };
  training_plan: TrainingDay[];
  coach_data: CoachData;
  id: any;
}

export function transformRawCourseData(serverData: any): TrainingData {
  const trainingTypeBadge: Badge = {
    badge_text: serverData["Activity Type"] || "Training",
    badge_color: "#9747FF"
  };

  const trainingInfoBadges: Badge[] = [
    {
      badge_text: serverData["Difficulty Level"]?.toLowerCase().split(/[,(]/)[0].trim() || "all levels",
      badge_color: "#696969"
    },
    {
      badge_text: serverData["Average Workout Duration"]?.toLowerCase() || "30 min/training",
      badge_color: "#696969"
    },
    {
      badge_text: serverData["Weekly Training Frequency"]?.toLowerCase() || "3-4 trainings/week",
      badge_color: "#696969"
    },
    {
      badge_text: `${serverData["Course Duration (weeks)"]} weeks` || "2 weeks",
      badge_color: "#696969"
    }
  ];

  const equipmentBadges: Badge[] = serverData["Required Equipment"]?.length 
    ? serverData["Required Equipment"].map((eq: string) => ({
        badge_text: eq.split(/[,(]/)[0].trim(),
        badge_color: "#888EE3"
      }))
    : [{
        badge_text: "No equipment",
        badge_color: "#888EE3"
      }];

  const courseInfo = {
    title: serverData["Course Title"] || "Unnamed Course",
    author: serverData["Trainer Name"] || "Unknown Trainer",
    description: "",
    rating: serverData["Average Course Rating"] || 0,
    reviews: serverData["Number of Reviews"] || 0
  };

  const trainingPlan: TrainingDay[] = serverData["training_plan"]?.map((day: any) => ({
    title: day.title || "Unnamed Routine",
    exercises: day.exercises?.map((ex: any) => ({
      exercise: ex.exercise || "Unknown Exercise",
      repeats: ex.repeats || "-",
      sets: ex.sets || "1",
      duration: ex.duration || "-",
      rest: ex.rest || "-",
      description: ex.description || "No description"
    })) || []
  })) || [];

  const coachData: CoachData = {
    username: serverData["Trainer Name"] || "Unknown Trainer",
    profile_picture: trainer,
    id: serverData["user_id"] || 0,
    rating: serverData["Experience"]?.Rating || 0,
    reviews: serverData["Active Participants"] || 0
  };

  return {
    header_badges: {
      training_type: [trainingTypeBadge],
      training_info: trainingInfoBadges,
      training_equipment: equipmentBadges
    },
    course_info: courseInfo,
    training_plan: trainingPlan,
    coach_data: coachData,
    id: serverData.id
  };
}