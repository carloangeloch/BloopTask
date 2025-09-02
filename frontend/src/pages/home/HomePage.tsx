import { Outlet } from "react-router-dom";
import Navbar from "../../components/Navbar";

const HomePage = () => {
  return (
    <div className="flex flex-col lg:flex-row min-h-screen text-brand-black bg-brand-white">
      <div className="w-full lg:w-1/5 relative bg-brand-white">
        <Navbar />
      </div>
      <div className="w-full lg:w-4/5 pt-16 lg:pt-0">
        <Outlet />
      </div>
    </div>
  );
};

export default HomePage;
