import axios from "axios";
import MockAdapter from "axios-mock-adapter";
import {
  userInfoRequest,
  trainerDataRequest,
  surveyDataRequest,
  coachAuthDataRequest,
  trainingsDataRequest,
  getSavedCoursesRequest,
  isTrainingSaved,
  saveProgram,
  deleteFromSavedPrograms,
  getMyTrainingsRequest,
  currentTrainingDataRequest,
  isTrainingCreatedByUser,
  getRecommendations,
  signUpRequest,
  signInRequest,
  logOutRequest,
  submitSurveyRequest,
  submitCoachDataRequest,
  submitNewTrainingRequest,
  deleteTrainingData,
  uploadFilesForAI,
} from "../apiRequests";// Укажите правильный путь к файлу

const mock = new MockAdapter(axios);

describe("API Functions", () => {
  const token = "test-token";
  const endpoint = "http://test-endpoint";
  const ai_endpoint = "http://test-ai-endpoint";

  beforeAll(() => {
    process.env.VITE_API_URL = endpoint;
    process.env.VITE_IMAGE2TRACKER_API_URL = ai_endpoint;
  });

  afterEach(() => {
    mock.reset();
  });

  describe("userInfoRequest", () => {
    it("should return user data on successful request", async () => {
      const mockData = { id: 1, name: "Test User" };
      mock.onGet(`${endpoint}/user-data`).reply(200, mockData);

      const result = await userInfoRequest(token);
      expect(result).toEqual(mockData);
    });

    it("should throw error on failed request", async () => {
      mock.onGet(`${endpoint}/user-data`).reply(500);

      await expect(userInfoRequest(token)).rejects.toThrow();
    });
  });

  describe("trainerDataRequest", () => {
    it("should return trainer data on successful request", async () => {
      const mockData = { id: 1, isTrainer: true };
      mock.onGet(`${endpoint}/auth/trainer-profile`).reply(200, mockData);

      const result = await trainerDataRequest(token);
      expect(result).toEqual(mockData);
    });
  });

  describe("surveyDataRequest", () => {
    it("should return survey data on successful request", async () => {
      const mockData = { question: "Test", answer: "Test" };
      mock.onGet(`${endpoint}/survey-data`).reply(200, mockData);

      const result = await surveyDataRequest(token);
      expect(result).toEqual(mockData);
    });
  });

  describe("coachAuthDataRequest", () => {
    it("should return coach survey data on successful request", async () => {
      const mockData = { question: "Coach", answer: "Test" };
      mock.onGet(`${endpoint}/trainer-survey-data`).reply(200, mockData);

      const result = await coachAuthDataRequest(token);
      expect(result).toEqual(mockData);
    });
  });

  describe("trainingsDataRequest", () => {
    it("should return trainings data on successful request", async () => {
      const mockData = [{ id: 1, title: "Training 1" }];
      mock.onGet(`${endpoint}/trainings`).reply(200, mockData);

      const result = await trainingsDataRequest(token);
      expect(result).toEqual(mockData);
    });
  });

  describe("getSavedCoursesRequest", () => {
    it("should return saved courses on successful request", async () => {
      const mockData = [{ id: 1, title: "Saved Course" }];
      mock.onGet(`${endpoint}/saved-programs`).reply(200, mockData);

      const result = await getSavedCoursesRequest(token);
      expect(result).toEqual(mockData);
    });
  });

  describe("isTrainingSaved", () => {
    it("should return true if training is saved", async () => {
      const courseId = "1";
      mock.onGet(`${endpoint}/saved-programs/${courseId}/status`).reply(200, { saved: true });

      const result = await isTrainingSaved(courseId, token);
      expect(result).toBe(true);
    });
  });

  describe("saveProgram", () => {
    it("should save program successfully", async () => {
      const courseId = "1";
      mock.onPost(`${endpoint}/saved-programs/${courseId}`).reply(200, { success: true });

      await expect(saveProgram(courseId, token)).resolves.toEqual({ success: true });
    });
  });

  describe("deleteFromSavedPrograms", () => {
    it("should delete program successfully", async () => {
      const courseId = "1";
      mock.onDelete(`${endpoint}/saved-programs/${courseId}`).reply(200, { success: true });

      await expect(deleteFromSavedPrograms(courseId, token)).resolves.toEqual({ success: true });
    });
  });

  describe("getMyTrainingsRequest", () => {
    it("should return user trainings", async () => {
      const userId = 1;
      const mockData = [{ id: 1, userId }];
      mock.onGet(`${endpoint}/trainings/user/${userId}`).reply(200, mockData);

      const result = await getMyTrainingsRequest(token, userId);
      expect(result).toEqual(mockData);
    });
  });

  describe("currentTrainingDataRequest", () => {
    it("should return current training data", async () => {
      const courseId = "1";
      const mockData = { id: courseId, title: "Current Training" };
      mock.onGet(`${endpoint}/trainings/${courseId}`).reply(200, mockData);

      const result = await currentTrainingDataRequest(courseId, token);
      expect(result).toEqual(mockData);
    });
  });

  describe("isTrainingCreatedByUser", () => {
    it("should return true if training belongs to user", async () => {
      const courseId = "1";
      mock.onGet(`${endpoint}/trainings/${courseId}/status`).reply(200, { belongs: true });

      const result = await isTrainingCreatedByUser(courseId, token);
      expect(result).toBe(true);
    });
  });

  describe("getRecommendations", () => {
    it("should return recommendations", async () => {
      const mockData = { recommendations: ["rec1", "rec2"] };
      mock.onGet(`${endpoint}/recommendations`).reply(200, mockData);

      const result = await getRecommendations(token);
      expect(result).toEqual(mockData.recommendations);
    });
  });

  describe("auth functions", () => {
    describe("signUpRequest", () => {
      it("should register user successfully", async () => {
        const credentials = { email: "test@test.com", password: "password" };
        const mockResponse = { token: "new-token" };
        mock.onPost(`${endpoint}/auth/register`).reply(200, mockResponse);

        const result = await signUpRequest(credentials);
        expect(result).toEqual(mockResponse);
      });
    });

    describe("signInRequest", () => {
      it("should login user successfully", async () => {
        const credentials = { email: "test@test.com", password: "password" };
        const mockResponse = { token: "auth-token" };
        mock.onPost(`${endpoint}/auth/login`).reply(200, mockResponse);

        const result = await signInRequest(credentials);
        expect(result).toEqual(mockResponse);
      });
    });

    describe("logOutRequest", () => {
      it("should logout successfully", async () => {
        mock.onPost(`${endpoint}/auth/logout`).reply(200, { success: true });

        await expect(logOutRequest(token)).resolves.toEqual({ success: true });
      });
    });
  });

  describe("submitSurveyRequest", () => {
    it("should submit survey data successfully", async () => {
      const data = { answer: "test" };
      mock.onPost(`${endpoint}/user-data`).reply(200, { success: true });

      await expect(submitSurveyRequest(token, data)).resolves.toEqual({ success: true });
    });
  });

  describe("submitCoachDataRequest", () => {
    it("should submit coach data successfully", async () => {
      const data = { certification: "test" };
      mock.onPut(`${endpoint}/auth/trainer-profile`).reply(200, { success: true });

      await expect(submitCoachDataRequest(token, data)).resolves.toEqual({ success: true });
    });
  });

  describe("submitNewTrainingRequest", () => {
    it("should submit new training successfully", async () => {
      const data = { title: "New Training" };
      mock.onPost(`${endpoint}/trainings`).reply(200, { id: 1, ...data });

      await expect(submitNewTrainingRequest(token, data)).resolves.toEqual({ id: 1, ...data });
    });
  });

  describe("deleteTrainingData", () => {
    it("should delete training successfully", async () => {
      const courseId = "1";
      mock.onDelete(`${endpoint}/trainings/${courseId}`).reply(200, { success: true });

      await expect(deleteTrainingData(courseId, token)).resolves.toEqual({ success: true });
    });
  });

  describe("uploadFilesForAI", () => {
    it("should upload files and return AI response", async () => {
      const imageBase64 = "base64string";
      const mockResponse = { result: "AI analysis" };
      mock.onPost(`${ai_endpoint}/image2tracker`).reply(200, mockResponse);

      const result = await uploadFilesForAI(imageBase64);
      expect(result).toEqual(mockResponse);
    });
  });
});
