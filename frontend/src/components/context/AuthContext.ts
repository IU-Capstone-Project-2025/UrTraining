import React, { createContext } from 'react'

export interface AuthCredentialsTokens {
  access_token: String;
  setAccessToken: (new_token: String) => void;
}

export const AuthContext = createContext<AuthCredentialsTokens>({
  access_token: "",
  setAccessToken: () => {}
});

export default AuthContext