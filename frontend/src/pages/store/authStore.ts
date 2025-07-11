import { create } from "zustand";
import { axiosInstance } from "../../utils/axios";
import toast from "react-hot-toast";

type AuthUser = {
  email: string;
  first_name: string;
  last_name: string;
};

type loginData = {
  email: string;
  password: string;
};

type AuthStore = {
  authUser: null | AuthUser;
  isSigningUp: boolean;
  isLoginIn: boolean;
  isLoginOut: boolean;
  isCheckingAuth: boolean;
  login: (user: loginData) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
};

export const useAuthStore = create<AuthStore>((set) => ({
  authUser: null,
  isSigningUp: false,
  isLoginIn: false,
  isLoginOut: false,
  isCheckingAuth: false,
  login: async (data) => {
    set({ isLoginIn: true });
    try {
      const res = await axiosInstance.post("/auth/login", data);
      set({ authUser: res.data });
    } catch (error) {
      toast.error(error instanceof Error ? error.message : String(error));
    } finally {
      set({ isLoginIn: false });
    }
  },
  logout: async () => {
    set({ isLoginOut: true });
    try {
      const res = await axiosInstance.post("/auth/logout");
      console.log(res.data);
      set({ authUser: null });
    } catch (error) {
      toast.error(error instanceof Error ? error.message : String(error));
    } finally {
      set({ isLoginOut: false });
    }
  },
  checkAuth: async () => {
    set({ isCheckingAuth: true });
    try {
      const res = await axiosInstance.post("/auth/check");
      console.log(res.data);
      set({ authUser: res.data });
    } catch (error) {
      toast.error(error instanceof Error ? error.message : String(error));
    } finally {
      set({ isCheckingAuth: false });
    }
  },
}));
