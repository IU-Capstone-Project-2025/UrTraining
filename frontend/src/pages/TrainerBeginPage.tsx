// import React from 'react'
import '../css/BeginPage.css'
import Begin from "../components/Begin"
import { useContext } from 'react';
import { useTranslation } from "react-i18next";
import AuthContext from '../components/context/AuthContext';


const TrainerBeginPage = () => {
    const authData = useContext(AuthContext)
    const { t } = useTranslation();

    const textProps = {
        title: t("begin_trainer.title"),
        description: t("begin_trainer.subtitle"),
        button_text: t("begin_trainer.button_text"),
        // button_2: "Grow audience",
        // button_3: "Monetize expertise"
    };

    const componentProps = {
        css_style: "begin__left",
        button_link: authData.access_token === "" ? "/signup?role=trainer" : "/trainer-registration",
        text: textProps,
    }

    return (
        <>
            <Begin {...componentProps}/>
        </>
    )
}

export default TrainerBeginPage