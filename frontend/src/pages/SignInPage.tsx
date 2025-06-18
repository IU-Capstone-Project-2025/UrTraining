// import React from 'react'
import Sign from "../components/Sign"
import type { SignProps } from "../components/interface/interfaces"

const SignInPage = () => {
  const received_data: SignProps = {
    user_exists: true,
    image_path: "images/signin_image.jpg",
    page_title: "Welcome back!",
    input_fields: [
      {
        name: "username",
        id: "username",
        input_type: "text",
        placeholder: "Username",
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
        placeholder: "Sign In with Google"
      },
      {
        name: "telegram-socials",
        placeholder: "Sign In with Telegram"
      },
    ]
  }

  return (
    <>
      <Sign {...received_data}/>
    </>
  )
}

export default SignInPage