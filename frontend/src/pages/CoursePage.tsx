// import React from 'react'
import { useParams } from 'react-router-dom';
import Course from "../components/Course"
import kanye from '../assets/kanye.jpg'
import { transformRawCourseData } from "../utils/transformRawCouseData"
import { useSaveProgram, useDeleteFromSavedPrograms, useDeleteTrainingData } from "../api/mutations";
import { currentTrainingDataRequest, isTrainingSaved } from "../api/apiRequests";
import AuthContext from "../components/context/AuthContext";
import { useQuery } from "@tanstack/react-query";
import { useContext, useEffect, useState } from "react";

const CoursePage = () => {

    const { courseId } = useParams();
    const authData = useContext(AuthContext);

    const saveProgram = useSaveProgram(authData.access_token);
    const deleteFromSavedPrograms = useDeleteFromSavedPrograms(authData.access_token);
    const deleteTraining = useDeleteTrainingData(authData.access_token);

    const { data: courseData = [], isLoading: isLoadingTraining, status } = useQuery<any, Error>({
        queryKey: ['formTraining'],
        queryFn: () => currentTrainingDataRequest(courseId as String, authData.access_token),
        enabled: !!authData?.access_token && !!courseId
    })

    const { data: isSaved, isLoading: isLoadingStatus, status: statusSaved } = useQuery({
        queryKey: ['is-saved'],
        queryFn: () => isTrainingSaved(courseId as String, authData.access_token),
        enabled: !!authData?.access_token && !!courseId,
    });

    const { data: isCreated, isLoading: isLoading, status: isCreatedStatus } = useQuery({
        queryKey: ['is-created'],
        queryFn: () => isTrainingSaved(courseId as String, authData.access_token),
        enabled: !!authData?.access_token && !!courseId,
    });

    const [savedStatus, setSavedStatus] = useState<boolean | undefined>(undefined)
    const [createdStatus, setCreatedStatus] = useState<boolean | undefined>(undefined)

    useEffect(() => {
        if (statusSaved === 'success') {
            setSavedStatus(isSaved);
        }
    }, [isSaved, statusSaved]);

    useEffect(() => {
        if (isCreatedStatus === 'success') {
            setCreatedStatus(isCreated);
        }
    }, [isCreated, isCreatedStatus]);

    const handleAddToSaved = () => {
        
        saveProgram.mutate(courseId, {
            onSuccess: (data) => {
                setSavedStatus(true);
                console.log(data.message);
            },
            onError: (error) => {
                console.error("Error when saving:", error);
            }
        });
    };

    const handleDeleteFromSaved = () => {

        deleteFromSavedPrograms.mutate(courseId, {
            onSuccess: (data) => {
                setSavedStatus(false)
                console.log(data.message);
            },
            onError: (error) => {
                console.error("Error when deleting from saved:", error);
            }
        });
    };

    const handleDeleteTraining = () => {

        deleteTraining.mutate(courseId, {
            onSuccess: (data) => {
                console.log(data.message);
            },
            onError: (error) => {
                console.error("Error when deleting the training:", error);
            }
        });
    };

    const training_data = transformRawCourseData(courseData);

    return (
        <Course 
            {...training_data} 
            savedStatus={savedStatus}
            isCreated={createdStatus} 
            handleAddToSaved={handleAddToSaved} 
            handleDeleteFromSaved={handleDeleteFromSaved}
            handleDeleteTraining={handleDeleteTraining} 
        />
    )
}

export default CoursePage