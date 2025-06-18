import { createContext } from "react";

export interface SurveyContextType {
    currentStep: number;
    updateStep: (step: number) => void;
}

export const SurveyPageContext = createContext<SurveyContextType>({
    currentStep: 1,
    updateStep: () => {},
});

export default SurveyPageContext;
