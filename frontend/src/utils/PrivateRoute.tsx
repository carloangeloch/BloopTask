import { Navigate, Outlet } from "react-router-dom";
import { useAuthStore } from "../store/authStore";

const PrivateRouter = () => {
  const { authUser } = useAuthStore();
  return authUser ? <Outlet /> : <Navigate to="/login" />;
};

export default PrivateRouter;
