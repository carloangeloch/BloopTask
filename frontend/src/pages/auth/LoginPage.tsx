import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import toast from "react-hot-toast";
import { useLogin } from "../../hooks/auth";
import { emailValidate } from "../../utils/emailValidate";
import { useAuthStore } from "../../store/authStore";
import { BsArrowLeft } from "react-icons/bs";
import DropboxImage from "../../components/DropboxImage";
import AnimInput from "../../components/AnimInput";

const LoginPage = () => {
  const { mutate: login } = useLogin();
  const { isLoginIn } = useAuthStore();
  const defaultLoginData = {
    email: "",
    password: "",
  };
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

  const checkEnter = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (
      e.key === "Enter" &&
      loginData.email != "" &&
      loginData.password != ""
    ) {
      console.log("Enter clicked!");
      handleLogin();
    }
  };

  return (
    <div className="w-full min-h-screen bg-linear-to-br from-brand-blue  to-brand-purple flex flex-col items-center justify-center p-4">
      <div
        id="login-card"
        className="w-full md:w-2/3 xl:w-1/2 2xl:w-1/4 flex flex-col gap-y-4 px-4 md:px-auto"
      >
        <Link to="/" className="text-sm flex flex-row items-center gap-x-2">
          <BsArrowLeft />
          <em>Back to home</em>
        </Link>
        <div
          id="form-container"
          className="p-12 bg-brand-white rounded-2xl text-brand-black flex flex-col"
        >
          <div id="welcome-name">
            <div className="flex flex-col items-center gap-4 p-4">
              <DropboxImage
                src="https://www.dropbox.com/scl/fi/5rvp0lw5ymrrckk73ixg2/bt-transparent.png?rlkey=489xd0owh8gjbyyaxdpsm74ci&st=oo7ojmxg&dl=0"
                alt="blooptask icon"
                className="w-24"
              />
              <h3 className="text-xl">Welcome to BloopTask</h3>
            </div>
          </div>
          <AnimInput
            content="Email Address"
            type="email"
            name="email"
            placeholder="Email Address"
            onKeyDown={checkEnter}
            onChange={(e) =>
              setLoginData((t) => ({ ...t, email: e.target.value }))
            }
          />
          <AnimInput
            content="Password"
            type="password"
            name="password"
            placeholder="Password"
            onKeyDown={checkEnter}
            onChange={(e) =>
              setLoginData((t) => ({ ...t, password: e.target.value }))
            }
          />
          <div className="w-full mt-4" id="login-btn">
            {loginData.email != "" && loginData.password != "" ? (
              isLoginIn ? (
                <button className="btn btn-ghost w-full" onClick={handleLogin}>
                  <span className="loading loading-dots loading-md"></span>
                </button>
              ) : (
                <button
                  className="btn btn-info w-full text-white"
                  onClick={handleLogin}
                >
                  Login
                </button>
              )
            ) : (
              <button className="btn btn-info w-full cursor-default opacity-10 text-white">
                Login
              </button>
            )}
          </div>
          <div className="divider divide-error">OR</div>
          <div id="google-btn">
            <button
              className="btn bg-white text-black border-[#e5e5e5] w-full"
              onClick={() => toast("Coming soon", { icon: "⌛" })}
            >
              <svg
                aria-label="Google logo"
                width="16"
                height="16"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 512 512"
              >
                <g>
                  <path d="m0 0H512V512H0" fill="#fff"></path>
                  <path
                    fill="#34a853"
                    d="M153 292c30 82 118 95 171 60h62v48A192 192 0 0190 341"
                  ></path>
                  <path
                    fill="#4285f4"
                    d="m386 400a140 175 0 0053-179H260v74h102q-7 37-38 57"
                  ></path>
                  <path
                    fill="#fbbc02"
                    d="m90 341a208 200 0 010-171l63 49q-12 37 0 73"
                  ></path>
                  <path
                    fill="#ea4335"
                    d="m153 219c22-69 116-109 179-50l55-54c-78-75-230-72-297 55"
                  ></path>
                </g>
              </svg>
              Login with Google
            </button>
          </div>
          <div className="text-center mt-8 text-sm">
            <p>
              Don’t have an account?{" "}
              <span className="hover:text-brand-purple hover:underline hover:underline-offset-4 cursor-pointer">
                Let us create one!
              </span>
            </p>
          </div>
          <div className="text-center mt-2 text-sm">
            <p className="hover:text-brand-purple hover:underline hover:underline-offset-4 cursor-pointer">
              Forgot your password?
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
