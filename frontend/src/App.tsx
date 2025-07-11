import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { lazy, Suspense, useEffect } from "react";
import "./App.css";
import { Toaster } from "react-hot-toast";
import { useAuthStore } from "./pages/store/authStore";

import PrivateRoute from "./utils/PrivateRoute";

const PageLoading = lazy(() => import("./components/PageLoading"));
const Landing = lazy(() => import("./pages/home/Landing"));
const LoginPage = lazy(() => import("./pages/auth/LoginPage"));
const HomePage = lazy(() => import("./pages/home/HomePage"));
const DashboardPage = lazy(() => import("./pages/dashboard/DashboardPage"));
const SettingsPage = lazy(() => import("./pages/settings/SettingsPage"));

function App() {
  const { authUser, checkAuth } = useAuthStore();

  useEffect(() => {
    console.log("checking user auth");
    checkAuth();
  }, [checkAuth]);

  return (
    <>
      <Router>
        <Suspense fallback={<PageLoading />}>
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={authUser ? <HomePage /> : <Landing />} />
            <Route path="/login" element={<LoginPage />} />

            <Route element={<PrivateRoute />}>
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Route>
          </Routes>
        </Suspense>
      </Router>
      <Toaster position="bottom-center" reverseOrder={true} />
    </>
  );
}

export default App;
