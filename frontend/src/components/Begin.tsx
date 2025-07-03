// import React from 'react'
import { Link } from "react-router-dom";

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
            <div className="begin__container">
                <div className="begin__title">
                    <div style={{ position: "relative" }}>
                        <div className="assets__background__gradient" style={{ top: "0", right: "0" }}></div>
                    </div>
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
        </div>
    )
}

export default Begin