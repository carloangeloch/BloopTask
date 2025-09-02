import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useAuthStore } from "../store/authStore";
import { login, logout } from "../api/auth";
import toast from "react-hot-toast";
import axios, { AxiosError } from "axios";

export const useLogin = () => {
  const { setAuthUser, setIsLoginIn } = useAuthStore();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: login,
    onMutate: () => {
      setIsLoginIn(true);
    },
    onSettled: () => {
      setIsLoginIn(false);
    },
    onSuccess: (data) => {
      setAuthUser(data);
      toast.success("Login Successfull");
      queryClient.invalidateQueries({ queryKey: ["auth"] });
    },
    onError: (error) => {
      const err = error as AxiosError;

      if (axios.isAxiosError(err)) {
        const data = err.response?.data as { error: string };
        toast.error(data.error);
      } else if (error instanceof Error) {
        const message = error.message;
        toast.error(message);
      } else toast.error("Something went wrong!");
    },
  });
};

export const useLogout = () => {
  const { setAuthUser } = useAuthStore();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: logout,
    onSuccess: () => {
      setAuthUser(null);
      toast.success("Logout Successfully");
      queryClient.invalidateQueries({ queryKey: ["auth"] });
    },
    onError: (error: Error | string) => {
      toast.error(error instanceof Error ? error.message : String(error));
    },
  });
};
