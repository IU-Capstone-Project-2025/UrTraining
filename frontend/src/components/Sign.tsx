// import React from 'react'
import type { SignProps, InputField, SocialLink } from "./interface/interfaces";
import '../css/Sing.css'

const Sign = (props: SignProps) => {
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
                    <form className='signup__form-area__options'>
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
                        <input
                            type="submit"
                            value="Let's start!"
                            className='btn-basic-black'
                        ></input>
                    </form>
                    <div className='signup__form-area__divider'></div>
                    <div className='signup__form-area__social'>
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