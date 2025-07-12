import { Link } from "react-router-dom";
import { useLogout } from "../hooks/auth";
const Navbar = () => {
  const { mutate: logout } = useLogout();

  const navlinks = [
    {
      name: "Home",
      link: "/home",
    },
    {
      name: "Dashboard",
      link: "/home/dashboard",
    },
    {
      name: "Settings",
      link: "/home/settings",
    },
  ];

  return (
    <div className="w-full flex flex-col">
      {navlinks.map((n) => {
        return (
          <Link to={n.link} key={n.name} className="btn btn-ghost">
            {n.name}
          </Link>
        );
      })}
      <button className="btn btn-error" onClick={() => logout()}>
        Logout
      </button>
    </div>
  );
};

export default Navbar;
