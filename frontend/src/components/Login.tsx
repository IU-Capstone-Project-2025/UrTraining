import { useState } from "react";
import "../css/Login.css";
// import SignUp_Image from "../assets/signup_image.jpg";
import { api } from "../api";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const onSubmit = async () => {
    try {
      const response = await api.post("/login", { email, password });
      console.log(response.data);
    } catch (e) {
      console.log(e);
    }
  };

  return (
    <div className="login__container">
      <div className="login__image">
        <h1>Join today and become a great member of our family</h1>
        <span>We value every member of our group, even the black one!</span>
      </div>

      <div className="login__form">
        <h1 className="login__title">Login</h1>

        <input
          className="form-basic-white login__input"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          className="form-basic-white login__input"
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button className="login__button submit" onClick={onSubmit}>
          Login
        </button>

        <div className="login__divider" />

        <div className="login__alternatives">
          <button className="login__button btn-white">Login with Google</button>
          <button className="login__button btn-white">
            Login with Telegram
          </button>
        </div>
      </div>
    </div>
  );
};

export default Login;
