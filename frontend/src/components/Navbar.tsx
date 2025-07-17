import { Link } from "react-router-dom";
import { useLogout } from "../hooks/auth";
import BloopTaskLogo from "./BloopTaskLogo";

const Navbar = () => {
  const { mutate: logout } = useLogout();

  const navlinks = [
    {
      name: "🏠 Home",
      link: "/home",
    },
    {
      name: "🧮 Dashboard",
      link: "/home/dashboard",
    },
    {
      name: "⚙ Settings",
      link: "/home/settings",
    },
  ];

  return (
    <>
      <div className="w-full bg-gradient-to-br from-brand-blue/70 via-brand-blue/70 to-brand-purple/90 absolute h-screen -top-5 -left-5 flex flex-col justify-between p-5">
        <div className="flex flex-col items-center gap-y-4 overflow-y-auto">
          <div className="w-full flex flex-row items-center gap-x-2">
            <BloopTaskLogo className="w-10" />
            <span> BloopTask</span>
          </div>
          {navlinks.map((n) => {
            return (
              <div className="w-full p-2 rounded-md hover:bg-brand-purple/80 duration-200 hover:drop-shadow-lg ease-in-out hover:pl-4">
                <Link key={n.name} to={n.link} className="w-full">
                  {n.name}
                </Link>
              </div>
            );
          })}
        </div>
        <button
          className="btn btn-error text-white hover:bg-red-600"
          onClick={() => logout()}
        >
          Logout
        </button>
      </div>
    </>
  );
};

export default Navbar;
