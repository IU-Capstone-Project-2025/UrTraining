import { useMutation } from "@tanstack/react-query";
import type {
    CredentialsData,
    SignInFailed,
    SignInSuccess,
    SignUpFailed,
    SignUpSuccess,
} from "../components/interface/interfaces";
import type { AxiosError } from "axios";
import { signInRequest, signUpRequest, submitSurveyRequest, submitCoachDataRequest, submitNewTrainingRequest } from "./apiRequests";
import { useNavigate } from "react-router-dom";
import type { AuthCredentialsTokens } from "../components/context/AuthContext";

// Mutation functions that is used for POST, PUT, DELETE, etc. requests
// For GET requests, Mutation is not necessary and useQuery is more preferable

export const useSignUp = () => {
    return useMutation<
        SignUpSuccess,
        AxiosError,
        CredentialsData
    >({
        mutationFn: signUpRequest
    });
};

export const useSignIn = (authData: AuthCredentialsTokens) => {
    return useMutation<
        SignInSuccess,
        AxiosError,
        CredentialsData
    >({
        mutationFn: signInRequest,
    });
};

export const useSubmitSurvey = (token: String) => {
  return useMutation({
    mutationFn: (data: any) => submitSurveyRequest(token, data),
    onSuccess: () => {
      console.log("Survey submitted successfully!");
    },
    onError: (error) => {
      console.error("Failed to submit survey: ", error);
    }
  })
};

export const useSubmitCoachData = (token: String) => {
  return useMutation({
    mutationFn: (data: any) => submitCoachDataRequest(token, data),
    onSuccess: (data) => {
      console.log(data);
      console.log("Coach data submitted successfully!");
    },
    onError: (error) => {
      console.error("Failed to submit coach data: ", error);
    }
  })
};

export const useSubmitNewTraining = (token: String) => {
  return useMutation({
    mutationFn: (data: any) => submitNewTrainingRequest(token, data),
    onSuccess: (data) => {
      console.log(data);
      console.log("New training data submitted successfully!");
      return data;
    },
    onError: (error) => {
      console.error("Failed to submit new training data: ", error);
    }
  })
};
