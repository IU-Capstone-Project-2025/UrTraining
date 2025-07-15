import { renderHook, waitFor } from '@testing-library/react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { vi, describe, it, expect, beforeEach, afterEach } from 'vitest';
import type { Mock } from 'vitest';
import {
  useSignUp,
  useSignIn,
  useSubmitSurvey,
  useSubmitCoachData,
  useSubmitNewTraining,
  useDeleteTrainingData,
  useSaveProgram,
  useDeleteFromSavedPrograms
} from './mutations.ts';
import {
  signUpRequest,
  signInRequest,
  submitSurveyRequest,
  submitCoachDataRequest,
  submitNewTrainingRequest,
  deleteTrainingData,
  saveProgram,
  deleteFromSavedPrograms
} from './apiRequests';

// Мокаем модули
vi.mock('@tanstack/react-query');
vi.mock('./apiRequests');
vi.mock('react-router-dom', () => ({
  useNavigate: () => vi.fn(),
}));

const mockToken = 'test-token';
const mockQueryClient = {
  invalidateQueries: vi.fn(),
};

describe('Mutation Hooks', () => {
  beforeEach(() => {
    // Мокаем useQueryClient
    (useQueryClient as unknown as Mock).mockReturnValue(mockQueryClient);
    
    // Мокаем useMutation
    (useMutation as unknown as Mock).mockImplementation((config) => ({
      mutate: vi.fn(),
      mutateAsync: vi.fn().mockImplementation(config.mutationFn),
      ...config,
    }));
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  describe('useSignUp', () => {
    it('should call signUpRequest with credentials', async () => {
      const credentials = { email: 'test@test.com', password: 'password', username: 'test', full_name: 'test test' };
      const mockResponse = { user: { id: 1 } };
      
      (signUpRequest as unknown as Mock).mockResolvedValue(mockResponse);
      
      const { result } = renderHook(() => useSignUp());
      const response = await result.current.mutateAsync(credentials);
      
      expect(signUpRequest).toHaveBeenCalledWith(credentials);
      expect(response).toEqual(mockResponse);
    });
  });

  describe('useSignIn', () => {
    it('should call signInRequest with credentials', async () => {
      const credentials = { email: 'test@test.com', password: 'password', username: 'test', full_name: 'test test' };
      const mockResponse = { token: 'test-token' };
      
      (signInRequest as unknown as Mock).mockResolvedValue(mockResponse);
      
      const { result } = renderHook(() => useSignIn());
      const response = await result.current.mutateAsync(credentials);
      
      expect(signInRequest).toHaveBeenCalledWith(credentials);
      expect(response).toEqual(mockResponse);
    });
  });

  describe('useSubmitSurvey', () => {
    it('should call submitSurveyRequest with data and token', async () => {
      const surveyData = { age: 25 };
      const mockResponse = { success: true };
      
      (submitSurveyRequest as unknown as Mock).mockResolvedValue(mockResponse);
      
      const { result } = renderHook(() => useSubmitSurvey(mockToken));
      const response = await result.current.mutateAsync(surveyData);
      
      expect(submitSurveyRequest).toHaveBeenCalledWith(surveyData, mockToken);
      expect(response).toEqual(mockResponse);
    });
  });

  describe('useSubmitCoachData', () => {
    it('should call submitCoachDataRequest with data and token', async () => {
      const coachData = { certification: 'NASM' };
      const mockResponse = { success: true };
      
      (submitCoachDataRequest as unknown as Mock).mockResolvedValue(mockResponse);
      
      const { result } = renderHook(() => useSubmitCoachData(mockToken));
      const response = await result.current.mutateAsync(coachData);
      
      expect(submitCoachDataRequest).toHaveBeenCalledWith(coachData, mockToken);
      expect(response).toEqual(mockResponse);
    });
  });

  describe('useSubmitNewTraining', () => {
    it('should call submitNewTrainingRequest with data and token', async () => {
      const trainingData = { title: 'New Program' };
      const mockResponse = { id: 123 };
      
      (submitNewTrainingRequest as unknown as Mock).mockResolvedValue(mockResponse);
      
      const { result } = renderHook(() => useSubmitNewTraining(mockToken));
      const response = await result.current.mutateAsync(trainingData);
      
      expect(submitNewTrainingRequest).toHaveBeenCalledWith(trainingData, mockToken);
      expect(response).toEqual(mockResponse);
    });
  });

  describe('useDeleteTrainingData', () => {
    it('should call deleteTrainingData with courseId and token', async () => {
      const courseId = '123';
      const mockResponse = { success: true };
      
      (deleteTrainingData as unknown as Mock).mockResolvedValue(mockResponse);
      
      const { result } = renderHook(() => useDeleteTrainingData(mockToken));
      const response = await result.current.mutateAsync(courseId);
      
      expect(deleteTrainingData).toHaveBeenCalledWith(courseId, mockToken);
      expect(response).toEqual(mockResponse);
    });
  });

  describe('useSaveProgram', () => {
    it('should call saveProgram and invalidate queries on success', async () => {
      const courseId = '123';
      const mockResponse = { success: true };
      
      (saveProgram as unknown as Mock).mockResolvedValue(mockResponse);
      
      const { result } = renderHook(() => useSaveProgram(mockToken));
      const response = await result.current.mutateAsync(courseId);
      
      expect(saveProgram).toHaveBeenCalledWith(courseId, mockToken);
      expect(response).toEqual(mockResponse);
      
      await waitFor(() => {
        expect(mockQueryClient.invalidateQueries).toHaveBeenCalledWith({
          queryKey: ['savedCourses']
        });
        expect(mockQueryClient.invalidateQueries).toHaveBeenCalledWith({
          queryKey: ['is-saved']
        });
      });
    });
  });

  describe('useDeleteFromSavedPrograms', () => {
    it('should call deleteFromSavedPrograms and invalidate queries', async () => {
      const courseId = '123';
      const mockResponse = { success: true };
      
      (deleteFromSavedPrograms as unknown as Mock).mockResolvedValue(mockResponse);
      
      const { result } = renderHook(() => useDeleteFromSavedPrograms(mockToken));
      const response = await result.current.mutateAsync(courseId);
      
      expect(deleteFromSavedPrograms).toHaveBeenCalledWith(courseId, mockToken);
      expect(response).toEqual(mockResponse);
      
      await waitFor(() => {
        expect(mockQueryClient.invalidateQueries).toHaveBeenCalledWith({
          queryKey: ['savedCourses']
        });
        expect(mockQueryClient.invalidateQueries).toHaveBeenCalledWith({
          queryKey: ['is-saved']
        });
      });
    });
  });
});
