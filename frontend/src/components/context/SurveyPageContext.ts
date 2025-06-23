import { createContext } from "react";

export interface SurveyContextType {
    currentStep: number;
    updateStep: (step: number) => void;
    submitSurvey: (data: any) => void;
}

export const SurveyPageContext = createContext<SurveyContextType>({
    currentStep: 1,
    updateStep: () => {},
    submitSurvey: () => {}
});

export default SurveyPageContext;
