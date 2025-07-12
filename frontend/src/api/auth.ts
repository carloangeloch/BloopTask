import { axiosInstance } from "../utils/axios";

export const login = async (data: { email: string; password: string }) => {
  const res = await axiosInstance.post("/auth/login", data);
  return res.data;
};

export const logout = async () => {
  const res = await axiosInstance.post("/auth/logout");
  return res.data;
};

export const checkTeam = async (data: { name: string }) => {
  const res = await axiosInstance.post("/auth/team/check", data);
  return res;
};

type signupData = {
  email: string;
  password: string;
  first_name: string;
  middle_name: string;
  last_name: string;
  suffix: string;
  team_name: string;
};

export const signup = async (data: signupData) => {
  const res = await axiosInstance.post("/auth/signup", data);
  return res.data;
};
