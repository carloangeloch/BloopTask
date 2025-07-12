import { useState } from "react";
import { checkTeam, signup } from "../../api/auth";
import toast from "react-hot-toast";
import axios, { AxiosError } from "axios";
import { ErrorResponse, Link } from "react-router-dom";
import { emailValidate } from "../../utils/emailValidate";
import { useAuthStore } from "../../store/authStore";

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

  const [teamName, setTeamName] = useState(defaultTeamName);
  const [signupForm, setSignupForm] = useState(defaultSignupForm);
  const [available, setAvailable] = useState(false);
  const [registerSuccess, setRegisterSuccess] = useState(false);

  const checkTeamName = async () => {
    try {
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

  return (
    <div>
      <div>Create a new Account</div>
      {registerSuccess ? (
        <div id="register-success">
          <div>Registration Success</div>
          <div>Let start bloop tasking</div>
          <div>
            <Link
              to="/home"
              className="btn btn-success"
              onClick={() => checkAuth()}
            >
              Let's go!
            </Link>
          </div>
        </div>
      ) : (
        <div id="register-account">
          <div>check for account</div>
          <label htmlFor="team_name">Team name</label>
          <input
            type="text"
            name="teamName"
            className="bg-white text-black"
            onChange={(e) =>
              setTeamName((t) => ({ ...t, name: e.target.value }))
            }
          />
          <button className="btn btn-success" onClick={() => checkTeamName()}>
            Check
          </button>
          {available && (
            <div className="text-green-500">Team name is available</div>
          )}
          <hr />
          {available && (
            <div>
              <div>Create a user</div>
              <label htmlFor="email">Email Address</label>
              <input
                type="text"
                name="email"
                className="bg-white text-black"
                onChange={(e) =>
                  setSignupForm((s) => ({ ...s, email: e.target.value }))
                }
              />
              <br />
              <label htmlFor="password">Password</label>
              <input
                type="text"
                name="password"
                className="bg-white text-black"
                onChange={(e) =>
                  setSignupForm((s) => ({ ...s, password1: e.target.value }))
                }
              />
              <br />
              <label htmlFor="password2">Confirm Password</label>
              <input
                type="text"
                name="password2"
                className="bg-white text-black"
                onChange={(e) =>
                  setSignupForm((s) => ({ ...s, password2: e.target.value }))
                }
              />
              <br />
              <label htmlFor="firstName">First Name</label>
              <input
                type="text"
                name="firstName"
                className="bg-white text-black"
                onChange={(e) =>
                  setSignupForm((s) => ({ ...s, firstName: e.target.value }))
                }
              />
              <br />
              <label htmlFor="middleName">Middle Name</label>
              <input
                type="text"
                name="middleName"
                className="bg-white text-black"
                onChange={(e) =>
                  setSignupForm((s) => ({ ...s, middleName: e.target.value }))
                }
              />
              <br />
              <label htmlFor="lastName">Last Name</label>
              <input
                type="text"
                name="lastName"
                className="bg-white text-black"
                onChange={(e) =>
                  setSignupForm((s) => ({ ...s, lastName: e.target.value }))
                }
              />
              <br />
              <label htmlFor="suffix">Suffix</label>
              <input
                type="text"
                name="suffix"
                className="bg-white text-black"
                onChange={(e) =>
                  setSignupForm((s) => ({ ...s, suffix: e.target.value }))
                }
              />
              {signupForm.email != "" &&
                signupForm.password1 != "" &&
                signupForm.password2 != "" &&
                signupForm.firstName != "" &&
                signupForm.lastName != "" && (
                  <div onClick={() => register()}>
                    <button className="btn btn-info">Register</button>
                  </div>
                )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SignupPage;
