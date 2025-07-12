import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import toast from "react-hot-toast";
import { useLogin } from "../../hooks/auth";
import { emailValidate } from "../../utils/emailValidate";

const LoginPage = () => {
  const { mutate: login } = useLogin();
  const defaultLoginData = {
    email: "",
    password: "",
  };
  const [showPassword, setShowPassword] = useState(false);
  const [loginData, setLoginData] = useState(defaultLoginData);

  const navigate = useNavigate();

  const handleLogin = () => {
    try {
      const isEmail = emailValidate(loginData.email);
      if (!isEmail) throw new Error("not a valid email");
      login(loginData);
      navigate("/home");
    } catch (error) {
      return toast.error(
        error instanceof Error ? error.message : String(error)
      );
    }
  };

  return (
    <>
      <Link to="/" className="btn btn-error">
        Back to home
      </Link>
      <div id="form-container">
        <label htmlFor="email">Email</label>
        <input
          type="email"
          name="email"
          className="bg-white text-black"
          onChange={(e) =>
            setLoginData((t) => ({ ...t, email: e.target.value }))
          }
        />
        <label htmlFor="password">Password</label>
        <input
          type={showPassword ? "text" : "password"}
          name="password"
          className="bg-white  text-black"
          onChange={(e) =>
            setLoginData((t) => ({ ...t, password: e.target.value }))
          }
        />
        <button onClick={() => setShowPassword(!showPassword)}>Show</button>
      </div>
      <div>
        <button className="btn btn-info" onClick={handleLogin}>
          Login
        </button>
      </div>
    </>
  );
};

export default LoginPage;
