import notebook from '../assets/Side image.png';
import "../css/AboutUs.css";
import { useState } from "react";

type FAQItem = {
  question: string;
  answer: string;
};

type AboutUsProps = {
  faqItems: FAQItem[];
};

const AboutUs = ({ faqItems }: AboutUsProps) => {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const toggle = (index: number) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <div className="about-us basic-page">

      {/* Левая часть — картинка */}
      <div className="faq__image__container">
        <img src={notebook} alt="notebook" />
        <div style={{ position: "relative" }}>
          <svg
              width="1600"
              height="1600"
              viewBox="0 0 1600 1600"
              style={{
                  position: "absolute",
                  bottom: "-200px",
                  right: "-300px",
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

                  <linearGradient id="grad" x1="0%" y1="100%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="rgba(229, 46, 232, 0.25)" />
                  <stop offset="100%" stopColor="rgba(32, 228, 193, 0.25)" />
                  </linearGradient>
              </defs>

              <ellipse
                  cx="800"
                  cy="800"
                  rx="300"
                  ry="200"
                  fill="url(#grad)"
                  filter="url(#blurOval)"
              />
            </svg>
          </div>
      </div>

      

      {/* Правая часть — FAQ */}
      <div className="faq-section">
        <h2>Frequently Asked Questions</h2>
        {faqItems.map((item, index) => (
          <div
            key={index}
            className="faq-item"
          >
            <div className="faq-question" onClick={() => toggle(index)}>
              <span>{item.question}</span>
              <span className="faq-toggle">{openIndex === index ? "−" : "+"}</span>
            </div>
            <div
              className="faq-answer"
              style={{
                maxHeight: openIndex === index ? "300px" : "0",
                opacity: openIndex === index ? 1 : 0,
                marginTop: openIndex === index ? "12px" : "0",
                marginLeft: openIndex === index ? "18px" : "0",
              }}
            >
              {item.answer}
            </div>
          </div>
        ))}

        <div style={{ position: "relative" }}>
          <svg
              width="1200"
              height="1200"
              viewBox="0 0 1200 1200"
              style={{
                  position: "absolute",
                  bottom: "0px",
                  left: "-200px",
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

                  <linearGradient id="grad" x1="0%" y1="100%" x2="100%" y2="0%">
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

      </div>
    </div>
  );
};

export default AboutUs;
