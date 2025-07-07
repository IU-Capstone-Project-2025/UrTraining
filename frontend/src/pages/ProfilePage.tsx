import React from 'react'
import Profile from '../components/Profile'

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
      text_top: "",
      text_button: "View my trainings"
    }
  }

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