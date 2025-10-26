// import React from 'react'
import '../css/BeginPage.css'
import Begin from "../components/Begin"
import { useContext } from 'react';
import { useTranslation } from "react-i18next";
import AuthContext from '../components/context/AuthContext';

const TraineeBeginPage = () => {

    const authData = useContext(AuthContext)
    const { t } = useTranslation();

    // Text data for element
    // Can be fetched from API or hardcoded
    const textProps = {
        title: t("begin_trainee.title"),
        description: t("begin_trainee.subtitle"),
        button_text: t("begin_trainee.button_text"),
        // button_2: "Smart plans",
        // button_3: "Start today"
    };

    const componentProps = {
        css_style: "begin__right",
        button_link: authData.access_token === "" ? "/signup?role=trainee" : "/survey",
        text: textProps,
    }

    return (
        <>
            <Begin {...componentProps}/>
        </>
    )
}

export default TraineeBeginPage