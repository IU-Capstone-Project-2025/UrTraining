import React from 'react'
import Profile from '../components/Profile'
import { trainerDataRequest} from '../api/apiRequests';
import { useQuery } from "@tanstack/react-query";
import { useContext } from "react";
import AuthContext from '../components/context/AuthContext';
import TraineeProfilePage from '../pages/TraineeProfilePage';
import TrainerProfilePage from '../pages/TrainerProfilePage';

const ProfilePage = () => {

  const authData = useContext(AuthContext);

  const { data: trainerData = [], isLoading, status } = useQuery<any, Error>({
    queryKey: ['myTrainings'],
    queryFn: () => trainerDataRequest(authData.access_token),
  })

  if (isLoading) return <div className="centered-content">
                            <div className="step-title-main">Loading...</div>
                        </div>

  if (status=="success" && trainerData.trainer_profile !== null) { console.log(trainerData.trainer_profile) }                      

  return (
    <>
      {trainerData.trainer_profile !== null ? (
        <TrainerProfilePage data={trainerData.trainer_profile}/>
      ) : (
        <TraineeProfilePage />
      )}
    </>
  )
};

export default ProfilePage