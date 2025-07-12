import { Outlet } from "react-router-dom";
import Navbar from "../../components/Navbar";

const HomePage = () => {
  return (
    <div className="flex flex-row p-5">
      <div className="w-1/4">
        <Navbar />
      </div>
      <div className="w-3/4">
        <Outlet />
      </div>
    </div>
  );
};

export default HomePage;
