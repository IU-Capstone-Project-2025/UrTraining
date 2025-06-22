import axios, { AxiosError } from "axios";
import type { CredentialsData, SignInFailed, SignInSuccess, SignUpFailed, SignUpSuccess } from "../components/interface/interfaces";

const endpoint = 'http://localhost:8000'

export async function userInfoRequest(
    token: String
): Promise<String> {
  try {
    const resp = await axios.get<String>(
      `${endpoint}/user-data`,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );
    return resp.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error) && error.response) {
      throw error as AxiosError<SignInFailed>;
    }
    throw error;
  }
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