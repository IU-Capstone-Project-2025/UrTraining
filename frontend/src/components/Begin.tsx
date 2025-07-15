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
                        <svg
                            width="1200"
                            height="1200"
                            viewBox="0 0 1200 1200"
                            style={{
                                position: "absolute",
                                top: "-300px",
                                right: "-400px",
                                zIndex: -1,
                                pointerEvents: "none"
                            }}
                            >
                            <defs>
                                <filter
                                id="blurOval"
                                x="-50%"
                                y="-50%"
                                width="200%"
                                height="200%"
                                filterUnits="objectBoundingBox"
                                >
                                <feGaussianBlur in="SourceGraphic" stdDeviation="80" />
                                </filter>

                                <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stopColor="rgba(229, 46, 232, 0.2)" />
                                <stop offset="100%" stopColor="rgba(32, 228, 193, 0.2)" />
                                </linearGradient>
                            </defs>

                            <ellipse
                                cx="600"
                                cy="600"
                                rx="300"
                                ry="200"
                                fill="url(#grad)"
                                filter="url(#blurOval)"
                            />
                        </svg>
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
                        <svg
                            width="1200"
                            height="1200"
                            viewBox="0 0 1200 1200"
                            style={{
                                position: "absolute",
                                top: "-300px",
                                right: "-400px",
                                zIndex: -1,
                                pointerEvents: "none"
                            }}
                            >
                            <defs>
                                <filter
                                id="blurOval"
                                x="-50%"
                                y="-50%"
                                width="200%"
                                height="200%"
                                filterUnits="objectBoundingBox"
                                >
                                <feGaussianBlur in="SourceGraphic" stdDeviation="80" />
                                </filter>

                                <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stopColor="rgba(229, 46, 232, 0.2)" />
                                <stop offset="100%" stopColor="rgba(32, 228, 193, 0.2)" />
                                </linearGradient>
                            </defs>

                            <ellipse
                                cx="600"
                                cy="600"
                                rx="300"
                                ry="200"
                                fill="url(#grad)"
                                filter="url(#blurOval)"
                            />
                        </svg>
                    </div>
                    <img src={notebook_right} alt="" />
                </div>
            }
        </div>
    )
}

export default Begin