import { useMutation } from "@tanstack/react-query";
import type {
    CredentialsData,
    SignInFailed,
    SignInSuccess,
    SignUpFailed,
    SignUpSuccess,
} from "../components/interface/interfaces";
import type { AxiosError } from "axios";
import { signInRequest, signUpRequest, submitSurveyRequest } from "./apiRequests";
import { useNavigate } from "react-router-dom";
import type { AuthCredentialsTokens } from "../components/context/AuthContext";

// Mutation functions that is used for POST, PUT, DELETE, etc. requests
// For GET requests, Mutation is not necessary and useQuery is more preferable

export const useSignUp = () => {
    return useMutation<
        SignUpSuccess,
        AxiosError<SignUpFailed>,
        CredentialsData
    >({
        mutationFn: signUpRequest,
        onSuccess: (data) => {
            console.log("Register success!", data);
        },
        onError: (error) => {
            console.error("Register failed:", error);
        },
    });
};

export const useSignIn = (authData: AuthCredentialsTokens) => {
    return useMutation<
        SignInSuccess,
        AxiosError<SignInFailed>,
        CredentialsData
    >({
        mutationFn: signInRequest,
        onSuccess: (data) => {
            localStorage.setItem("token", data.access_token);
            authData.setAccessToken(data.access_token);
            console.log("Logged in!");
        },
        onError: (error) => {
            console.error("Login failed: ", error);
        },
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
