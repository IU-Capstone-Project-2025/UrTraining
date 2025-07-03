import { createContext } from "react";
import type { CredentialsData } from "../interface/interfaces";

export const emptyCredentials = { username: "", email: "", password: "", full_name: "example" };

export interface SignContextType {
    credentials: CredentialsData;
    isError: boolean;
    errorMessage: string;
    submitCredentials: (credentials: CredentialsData) => void;
}

export const SignPageContext = createContext<SignContextType>({
    credentials: emptyCredentials,
    isError: false,
    errorMessage: "",
    submitCredentials: () => {}
});

export default SignPageContext;
