import AboutUs from "../components/AboutUs";

type FAQItem = {
  question: string;
  answer: string;
};

const faqItems: FAQItem[] = [
  {
    question: "What is UrTraining and how does it work?",
    answer: "UrTraining is a web-based platform for creating, distributing, and following personalized training plans. Users receive AI-assisted workout recommendations based on their fitness goals and preferences. Trainers can upload and manage their own structured programs for users to follow.",
  },
  {
    question: "Do I need to register to browse the courses?",
    answer: "Currently, registration is required to access full course details. We are working on adding preview options for unregistered users.",
  },
  {
    question: "How long does the personalization questionnaire take?",
    answer: "It takes about 3–5 minutes and helps tailor the training plan to your needs or recommend your plans to the right audience (for trainers).",
  },
  {
    question: "Is the platform free to use?",
    answer: "Yes, UrTraining is free. However, we may introduce paid features in the future for advanced tools or monetization options.",
  },
  {
    question: "How do I start a workout or course after registering?",
    answer: "Once registered and the questionnaire is complete, you'll receive workout recommendations and can start directly from the catalog. Your active programs appear in your profile.",
  },
  {
    question: "How do I switch between trainer and trainee roles?",
    answer: "The role is selected during registration and currently cannot be changed. You can log out and create a new account. Role-switching will be available in future updates.",
  },
  {
    question: "What kind of workouts are available on the platform?",
    answer: "We currently offer strength training, cardio, HIIT, yoga, pilates, functional training, CrossFit, bodybuilding, stretching, running, swimming, cycling, boxing, and dancing. You can suggest new types!",
  },
  {
    question: "How are personalized workouts generated?",
    answer: "After completing the questionnaire, AI selects and adjusts workouts based on your fitness level, goals, preferences, and available equipment. Workouts are authored by qualified trainers.",
  },
  {
    question: "Will I receive money for creating the courses?",
    answer: "At the moment, there is no monetization. However, trainer compensation features are being considered for future updates.",
  },
  {
    question: "Why do I need to add certificates of my education?",
    answer: "Certificates help verify your qualifications and build user trust. Verified trainers may receive more visibility on the platform.",
  },
  {
    question: "What if I have a workout type not listed in the predefined list?",
    answer: "We are continuously expanding the list. Feel free to suggest new workout categories.",
  },
  {
    question: "Can I upload photos of the exercise plan?",
    answer: "Photo and video support for exercise plans is in development. Stay tuned for future updates.",
  },
  {
    question: "Is there a Russian version of the platform?",
    answer: "Not yet, but localization is in progress — a Russian version is planned soon.",
  },
  {
    question: "What are the terms I agree to during registration?",
    answer: "You agree to our terms of service, which cover content usage, data privacy, user conduct, and platform policies.",
  },
  {
    question: "How do I log out of my account?",
    answer: "Just go to your profile page and click the logout button.",
  },
];

const AboutUsPage = () => {

  return (
    <AboutUs faqItems={faqItems} />
  )
}

export default AboutUsPage;