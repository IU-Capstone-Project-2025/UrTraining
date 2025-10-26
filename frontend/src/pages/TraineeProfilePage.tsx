import React, { useContext } from 'react'
import Profile from '../components/Profile'
import { getAllScheduleRequest, userInfoRequest } from '../api/apiRequests';
import TraineeProfile from '../components/TraineeProfile';
import { useQuery } from '@tanstack/react-query';
import AuthContext from '../components/context/AuthContext';
import { useTranslation } from 'react-i18next';

const TraineeProfilePage = () => {

  const authData = useContext(AuthContext);
  const { t, i18n } = useTranslation();
  const today = new Date();

  const options: Intl.DateTimeFormatOptions = { day: 'numeric', month: 'long'};
  const formattedDate = today.toLocaleDateString(
    i18n.language === "ru" ? "ru-RU" : "en-GB",
    options
  );

  const { data: userData, isLoading: userDataIsLoading, status: userDataStatus } = useQuery({
    queryKey: ['me'],
    queryFn: () => userInfoRequest(authData.access_token),
    enabled: authData.access_token !== ""
  })

  const { data: userSchedule, isLoading: userScheduleIsLoading, status: userScheduleStatus } = useQuery({
    queryKey: ['mySchedule'],
    queryFn: () => getAllScheduleRequest(authData.access_token),
    enabled: authData.access_token !== ""
  })

  const data_trainee = {
    schedule: userSchedule,
    picture: "/images/kanyeeast.jpg",
    username: userData?.username,
    user_type: t("trainee_profile.type"),
    full_name: userData?.full_name,
    email: userData?.email || "example@example.example",
    gender:
      userData?.training_profile?.basic_information?.gender ||
      t("trainee_profile.gender_unspecified"),
    age:
      userData?.training_profile?.basic_information?.age ||
      t("trainee_profile.age_unspecified"),
    tags: ["Yoga", "HIIT", "Boxing", "Cardio", "Stretching"],
    date: formattedDate,
    grid_template: [
      "info info",
      "info info",
      "calendar personal",
      "calendar personal",
      "calendar trainings",
      "upload trainings",
    ],
    calendar_text: {
      text_top: t("trainee_profile.calendar.text_top"),
      text_button_top: t("trainee_profile.calendar.text_button_top"),
      text_bottom: t("trainee_profile.calendar.text_bottom"),
      text_button_bottom: t("trainee_profile.calendar.text_button_bottom"),
    },
    trainings_text: {
      text_top: t("trainee_profile.trainings.text_top"),
      text_bottom: t("trainee_profile.trainings.text_bottom"),
    },
    today_text: {
      text_top: t("trainee_profile.today.text_top"),
      text_button: t("trainee_profile.today.text_button"),
    },
    upload_text: {
      text_top: t("trainee_profile.upload.text_top"),
      text_button: t("trainee_profile.upload.text_button"),
    },
  };

  if (userDataIsLoading || userScheduleIsLoading) {
    return <div className="centered-content">
            <div className="step-title-main">{t("catalogue.loading")}</div>
           </div>
  }

  return (
    <TraineeProfile {...data_trainee} />
  )
}

export default TraineeProfilePage