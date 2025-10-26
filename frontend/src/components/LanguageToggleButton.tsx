import React from "react";
import { useTranslation } from "react-i18next";

const LanguageToggleButton: React.FC = () => {
  const { i18n } = useTranslation();

  const currentLang = i18n.language;

  const nextLang = currentLang.startsWith("ru") ? "en" : "ru";

  const buttonLabel =
  currentLang.startsWith("ru")
    ? "Eng"
    : "Ru";

  const handleToggle = () => {
    i18n.changeLanguage(nextLang);
  };

  return (
    <button
    onClick={handleToggle}
    className={`btn-basic-${i18n.language.startsWith("ru") ? "white" : "black"}`}
    >
        {buttonLabel}
    </button>
  );
};

export default LanguageToggleButton;