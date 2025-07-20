import axios, { AxiosError } from "axios";
import type {
    CredentialsData,
    SignInFailed,
    SignInSuccess,
    SignUpFailed,
    SignUpSuccess,
} from "../components/interface/interfaces";
import type { SurveyProp } from "../components/interface/surveyInterface";
import type { TrainingProfile, UserProp } from "../components/interface/userInterface";
import type { TrackerProp, TrackerWithDataProp } from "../components/interface/TrackerInterface"

type FlatFormData = { [key: string]: any };

const endpoint = import.meta.env.VITE_API_URL;
const ai_endpoint = import.meta.env.VITE_IMAGE2TRACKER_API_URL;
const assistant_endpoint = import.meta.env.VITE_COURSE_ASSISTANT_API_URL;
const schedule_creatror_endpoint = import.meta.env.VITE_SCHEDULE_CREATOR_API_URL;

export async function userInfoRequest(token: String): Promise<UserProp> {
    try {
        const resp = await axios.get<String>(`${endpoint}/user-data`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return resp.data as unknown as UserProp;
    } catch (error: unknown) {
        if (axios.isAxiosError(error) && error.response) {
            throw error;
        }
        throw error;
    }
}

export async function trainerDataRequest(token: String): Promise<FlatFormData> {
    try {
        const resp = await axios.get(`${endpoint}/auth/trainer-profile`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return resp.data;
    } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            throw error;
        }
        throw error;
    }
}

export async function surveyDataRequest(token: String): Promise<SurveyProp> {
    try {
        const resp = await axios.get<String>(`${endpoint}/survey-data`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return resp.data as unknown as SurveyProp;
    } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            throw error;
        }
        throw error;
    }
}

export async function coachAuthDataRequest(token: String): Promise<SurveyProp> {
    try {
        const resp = await axios.get<String>(`${endpoint}/trainer-survey-data`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return resp.data as unknown as SurveyProp;
    } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            throw error;
        }
        throw error;
    }
}

export async function trainingsDataRequest(token: String): Promise<any> {
    try {
        const resp = await axios.get<String>(`${endpoint}/trainings`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return resp.data;
    } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            throw error;
        }
        throw error;
    }
}

export async function getSavedCoursesRequest(token: String): Promise<any> {
    try {
        const resp = await axios.get<String>(`${endpoint}/saved-programs`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return resp.data;
    } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            throw error;
        }
        throw error;
    }
}

export async function isTrainingSaved(courseId: String, token: String): Promise<boolean> {
    try {
        const resp = await axios.get<{ saved: boolean }>(`${endpoint}/saved-programs/${courseId}/status`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return resp.data.saved;
    } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            throw error;
        }
        throw error;
    }
}

export async function saveProgram(courseId: any, token: String) {
    try {

        const resp = await axios.post(
            `${endpoint}/saved-programs/${courseId}`,
            {},
            {
                headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
                },
            }
        );
        return resp.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error) && error.response) {
            throw error;
        }
        throw error;
    }
}

export async function deleteFromSavedPrograms(courseId: any, token: String) {
    try {

        const resp = await axios.delete(`${endpoint}/saved-programs/${courseId}`, {
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
            },
        });
        return resp.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error) && error.response) {
            throw error;
        }
        throw error;
    }
}

export async function getMyTrainingsRequest(token: String, userId: number): Promise<any> {
    try {
        const resp = await axios.get<any>(`${endpoint}/trainings/user/${userId}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return resp.data;
    } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            throw error;
        }
        throw error;
    }
}

export async function currentTrainingDataRequest(courseId: String, token: String): Promise<any> {
    try {
        const resp = await axios.get<String>(`${endpoint}/trainings/${courseId}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return resp.data;
    } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            throw error;
        }
        throw error;
    }
}

export async function isTrainingCreatedByUser(courseId: String, token: String): Promise<boolean> {
    try {
        const resp = await axios.get<{ belongs: boolean }>(`${endpoint}/trainings/${courseId}/status`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return resp.data.belongs;
    } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            throw error;
        }
        throw error;
    }
}

export async function getRecommendations(token: String): Promise<any> {
    const response = await fetch(`${endpoint}/recommendations`, {
        headers: {
        Authorization: `Bearer ${token}`,
        }
    });
    
    if (!response.ok) {
        throw new Error('Failed to fetch recommendations');
    }
    
    const data = await response.json();
    return data.recommendations || [];
}


export async function signUpRequest(
    credentials: CredentialsData
): Promise<SignUpSuccess> {
    try {
        const resp = await axios.post<SignUpSuccess>(
            `${endpoint}/auth/register`,
            credentials
        );
        return resp.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error) && error.response) {
            throw error as AxiosError<SignUpFailed>;
        }
        throw error;
    }
}

export async function signInRequest(
    credentials: CredentialsData
): Promise<SignInSuccess> {
    try {
        const resp = await axios.post<SignInSuccess>(
            `${endpoint}/auth/login`,
            credentials
        );
        return resp.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error) && error.response) {
            throw error as AxiosError<SignInFailed>;
        }
        throw error;
    }
}

