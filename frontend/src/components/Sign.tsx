// import React from 'react'
import { useContext, useEffect, useState } from "react";
import type { SignProps, InputField, SocialLink, CredentialsData } from "./interface/interfaces";
import '../css/Sing.css'
import SignInPageContext from "./context/SignPageContext";
import { emptyCredentials } from "./context/SignPageContext";

const Sign = (props: SignProps) => {
    const [savedData, setSavedData] = useState<CredentialsData>(emptyCredentials);
    const [agreementChecked, setAgreementChecked] = useState(false);
    const [showAgreementError, setShowAgreementError] = useState(false);
    const [showPassword, setShowPassword] = useState(false);

    const credentialsContext = useContext(SignInPageContext)

    const handleChange = (event: React.FormEvent<HTMLFormElement>) => {
        const target = event.target as HTMLInputElement;
        const { name, value } = target;
        setSavedData(prev => ({ ...prev, [name]: value }));
    }

    const handleSubmit = () => {
        if (!agreementChecked && !props.user_exists) {
            setShowAgreementError(true);
            return;
        }

        credentialsContext.submitCredentials(savedData)
    }

    return (
        <div className="signup basic-page">
            <div className='signup__container'>
                <div className='signup__image'>
                    <img src={props.image_path} alt="" />
                </div>
                <div className='signup__form-area'>
                    <h2 className='signup__form-area__title'>
                        {props.page_title}
                    </h2>
                    <form className='signup__form-area__options' onChange={handleChange} onSubmit={(e) => e.preventDefault()}>
                        {props.input_fields.map((input: InputField, value: number) => {
                            return (
                                <>
                                    <input
                                    key={input.id}
                                    type={input.name === "password" && showPassword ? "text" : input.input_type}
                                    id={input.id}
                                    name={input.name}
                                    className='form-basic-white'
                                    placeholder={input.placeholder}
                                    />
                                    {input.name === "password" && (
                                    <button
                                        type="button"
                                        onClick={() => setShowPassword(prev => !prev)}
                                        style={{
                                        marginLeft: "8px",
                                        background: "none",
                                        border: "none",
                                        color: "gray",
                                        cursor: "pointer",
                                        }}
                                    >
                                        {showPassword ? "Hide password" : "Show password"}
                                    </button>
                                    )}
                                </>
                            );
                        })}
                        {!props.user_exists ?
                            <label
                                style={{ display: "flex", alignItems: "baseline" }}
                            >
                                <input
                                    type="checkbox"
                                    id="agreement"
                                    name="agreement"
                                    className='checkbox-basic-white'
                                    value="Boat"
                                    checked={agreementChecked}
                                    onChange={(e) => {
                                        setAgreementChecked(e.target.checked);
                                        setShowAgreementError(false);
                                    }}
                                ></input>
                                <p style={{ marginLeft: "8px" }}>
                                    You agree with our Terms of Service
                                </p>
                            </label> :
                            <></>
                        }
                        {showAgreementError && (
                        <div className="signup__form-area__error">
                            Please, confirm the Terms of Use
                        </div>
                        )}
                        {
                            credentialsContext.isError &&
                            <div className="signup__form-area__error">
                                {credentialsContext.errorMessage}
                            </div>
                        }
                        <button
                            className='btn-basic-black'
                            onClick={handleSubmit}
                        >Let's start!</button>
                    </form>
                    <div className='signup__form-area__divider' style={{ display: "none" }}></div>
                    <div className='signup__form-area__social' style={{ display: "none" }}>
                        {props.social_links.map((social: SocialLink, value: number) => {
                            return (<button key={value} className='btn-basic-white'>
                                {social.placeholder}
                            </button>);
                        })}
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Sign