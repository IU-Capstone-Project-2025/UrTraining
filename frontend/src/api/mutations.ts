import { useMutation, useQueryClient } from "@tanstack/react-query";
import type {
    CredentialsData,
    SignInFailed,
    SignInSuccess,
    SignUpFailed,
    SignUpSuccess,
} from "../components/interface/interfaces";
import type { AxiosError } from "axios";
import { 
  signInRequest, signUpRequest, submitSurveyRequest, submitCoachDataRequest, 
  submitNewTrainingRequest, saveProgram, deleteFromSavedPrograms, deleteTrainingData, logOutRequest
} from "./apiRequests";
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

export const useSignIn = () => {
    return useMutation<
        SignInSuccess,
        AxiosError,
        CredentialsData
    >({
        mutationFn: signInRequest
    });
};

export const useSubmitSurvey = (token: String) => {
  return useMutation({
    mutationFn: (data: any) => submitSurveyRequest(data, token),
    onSuccess: (data) => {
      console.log(data);
      console.log("Survey was submitted successfully!");
      return data;
    },
    onError: (error) => {
      console.error("Failed to submit the survey: ", error);
    }
  })
};

export const useSubmitCoachData = (token: String) => {
  return useMutation({
    mutationFn: (data: any) => submitCoachDataRequest(data, token),
    onSuccess: (data) => {
      console.log(data);
      console.log("Coach Data was submitted successfully!");
      return data;
    },
    onError: (error) => {
      console.error("Failed to submit the coach data: ", error);
    }
  })
};

export const useSubmitNewTraining = (token: String) => {
  return useMutation({
    mutationFn: (data: any) => submitNewTrainingRequest(data, token),
    onSuccess: (data) => {
      console.log(data);
      console.log("Training data was submitted successfully!");
      return data;
    },
    onError: (error) => {
      console.error("Failed to submit the training data: ", error);
    }
  })
};

export const useDeleteTrainingData = (token: String) => {
  return useMutation({
    mutationFn: (courseId: any) => deleteTrainingData(courseId, token),
    onSuccess: (data) => {
      console.log(data);
      console.log("Training was deleted successfully!");
      return data;
    },
    onError: (error) => {
      console.error("Failed to delete the training: ", error);
    }
  })
};

export const useSaveProgram = (token: String) => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (courseId: any) => saveProgram(courseId, token),
    onSuccess: (data) => {
      // Инвалидируем кеш сохраненных курсов для обновления фильтров
      queryClient.invalidateQueries({ queryKey: ['savedCourses'] });
      // Инвалидируем кеш статуса сохранения
      queryClient.invalidateQueries({ queryKey: ['is-saved'] });
      
      console.log(data);
      console.log("Program was saved successfully!");
      return data;
    },
    onError: (error) => {
      console.error("Failed to save the program: ", error);
    }
  })
};

export const useDeleteFromSavedPrograms = (token: String) => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (courseId: any) => deleteFromSavedPrograms(courseId, token),
    onSuccess: (data) => {
      // Инвалидируем кеш сохраненных курсов для обновления фильтров
      queryClient.invalidateQueries({ queryKey: ['savedCourses'] });
      // Инвалидируем кеш статуса сохранения
      queryClient.invalidateQueries({ queryKey: ['is-saved'] });
      
      console.log(data);
      console.log("Program was deleted from saved successfully!");
      return data;
    },
    onError: (error) => {
      console.error("Failed to delete the program from saved: ", error);
    }
  })
};
