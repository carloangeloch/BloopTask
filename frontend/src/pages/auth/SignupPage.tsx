import { useState } from "react";
import { checkTeam, signup } from "../../api/auth";
import toast from "react-hot-toast";
import axios, { AxiosError } from "axios";
import { ErrorResponse, Link } from "react-router-dom";
import { emailValidate } from "../../utils/emailValidate";
import { useAuthStore } from "../../store/authStore";
import { BsArrowLeft } from "react-icons/bs";
import DropboxImage from "../../components/DropboxImage";
import AnimInput from "../../components/AnimInput";
import { validateString } from "../../utils/validateString";

const SignupPage = () => {
  const { checkAuth } = useAuthStore();

  const defaultTeamName = {
    name: "",
  };

  const defaultSignupForm = {
    email: "",
    password1: "",
    password2: "",
    firstName: "",
    middleName: "",
    lastName: "",
    suffix: "",
  };

  const formItemList = [
    {
      name: "email",
      type: "text",
      content: "Email Address",
    },
    {
      name: "password1",
      type: "password",
      content: "Password",
    },
    {
      name: "password2",
      type: "password",
      content: "Confirm Password",
    },
    {
      name: "firstName",
      type: "text",
      content: "First Name",
    },
    {
      name: "middleName",
      type: "text",
      content: "Middle Name",
    },
    {
      name: "lastName",
      type: "text",
      content: "Last Name",
    },
    {
      name: "suffix",
      type: "text",
      content: "Suffix",
    },
  ];

  const formItemOnChange = (
    name: string,
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    switch (name) {
      case "email":
        setSignupForm((s) => ({ ...s, email: e.target.value }));
        break;
      case "password1":
        setSignupForm((s) => ({ ...s, password1: e.target.value }));
        break;
      case "password2":
        setSignupForm((s) => ({ ...s, password2: e.target.value }));
        break;
      case "firstName":
        setSignupForm((s) => ({ ...s, firstName: e.target.value }));
        break;
      case "middleName":
        setSignupForm((s) => ({ ...s, middleName: e.target.value }));
        break;
      case "lastName":
        setSignupForm((s) => ({ ...s, lastName: e.target.value }));
        break;
      case "suffix":
        setSignupForm((s) => ({ ...s, suffix: e.target.value }));
        break;
      default:
        console.log("No matching name");
    }
  };

  const [teamName, setTeamName] = useState(defaultTeamName);
  const [signupForm, setSignupForm] = useState(defaultSignupForm);
  const [available, setAvailable] = useState(false);
  const [registerSuccess, setRegisterSuccess] = useState(true);

  const checkTeamName = async () => {
    try {
      if (teamName.name.length < 6)
        throw Error("Please use atleast 6 characters");
      const validTeam = validateString(teamName.name);
      if (!validTeam)
        throw Error("Use letters, number, underscore or hypen only.");
      const res = await checkTeam(teamName);
      if (res.status === 200) setAvailable(true);
    } catch (error) {
      const err = error as AxiosError<ErrorResponse>;
      if (axios.isAxiosError(err)) {
        const status = err.response?.status;
        console.log(status);
        if (status === 400)
          toast.error("Team already exists. Please try a different one.");
        else toast.error("Something went wrong");
      } else if (error instanceof Error) {
        toast.error(error.message);
      } else toast.error("Unexpected error occured!");
    }
  };

  const register = async () => {
    try {
      if (signupForm.password1 !== signupForm.password2) {
        toast.error("Password mismatched.");
        throw new Error("Password mismatched.");
      } else if (signupForm.password1.length < 8) {
        toast.error("Password must be at least 8 characters long.");
        throw new Error("Password must be at least 8 characters long.");
      }
      const isEmail = emailValidate(signupForm.email);
      console.log("isEmail: ", isEmail);
      if (!isEmail) {
        toast.error("Not a valid email address.");
        throw new Error("Not a valid email address.");
      }
      const formData = {
        email: signupForm.email,
        password: signupForm.password1,
        first_name: signupForm.firstName,
        middle_name: signupForm.middleName,
        last_name: signupForm.lastName,
        suffix: signupForm.suffix,
        team_name: teamName.name,
      };
      const data = await signup(formData);
      console.log(data);
      setRegisterSuccess(true);
    } catch (error: unknown) {
      const err = error as AxiosError;

      if (axios.isAxiosError(err)) {
        const data = err.response?.data as { error: string };
        toast.error(data.error);
      } else if (error instanceof Error) {
        const message = error.message;
        toast.error(message);
      } else toast.error("Unexpected error occured!");
    }
  };

  const enterKeyPressed = (
    e: React.KeyboardEvent<HTMLInputElement>,
    target_func: () => void
  ) => {
    if (e.key === "Enter") {
      target_func();
    }
  };

  return (
    <div className="w-full min-h-screen flex flex-col items-center justify-center  bg-linear-to-br from-brand-blue  to-brand-purple p-4">
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
              {registerSuccess ? (
                <h3 className="text-xl">Congratulations! 🎉</h3>
              ) : (
                <h3 className="text-xl">Create a new Account</h3>
              )}
            </div>
          </div>
          {registerSuccess ? (
            <div id="register-success">
              <div>Registration Success</div>
              <div>Let start bloop tasking</div>
              <div>
                <Link
                  to="/home"
                  className="btn btn-success text-brand-white"
                  onClick={() => checkAuth()}
                >
                  Let's go!
                </Link>
              </div>
            </div>
          ) : (
            <div id="register-account">
              <AnimInput
                type="text"
                name="team"
                content="Team Name"
                placeholder="Team Name"
                maxLength={32}
                required={true}
                disabled={available ? true : false}
                onKeyDown={(e) => enterKeyPressed(e, checkTeamName)}
                onChange={(e) =>
                  setTeamName((t) => ({ ...t, name: e.target.value }))
                }
              />
              <div className="flex flex-row justify-between items-center">
                <div className="text-green-500">
                  {available && <span>Team name is available</span>}
                </div>
                {available ? (
                  <button
                    className="btn btn-error text-brand-white mt-2"
                    onClick={() => setAvailable(false)}
                  >
                    Edit
                  </button>
                ) : (
                  <button
                    className="btn btn-success text-brand-white mt-2"
                    onClick={() => checkTeamName()}
                  >
                    Check
                  </button>
                )}
              </div>
              {available && (
                <div>
                  <hr className="my-6 text-brand-blue" />
                  <div className="text-center">Create a user account</div>
                  {formItemList.map((f) => {
                    return (
                      <AnimInput
                        key={f.name}
                        name={f.name}
                        type={f.type}
                        content={f.content}
                        placeholder={f.content}
                        required={
                          f.name === "suffix" || f.name === "middleName"
                            ? false
                            : true
                        }
                        maxLength={f.name == "suffix" ? 5 : 999}
                        onChange={(e, name = f.name) => {
                          formItemOnChange(name as string, e);
                        }}
                      />
                    );
                  })}
                  <div className="w-full flex flex-row justify-end py-4 h-16">
                    {signupForm.email != "" &&
                    signupForm.password1 != "" &&
                    signupForm.password2 != "" &&
                    signupForm.firstName != "" &&
                    signupForm.lastName != "" ? (
                      <button
                        className="btn btn-info text-brand-white"
                        onClick={() => register()}
                      >
                        Register
                      </button>
                    ) : (
                      <button className="btn bg-slate-300 border-0 cursor-default relative">
                        Register
                      </button>
                    )}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SignupPage;
