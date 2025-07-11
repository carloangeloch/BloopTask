import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import { useAuthStore } from "../store/authStore";
import toast from "react-hot-toast";

const LoginPage = () => {
  const defaultLoginData = {
    email: "",
    password: "",
  };
  const [showPassword, setShowPassword] = useState(false);
  const [loginData, setLoginData] = useState(defaultLoginData);
  const { login } = useAuthStore();

  const navigate = useNavigate();

  const handleLogin = () => {
    try {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (emailRegex.test(loginData.email) === false)
        throw new Error("not a valid email");
      login(loginData);
      navigate("/");
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
