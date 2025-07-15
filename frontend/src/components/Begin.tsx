// import React from 'react'
import { Link } from "react-router-dom";
import notebook_right from "../assets/Group 5.png"
import notebook_left from "../assets/Side 6.png"

interface BeginProps {
    css_style: string;
    button_link: string;
    text: {
        title: string;
        description: string;
        button_text: string;
    };
}

const Begin = ({ css_style, button_link, text }: BeginProps) => {

    return (
        <div className={"begin basic-page " + css_style}>

            { css_style === "begin__left" &&
                <div className="begin__image">
                    <div style={{ position: "relative" }}>
                        <div className="assets__background__gradient" style={{ background: 'linear-gradient(45deg, rgba(229, 46, 232, 0.2) 0%, rgba(32, 228, 193, 0.2) 100%)',
                        filter: 'url(#blurOval)', top: "0", right: "0" }}></div>
                    </div>
                    <img src={notebook_left} alt="" />
                </div>
            }
            <div className="begin__container">
                <div className="begin__title">
                    <h1>
                        {text.title}
                    </h1>
                </div>
                <div className="begin__description">
                    <p>
                        {text.description}
                    </p>
                </div>
                <div className={"begin__buttons " + css_style}>
                    <Link to={button_link}>
                        <button className="btn-basic-black">
                            {text.button_text}
                        </button>
                    </Link>
                </div>
            </div>
            { css_style === "begin__right" &&
                <div className="begin__image">
                    <div style={{ position: "relative" }}>
                        <div className="assets__background__gradient" style={{ background: 'linear-gradient(45deg, rgba(229, 46, 232, 0.2) 0%, rgba(32, 228, 193, 0.2) 100%)',
                        filter: 'url(#blurOval)', top: "0", right: "0" }}></div>
                    </div>
                    <img src={notebook_right} alt="" />
                </div>
            }
        </div>
    )
}

export default Begin