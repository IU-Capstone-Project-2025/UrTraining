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
      </div>

      <div className="assets__background__gradient left-gradient" />
      <div className="assets__background__gradient right-gradient" />

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
