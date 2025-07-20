// import React from 'react'
import { useParams } from 'react-router-dom';
import Course from "../components/Course"
import kanye from '../assets/kanye.jpg'
import { transformRawCourseData } from "../utils/transformRawCouseData"
import { useSaveProgram, useDeleteFromSavedPrograms, useDeleteTrainingData, useGetScheduleFromAI, useSendSchedule } from "../api/mutations";
import { currentTrainingDataRequest, isTrainingSaved, isTrainingCreatedByUser, userInfoRequest } from "../api/apiRequests";
import AuthContext from "../components/context/AuthContext";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useContext, useEffect, useState } from "react";
import type { GeneratedTrackerProp, TrackerProp } from '../components/interface/TrackerInterface';

const CoursePage = () => {

    const { courseId } = useParams();
    const authData = useContext(AuthContext);
    const queryClient = useQueryClient();

    const saveProgram = useSaveProgram(authData.access_token);
    const deleteFromSavedPrograms = useDeleteFromSavedPrograms(authData.access_token);
    const deleteTraining = useDeleteTrainingData(authData.access_token);
    const getScheduleFromAI = useGetScheduleFromAI();
    const sendSchedule = useSendSchedule(authData.access_token);
    const [addStatus, setAddStatus] = useState<'idle' | 'loading' | 'success'>('idle')
 
    const { data: courseData = [], isLoading: isLoadingTraining, status } = useQuery<any, Error>({
        queryKey: ['formTraining'],
        queryFn: () => currentTrainingDataRequest(courseId as String, authData.access_token),
        enabled: !!authData?.access_token && !!courseId
    })

    const { data: userData, isLoading: userDataIsLoading, status: userDataStatus } = useQuery({
        queryKey: ['me'],
        queryFn: () => userInfoRequest(authData.access_token),
        enabled: authData.access_token !== ""
    })

    const { data: isSaved, isLoading: isLoadingStatus, status: statusSaved } = useQuery({
        queryKey: ['is-saved'],
        queryFn: () => isTrainingSaved(courseId as String, authData.access_token),
        enabled: !!authData?.access_token && !!courseId,
    });

    const { data: isCreated, isLoading: isLoading, status: isCreatedStatus } = useQuery({
        queryKey: ['is-created'],
        queryFn: () => isTrainingCreatedByUser(courseId as String, authData.access_token),
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
        console.log(isCreated)
    }, [isCreated, isCreatedStatus]);

    const handleAddToSaved = () => {
        
        saveProgram.mutate(courseId, {
            onSuccess: (data) => {
                setSavedStatus(true);
                console.log(data.message);
                
                // Invalidate saved courses cache to update catalogue
                queryClient.invalidateQueries({ queryKey: ['savedCourses'] });
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
                //console.log(data.message);
                
                // Invalidate saved courses cache to update catalogue
                queryClient.invalidateQueries({ queryKey: ['savedCourses'] });
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

    const handleAddInSchedule = () => {
        setAddStatus('loading');
        
        getScheduleFromAI.mutate(
            {
                weeks: courseData["Course Duration (weeks)"],
                trainingPlan: courseData.training_plan,
                trainingProfile: userData?.training_profile,
            },
            {
                onSuccess: (data) => {

                    const scheduleWithCourseId: TrackerProp[] = data.schedule.map((item: GeneratedTrackerProp) => ({
                        ...item,
                        course_id: courseData.id,
                    }));

                    sendSchedule.mutate(scheduleWithCourseId, {
                            onSuccess: (data) => {
                                console.log(data);
                                setAddStatus('success');
                                setTimeout(() => setAddStatus('idle'), 2000);
                            },
                            onError: (error) => {
                                console.error("Error when sending the schedule:", error);
                                setAddStatus('idle');
                            }
                        }
                    );
                },
                onError: (error) => {
                    console.error("Error when adding in schedule:", error);
                    setAddStatus('idle');
                }
            }
        );

    }; 

    const training_data = transformRawCourseData(courseData);       

    return (
        <Course
            courseData={courseData}
            trainingData={training_data}
            savedStatus={savedStatus}
            isCreated={createdStatus}
            addStatus={addStatus} 
            handleAddToSaved={handleAddToSaved} 
            handleDeleteFromSaved={handleDeleteFromSaved}
            handleDeleteTraining={handleDeleteTraining}
            handleAddInSchedule={handleAddInSchedule} 
        />
    )
}

export default CoursePage