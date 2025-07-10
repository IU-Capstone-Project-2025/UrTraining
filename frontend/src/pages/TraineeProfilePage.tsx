import React from 'react'
import Profile from '../components/Profile'
import {  } from '../api/apiRequests';

const ProfilePage = () => {



  const data_trainee = {
    picture: "/images/kanyeeast.jpg",
    username: "traineeTwo",
    user_type: "trainee",
    email: "k.east@mail.ru",
    gender: "male",
    age: 35,
    tags: [
      "Yoga",
      "HIIT",
      "Fortnite",
      "Balls",
      "Stretching"
    ],
    date: "30 April 1997",
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
      text_top: "You have uncompleted trainings",
      text_bottom: "Try all saved trainings now"
    },
    upload_text: {
      text_top: "Add new preferences and goals to get better training experience",
      text_button: "Get new personalized recommendation"
    }
  }



  return (
    <Profile {...data_trainee} />
  )
}

export default ProfilePage