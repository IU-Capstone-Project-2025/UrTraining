import React, { useContext } from 'react'
import Profile from '../components/Profile'
import { userInfoRequest } from '../api/apiRequests';
import TraineeProfile from '../components/TraineeProfile';
import { useQuery } from '@tanstack/react-query';
import AuthContext from '../components/context/AuthContext';

const TraineeProfilePage = () => {

  const authData = useContext(AuthContext);
  const today = new Date();

  const options: Intl.DateTimeFormatOptions = { day: 'numeric', month: 'long'};
  const formattedDate = today.toLocaleDateString('en-GB', options);

  const { data: userData, isLoading: userDataIsLoading, status: userDataStatus } = useQuery({
    queryKey: ['me'],
    queryFn: () => userInfoRequest(authData.access_token),
    enabled: authData.access_token !== ""
  })

  if (userDataStatus == "success") {
    console.log(userData)
  }

  const data_trainee = {
    picture: "/images/kanyeeast.jpg",
    username: userData!.username,
    user_type: "trainee",
    full_name: userData!.full_name,
    email: userData!.email || "example@example.example",
    gender: userData!.training_profile.basic_information.gender || "prefer not to specify",
    age: userData!.training_profile.basic_information.age || "prefer not to specify",
    tags: [
      "Yoga",
      "HIIT",
      "Boxing",
      "Cardio",
      "Stretching"
    ],
    date: formattedDate,
    grid_template: [
      "info info",
      "info info",
      "calendar personal",
      "calendar personal",
      "calendar trainings",
      "upload trainings"
    ],
    calendar_text: {
      text_top: " Welcome to a new day - let’s take one step closer to your goals today!",
      text_button_top: "View all training plans",
      text_bottom: "",
      text_button_bottom: "View recommendations"
    },
    trainings_text: {
      text_top: "Do you have uncompleted trainings?",
      text_bottom: "Try all saved trainings now"
    },
    upload_text: {
      text_top: "Add new preferences and goals to get better training experience",
      text_button: "Get new personalized recommendation"
    }
  }

  if (userDataIsLoading) {
    return <div className="centered-content">
            <div className="step-title-main">Loading...</div>
           </div>
  }

  return (
    <TraineeProfile {...data_trainee} />
  )
}

export default TraineeProfilePage