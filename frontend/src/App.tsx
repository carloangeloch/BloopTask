import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { lazy, Suspense, useEffect } from "react";
import "./App.css";
import { Toaster } from "react-hot-toast";
import { useAuthStore } from "./store/authStore";

import PrivateRoute from "./utils/PrivateRoute";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const PageLoading = lazy(() => import("./components/PageLoading"));
const Page404 = lazy(() => import("./components/Page404"));
const Landing = lazy(() => import("./pages/home/Landing"));
const LoginPage = lazy(() => import("./pages/auth/LoginPage"));
const SignupPage = lazy(() => import("./pages/auth/SignupPage"));
const HomePage = lazy(() => import("./pages/home/HomePage"));
const HomeOverview = lazy(() => import("./pages/home/HomeOverview"));
const DashboardPage = lazy(() => import("./pages/dashboard/DashboardPage"));
const SettingsPage = lazy(() => import("./pages/settings/SettingsPage"));

function App() {
  const { authUser, checkAuth, isCheckingAuth } = useAuthStore();
  const queryClient = new QueryClient();

  useEffect(() => {
    checkAuth();
    const interval = setInterval(() => {
      checkAuth();
    }, 1000000);
    return () => clearInterval(interval);
  }, [checkAuth]);

  return (
    <>
      <Router>
        <QueryClientProvider client={queryClient}>
          <Suspense fallback={<PageLoading />}>
            <Routes>
              {/* Public Routes */}
              <Route
                path="/"
                element={
                  isCheckingAuth ? (
                    <PageLoading />
                  ) : authUser ? (
                    <Navigate to="/home" />
                  ) : (
                    <Landing />
                  )
                }
              />
              <Route
                path="/login"
                element={
                  isCheckingAuth ? (
                    <PageLoading />
                  ) : authUser ? (
                    <Navigate to="/home" />
                  ) : (
                    <LoginPage />
                  )
                }
              />
              <Route
                path="/create"
                element={
                  isCheckingAuth ? (
                    <PageLoading />
                  ) : authUser ? (
                    <Navigate to="/home" />
                  ) : (
                    <SignupPage />
                  )
                }
              />
              <Route path="*" element={<Page404 />} />
              {/* Private Routes */}
              <Route path="/home" element={<PrivateRoute />}>
                <Route element={<HomePage />}>
                  <Route index element={<HomeOverview />} />
                  <Route path="dashboard" element={<DashboardPage />} />
                  <Route path="settings" element={<SettingsPage />} />
                </Route>
              </Route>
            </Routes>
          </Suspense>
        </QueryClientProvider>
      </Router>
      <Toaster position="bottom-center" reverseOrder={true} />
    </>
  );
}

export default App;
