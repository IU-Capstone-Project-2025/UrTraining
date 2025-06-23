import { createContext } from "react";
import type { CredentialsData } from "../interface/interfaces";

export const emptyCredentials = { username: "", email: "", password: "", full_name: "example" };

export interface SignContextType {
    credentials: CredentialsData;
    submitCredentials: (credentials: CredentialsData) => void;
}

export const SignPageContext = createContext<SignContextType>({
    credentials: emptyCredentials,
    submitCredentials: () => {}
});

export default SignPageContext;
