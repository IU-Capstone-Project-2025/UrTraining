// import React from 'react'
import { useContext, useEffect, useState } from "react";
import type { SignProps, InputField, SocialLink, CredentialsData } from "./interface/interfaces";
import '../css/Sing.css'
import SignInPageContext from "./context/SignPageContext";
import { emptyCredentials } from "./context/SignPageContext";

const Sign = (props: SignProps) => {
    const [savedData, setSavedData] = useState<CredentialsData>(emptyCredentials);

    const credentialsContext = useContext(SignInPageContext)

    const handleChange = (event: React.FormEvent<HTMLFormElement>) => {
        const target = event.target as HTMLInputElement;
        const { name, value } = target;
        setSavedData(prev => ({ ...prev, [name]: value }));
    }

    const handleSubmit = () => {
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
                                <input
                                    type={input.input_type}
                                    id={input.id}
                                    key={value}
                                    name={input.name}
                                    className='form-basic-white'
                                    placeholder={input.placeholder}
                                />
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
                                ></input>
                                <p style={{ marginLeft: "8px" }}>
                                    You agree with our Terms of Service
                                </p>
                            </label> :
                            <></>
                        }
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