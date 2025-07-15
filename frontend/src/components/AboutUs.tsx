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

      <svg style={{ position: 'absolute', width: 0, height: 0 }}>
          <filter id="blurOval" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur stdDeviation="60" />
          </filter>
      </svg>

      {/* Левая часть — картинка */}
      <div className="faq__image__container">
        <img src={notebook} alt="notebook" />
      </div>

      <div className="assets__background__gradient left-gradient" style={{ background: 'linear-gradient(45deg, rgba(229, 46, 232, 0.2) 0%, rgba(32, 228, 193, 0.2) 100%)',
                    filter: 'url(#blurOval)' }} />
      <div className="assets__background__gradient right-gradient" style={{ background: 'linear-gradient(45deg, rgba(229, 46, 232, 0.2) 0%, rgba(32, 228, 193, 0.2) 100%)',
                    filter: 'url(#blurOval)' }} />

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
      </div>
    </div>
  );
};

export default AboutUs;
