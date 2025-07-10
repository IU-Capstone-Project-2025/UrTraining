import React, { useContext } from 'react'
import Profile from '../components/Profile'
import { userInfoRequest } from '../api/apiRequests';
import TrainerProfile from '../components/TrainerProfile';
import AuthContext from '../components/context/AuthContext';
import { useQuery } from '@tanstack/react-query';

const TrainerProfilePage = (data: any) => {

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

  console.log(data.data)

  const data_trainer = {
    username: userData?.username,
    user_type: "trainer",
    email: userData?.email,
    gender: "prefer not to specify",
    age: "prefer not to specify",
    profile: data.data?.experience.Specialization,
    date: formattedDate,
    grid_template: [
      "info info",
      "info info",
      "personal calendar",
      "personal calendar",
      "trainings calendar",
      "trainings upload"
    ],
    calendar_text: {
      text_top: "Ready to lead the way today? Your athletes are waiting!",
      text_button_top: "See the statistics",
      text_bottom: "You can discover the programs of other trainers or create your own:",
      text_button_bottom: "View all plans"
    },
    trainings_text: {
      text_top: "Have some new ideas on paper?",
      text_bottom: "Upload new training plan now"
    },
    upload_text: {
      text_top: "See all the uploaded trainings and edit it, if needed:",
      text_button: "View my trainings"
    }
  }

  return (
    <TrainerProfile {...data_trainer} />
  )
}

export default TrainerProfilePage