import { Link } from "react-router-dom";
import Login from "../components/Login";

const LoginPage = () => {
  return (
    <div>
      <div className="login__navbar__logo">
        <Link to="/">
          <h1>URTRAINING</h1>
        </Link>
      </div>
      <Login />
    </div>
  );
};

export default LoginPage;
