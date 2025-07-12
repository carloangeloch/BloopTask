import { create } from "zustand";
import { axiosInstance } from "../utils/axios";
import toast from "react-hot-toast";
type AuthUser = {
  email: string;
  first_name: string;
  last_name: string;
};

type AuthStore = {
  authUser: null | AuthUser;
  setAuthUser: (user: AuthUser | null) => void;
  isSigningUp: boolean;
  setIsSigningUp: (signup: boolean) => void;
  isLoginIn: boolean;
  setIsLoginIn: (login: boolean) => void;
  isLoginOut: boolean;
  setIsLoginOut: (logout: boolean) => void;
  isCheckingAuth: boolean;
  setIsCheckingAuth: (check: boolean) => void;
  checkAuth: () => void;
};

export const useAuthStore = create<AuthStore>((set) => ({
  authUser: null,
  setAuthUser: (user) => set({ authUser: user }),
  isSigningUp: false,
  setIsSigningUp: (signup) => set({ isSigningUp: signup }),
  isLoginIn: false,
  setIsLoginIn: (login) => set({ isLoginIn: login }),
  isLoginOut: false,
  setIsLoginOut: (logout) => set({ isLoginOut: logout }),
  isCheckingAuth: false,
  setIsCheckingAuth: (check) => set({ isCheckingAuth: check }),
  /**
   ** we are having "no matching overload" error on using useQuery with checkauth,
   ** while using useMutation works and since we validating on App.tsx where
   ** our BrowserRouter is, which is also not embedded in QueryClientProvider,
   ** I decided to instead we make an api call here
   **/
  checkAuth: async () => {
    set({ isCheckingAuth: true });
    try {
      const res = await axiosInstance.post("/auth/check");
      set({ authUser: res.data });
      toast.success("User Verified");
    } catch (error) {
      console.error(error instanceof Error ? error.message : String(error));
    } finally {
      set({ isCheckingAuth: false });
    }
  },
}));
