// import React from 'react'
import Sign from "../components/Sign"
import type { SignProps } from "../components/interface/interfaces"

const SignUpPage = () => {
  const received_data: SignProps = {
    user_exists: false,
    image_path: "images/signup_image.jpg",
    page_title: "Sign Up",
    input_fields: [
      {
        name: "username",
        id: "username",
        input_type: "text",
        placeholder: "Username",
        options: ""
      },
      {
        name: "email",
        id: "email",
        input_type: "email",
        placeholder: "Email",
        options: ""
      },
      {
        name: "password",
        id: "password",
        input_type: "password",
        placeholder: "Password",
        options: ""
      },
    ],
    social_links: [
      {
        name: "google-socials",
        placeholder: "Sign Up with Google"
      },
      {
        name: "telegram-socials",
        placeholder: "Sign Up with Telegram"
      },
    ]
  }

  return (
    <>
      <Sign {...received_data} />
    </>
  )
}

export default SignUpPage