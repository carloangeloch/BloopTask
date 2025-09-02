import { Link, useNavigate } from "react-router-dom";
import { useLogout } from "../hooks/auth";
import BloopTaskLogo from "./BloopTaskLogo";
import { RxHamburgerMenu } from "react-icons/rx";
import { IoCloseOutline } from "react-icons/io5";
import { useEffect, useState } from "react";
import { motion } from "motion/react";
import { useGetUserTeam } from "../hooks/team";
import DropboxImage from "./DropboxImage";
import { useComponentStore } from "../store/componentsStore";
import { useTeamStore } from "../store/teamStore";

const Navbar = () => {
  const { isNavbarOpen, setIsNavbarOpen } = useComponentStore();
  const { mutate: logout } = useLogout();
  const [width, setWidth] = useState(window.innerWidth);
  const [closeTeamList, setCloseTeamList] = useState(false);
  const navigate = useNavigate();

  const { status, data } = useGetUserTeam();
  const { activeTeam, setActiveTeam } = useTeamStore();

  const navlinks = [
    {
      name: "🧮 Dashboard",
      link: "/home/dashboard",
      type: "link",
      data: [],
    },
    {
      name: "🌃 Teams",
      link: "",
      type: "menu",
      data: status === "pending" ? [] : data,
    },
  ];

  useEffect(() => {
    const handleWidth = () => setWidth(window.innerWidth);
    window.addEventListener("resize", handleWidth);
    return () => window.removeEventListener("resize", handleWidth);
  }, []);

  console.log(activeTeam);

  return (
    <>
      {width <= 1024 ? (
        <div className="w-full bg-gradient-to-br from-brand-blue to-brand-purple absolute flex flex-col justify-between p-3 drop-shadow-lg text-brand-white z-10">
          <div className="flex flex-col gap-y-4">
            <div className="w-full flex flex-row justify-between">
              <div
                className="flex flex-row items-center gap-x-2 cursor-pointer"
                onClick={() => {
                  setIsNavbarOpen(false);
                  navigate("/home");
                }}
              >
                <BloopTaskLogo className="w-10 drop-shadow-lg drop-shadow-blue-300/50" />
                <span> BloopTask</span>
              </div>
              <div id="close-navbar">
                {isNavbarOpen ? (
                  <button
                    className="btn btn-ghost text-brand-white"
                    onClick={() => setIsNavbarOpen(false)}
                  >
                    <IoCloseOutline size={24} />
                  </button>
                ) : (
                  <button
                    className="btn btn-ghost text-brand-white"
                    onClick={() => setIsNavbarOpen(true)}
                  >
                    <RxHamburgerMenu size={24} />
                  </button>
                )}
              </div>
            </div>
            {isNavbarOpen && (
              <div className="w-full flex-col">
                {navlinks.map((n, ind) => {
                  return (
                    <motion.div
                      key={n.name}
                      initial={
                        isNavbarOpen
                          ? { opacity: 0, display: "hidden" }
                          : { opacity: 1, display: "block" }
                      }
                      animate={
                        isNavbarOpen
                          ? { opacity: 1, display: "block" }
                          : { opacity: 0, display: "hidden" }
                      }
                      exit={
                        isNavbarOpen
                          ? { opacity: 0, display: "hidden" }
                          : { opacity: 1, display: "block" }
                      }
                      transition={{
                        duration: 0.2,
                        ease: "easeInOut",
                        delay: 0.05 * ind,
                      }}
                      className=" p-2 rounded-md mt-2"
                    >
                      {n.type === "link" ? (
                        <Link
                          to={n.link}
                          className="w-full"
                          onClick={() => setIsNavbarOpen(false)}
                        >
                          {n.name}
                        </Link>
                      ) : (
                        <div className="w-full">
                          <div>{n.name} +</div>
                          <div>
                            {n.data.map((d: { name: string }) => {
                              return <div key={d.name}>{d.name}</div>;
                            })}
                          </div>
                        </div>
                      )}
                    </motion.div>
                  );
                })}
              </div>
            )}
          </div>
          {isNavbarOpen && (
            <>
              <div
                className="h-4"
                id="
              "
              />
              <motion.button
                initial={isNavbarOpen ? { opacity: 0 } : { opacity: 1 }}
                animate={isNavbarOpen ? { opacity: 1 } : { opacity: 0 }}
                exit={isNavbarOpen ? { opacity: 0 } : { opacity: 1 }}
                transition={{
                  duration: 0.2,
                  ease: "easeInOut",
                  delay: 0.05 * navlinks.length,
                }}
                className="btn btn-error  hover:bg-red-600 text-brand-white"
                onClick={() => logout()}
              >
                Logout
              </motion.button>
            </>
          )}
        </div>
      ) : (
        <div className="w-full bg-gradient-to-br from-brand-blue/70 via-brand-blue/70 to-brand-purple/90 absolute h-screen flex flex-col justify-between p-5 text-brand-white border-r-3 border-slate-200 drop-shadow-lg">
          <div className="flex flex-col items-center gap-y-4 overflow-y-auto">
            <div className="w-full ">
              <div className="w-full flex flex-row items-center gap-x-2 hover:pl-4 duration-200 ease-in-out">
                <BloopTaskLogo className="w-10" />
                <span> BloopTask</span>
              </div>
            </div>
            {navlinks.map((n) => {
              return (
                <div key={n.name} className="w-full p-2">
                  {n.type === "link" ? (
                    <div
                      className="w-full py-2 rounded-md hover:bg-brand-purple/80 duration-200 hover:drop-shadow-lg ease-in-out hover:pl-4 cursor-pointer"
                      onClick={() => {
                        setIsNavbarOpen(false);
                        navigate(n.link);
                      }}
                    >
                      {n.name}
                    </div>
                  ) : (
                    <div className="w-full" id="teams-container">
                      <div
                        id="teams-title"
                        className="w-full  py-2 rounded-md hover:bg-brand-purple/80 duration-200 hover:drop-shadow-lg ease-in-out hover:pl-4  cursor-pointer"
                        onClick={() => setCloseTeamList(!closeTeamList)}
                      >
                        <div className="flex flex-row items-center justify-between pr-4">
                          <span>{n.name}</span>
                          {closeTeamList ? (
                            <span className="text-xl">
                              <strong>-</strong>
                            </span>
                          ) : (
                            <span className="text-xl">
                              <strong>+</strong>
                            </span>
                          )}
                        </div>
                      </div>
                      {closeTeamList && (
                        <div
                          className="w-full flex flex-col gap-y-2 mt-2"
                          id="team-list"
                        >
                          {n.data.map((d: { id: number; name: string }) => {
                            return (
                              <div
                                key={d.name}
                                className="w-full py-2 pl-6 rounded-md hover:bg-brand-purple/80 duration-200 hover:drop-shadow-lg ease-in-out hover:pl-8 flex flex-row gap-2 items-center cursor-pointer"
                                onClick={() => setActiveTeam(d.id)}
                              >
                                {d.id === activeTeam && (
                                  <div className="w-1.5 h-8 bg-brand-purple rounded-[0px_5px_5px_0px]"></div>
                                )}
                                <DropboxImage
                                  src="https://img.freepik.com/free-vector/bird-colorful-logo-gradient-vector_343694-1365.jpg?semt=ais_hybrid&w=740"
                                  alt="team-logo"
                                  className="w-8"
                                />
                                {d.name}
                              </div>
                            );
                          })}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
          <button
            className="btn btn-error  hover:bg-red-600"
            onClick={() => logout()}
          >
            Logout
          </button>
        </div>
      )}
    </>
  );
};

export default Navbar;