export async function logOutRequest(token: String): Promise<any> {
    try {
        const resp = await axios.post<any>(`${endpoint}/auth/logout`, {}, {
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json",
            },    
        });
        return resp.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error) && error.response) {
            throw error as AxiosError<any>;
        }
        throw error;
    }
}

export async function submitSurveyRequest(token: String, data: any) {
    try {
        console.log(data);

        const resp = await axios.post(`${endpoint}/user-data`, data, {
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
            },
        });
        return resp.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error) && error.response) {
            throw error;
        }
        throw error;
    }
}

export async function submitCoachDataRequest(token: String, data: any) {
    try {
        console.log(data);

        const resp = await axios.put(`${endpoint}/auth/trainer-profile`, data, {
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
            },
        });
        return resp.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error) && error.response) {
            throw error;
        }
        throw error;
    }
}

export async function submitNewTrainingRequest(token: String, data: any) {
    try {

        const resp = await axios.post(`${endpoint}/trainings`, data, {
            headers: { 
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
            },
        });
        return resp.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error) && error.response) {
            throw error;
        }
        throw error;
    }
}

export async function deleteTrainingData(courseId: any, token: String) {
    try {
      
        const resp = await axios.delete(`${endpoint}/trainings/${courseId}`, {
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
            },
        });
        return resp.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error) && error.response) {
            throw error;
        }
        throw error;
    }
}

export async function uploadFilesForAI(imageBase64: String) {
    try {
        const requestData = {
            image: imageBase64,
        };

        const resp = await axios.post(`${ai_endpoint}/image2tracker`, requestData, {
            headers: {
                "Content-Type": "application/json",
            },
        });
        return resp.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error) && error.response) {
            throw error;
        }
        throw error;
    }
}

// Training Progress API requests
export async function getTrainingProgress(courseId: String, token: String): Promise<any> {
    try {
        const resp = await axios.get(`${endpoint}/progress/${courseId}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return resp.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error) && error.response) {
            throw error;
        }
        throw error;
    }
}

export async function updateTrainingProgress(courseId: String, itemNumber: number, token: String): Promise<any> {
    try {
        const resp = await axios.post(`${endpoint}/progress/update`, {
            course_id: courseId,
            item_number: itemNumber
        }, {
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
            },
        });
        return resp.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error) && error.response) {
            throw error;
        }
        throw error;
    }
}

export async function resetTrainingProgress(courseId: String, token: String): Promise<any> {
    try {
        const resp = await axios.post(`${endpoint}/progress/reset`, {
            course_id: courseId
        }, {
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
            },
        });
        return resp.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error) && error.response) {
            throw error;
        }
        throw error;
    }
}

export async function getAllTrainingProgress(token: String): Promise<any> {
    try {
        const resp = await axios.get(`${endpoint}/progress/`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return resp.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error) && error.response) {
            throw error;
        }
        throw error;
    }
}

export async function sendCourseAssistantMessage(
  sessionId: String,
  query: String,
  courseData: any,
  trainingProfile: any,
): Promise<any> {
  try {
    const resp = await axios.post(
      `${assistant_endpoint}/course-assistant-chat`,
      {
        session_id: sessionId,
        query,
        user_form: "string",
        course_data: courseData,
        training_profile: trainingProfile,
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    )

    return resp.data
  } catch (error: unknown) {
    if (axios.isAxiosError(error) && error.response) {
      throw error
    }
    throw error
  }
}

function getCurrentDateString() {
        const now = new Date();

        const day = String(now.getDate()).padStart(2, '0');
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const year = now.getFullYear();

        return `${day}.${month}.${year}`;
    }

export async function getScheduleFromAssistant(weeks: number, trainingPlan: any, trainingProfile: TrainingProfile) {

    const today = new Date();

    try {
        const resp = await axios.post(
            `${schedule_creatror_endpoint}/generate-tracker`,
            {
                weeks_number: weeks,
                training_plan: trainingPlan,
                training_profile: trainingProfile,
                start_date: getCurrentDateString()
            },
            {
                headers: {
                    "Content-Type": "application/json",
                },
            }
        )
        return resp.data;

    } catch (error: unknown) {
        if (axios.isAxiosError(error) && error.response) {
            throw error;
        }
        throw error;
    }

}

export async function sendScheduleRequest(schedule: TrackerProp[], token: String): Promise<TrackerProp[]> {

    const today = new Date();

    try {
        const resp = await axios.post(`${endpoint}/tracker/schedule`, { schedule: schedule }, {
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json",
                },
            });
        return resp.data;
    } catch (error: unknown) {
        if (axios.isAxiosError(error) && error.response) {
            throw error;
        }
        throw error;
    }
}

export async function getAllScheduleRequest(token: String): Promise<TrackerProp[]> {

    try {
        const resp = await axios.get(`${endpoint}/tracker/schedule`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
        return resp.data.schedule;
    } catch (error: unknown) {
        if (axios.isAxiosError(error) && error.response) {
            throw error;
        }
        throw error;
    }
}

export async function getTrainingsByDateRequest(date: String, token: String): Promise<TrackerWithDataProp[]> {

    try {
        const resp = await axios.get(`${endpoint}/tracker/schedule/date/${date}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
        return resp.data.trainings;
    } catch (error: unknown) {
        if (axios.isAxiosError(error) && error.response) {
            throw error;
        }
        throw error;
    }
}