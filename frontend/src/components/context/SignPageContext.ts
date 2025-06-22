import { createContext } from "react";
import type { CredentialsData } from "../interface/interfaces";

export const emptyCredentials = { username: "", email: "", password: "", full_name: "example" };

export interface SignContextType {
    credentials: CredentialsData;
    sendCredentials: (credentials: CredentialsData) => void;
}

export const SignPageContext = createContext<SignContextType>({
    credentials: emptyCredentials,
    sendCredentials: () => {}
});

export default SignPageContext;
