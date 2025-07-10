import React from 'react'
import Profile from '../components/Profile'
import {  } from '../api/apiRequests';

const ProfilePage = () => {

  

  const data_trainer = {
    username: "trainerOne",
    user_type: "trainer",
    email: "y.ye@mail.ru",
    gender: "male",
    age: 40,
    tags: [
      "Cardio",
      "HIIT",
      "Yoga",
      "Functional trainings",
      "Stretching"
    ],
    date: "11 September 2001",
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
    <Profile {...data_trainer} />
  )
}

export default ProfilePage