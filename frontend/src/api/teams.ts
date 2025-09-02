import { axiosInstance } from "../utils/axios";

export const getUserTeams = async () => {
  const res = await axiosInstance.get("/team/all");

  return res.data;
};
