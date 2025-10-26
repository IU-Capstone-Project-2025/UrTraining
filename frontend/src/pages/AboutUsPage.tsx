import AboutUs from "../components/AboutUs";
import { useTranslation } from "react-i18next";

type FAQItem = {
  question: string;
  answer: string;
};

const getFaqItems = (t: (key: string) => string): FAQItem[] => [
  {
    question: t("faq.q1.question"),
    answer: t("faq.q1.answer"),
  },
  {
    question: t("faq.q2.question"),
    answer: t("faq.q2.answer"),
  },
  {
    question: t("faq.q3.question"),
    answer: t("faq.q3.answer"),
  },
  {
    question: t("faq.q4.question"),
    answer: t("faq.q4.answer"),
  },
  {
    question: t("faq.q5.question"),
    answer: t("faq.q5.answer"),
  },
  {
    question: t("faq.q6.question"),
    answer: t("faq.q6.answer"),
  },
  {
    question: t("faq.q7.question"),
    answer: t("faq.q7.answer"),
  },
  {
    question: t("faq.q8.question"),
    answer: t("faq.q8.answer"),
  },
  {
    question: t("faq.q9.question"),
    answer: t("faq.q9.answer"),
  },
  {
    question: t("faq.q10.question"),
    answer: t("faq.q10.answer"),
  },
  {
    question: t("faq.q11.question"),
    answer: t("faq.q11.answer"),
  },
  {
    question: t("faq.q12.question"),
    answer: t("faq.q12.answer"),
  },
  {
    question: t("faq.q13.question"),
    answer: t("faq.q13.answer"),
  },
  {
    question: t("faq.q14.question"),
    answer: t("faq.q14.answer"),
  },
  {
    question: t("faq.q15.question"),
    answer: t("faq.q15.answer"),
  },
];

const AboutUsPage = () => {
  const { t } = useTranslation();
  const faqItems = getFaqItems(t);

  return <AboutUs faqItems={faqItems} />;
};

export default AboutUsPage;
