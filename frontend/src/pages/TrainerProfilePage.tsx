import React, { useContext } from 'react'
import Profile from '../components/Profile'
import { userInfoRequest } from '../api/apiRequests';
import TrainerProfile from '../components/TrainerProfile';
import AuthContext from '../components/context/AuthContext';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';

const TrainerProfilePage = (data: any) => {

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



  if (userDataStatus == "success") {
    console.log(userData)
  }

  console.log(data.data)

  const data_trainer = {
    username: userData?.username,
    user_type: t("trainer_profile.type"),
    email: userData?.email,
    gender: t("trainer_profile.gender_unspecified"),
    age: t("trainer_profile.age_unspecified"),
    profile: data.data?.experience.Specialization,
    date: formattedDate,
    grid_template: [
      "info info",
      "info info",
      "personal calendar",
      "personal calendar",
      "trainings calendar",
      "trainings upload",
    ],
    calendar_text: {
      text_top: t("trainer_profile.calendar.text_top"),
      text_button_top: t("trainer_profile.calendar.text_button_top"),
      text_bottom: t("trainer_profile.calendar.text_bottom"),
      text_button_bottom: t("trainer_profile.calendar.text_button_bottom"),
    },
    trainings_text: {
      text_top: t("trainer_profile.trainings.text_top"),
      text_bottom: t("trainer_profile.trainings.text_bottom"),
    },
    upload_text: {
      text_top: t("trainer_profile.upload.text_top"),
      text_button: t("trainer_profile.upload.text_button"),
    },
  };

  return (
    <TrainerProfile {...data_trainer} />
  )
}

export default TrainerProfilePage