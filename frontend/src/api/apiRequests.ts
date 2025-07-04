import axios, { AxiosError } from "axios";
import type {
    CredentialsData,
    SignInFailed,
    SignInSuccess,
    SignUpFailed,
    SignUpSuccess,
} from "../components/interface/interfaces";
import type { SurveyProp } from "../components/interface/surveyInterface";
import type { UserProp } from "../components/interface/userInterface";

type FlatFormData = { [key: string]: any };

const endpoint = import.meta.env.VITE_API_URL;

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
        console.log("бро красава")
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
        // console.log("бро красава")
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
        // console.log("бро красава")
        return resp.data;
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
