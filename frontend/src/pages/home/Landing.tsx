import { Link } from "react-router-dom";
import DropboxImage from "../../components/DropboxImage";
import { useEffect, useState } from "react";
import { motion } from "motion/react";

const Landing = () => {
  const cardContent = [
    {
      image: "",
      title: "Intuitive Task Management",
      description: "Organize your tasks with our beautiful kanban boards",
    },
    {
      image: "",
      title: "Team Collaboration",
      description: "Work together seamlessly with your team members",
    },
    {
      image: "",
      title: "Lightning Fast",
      description: "Built for speed and efficiency in your daily workflow",
    },
    {
      image: "",
      title: "Made with Love",
      description: "Crafted with care to make your productivity journey joyful",
    },
  ];
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 400) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };

    // const handleScroll = () => {
    //   if (window.scrollY > 400) {
    //     setYValue(100);
    //   } else {
    //     setYValue(window.scrollY / 4);
    //   }
    // };

    window.addEventListener("scroll", handleScroll);

    return () => window.removeEventListener("scroll", handleScroll);
  });

  // console.log(yValue);

  return (
    <>
      <div
        id="landing-header"
        className="w-full fixed flex flex-row justify-between items-center py-2 px-4 z-10 duration-300 ease-in-out"
      >
        <div className="flex items-center gap-x-2 z-10">
          <DropboxImage
            src="https://www.dropbox.com/scl/fi/5rvp0lw5ymrrckk73ixg2/bt-transparent.png?rlkey=489xd0owh8gjbyyaxdpsm74ci&st=oo7ojmxg&dl=0"
            alt="blooptask icon"
            className="w-8"
          />
          <span className="hidden sm:block">BloopTask</span>
        </div>
        <div className="flex gap-x-4  z-10">
          <Link
            to="/login"
            className="btn btn-ghost border-0 hover:bg-brand-purple"
          >
            Sign in
          </Link>
          <Link
            to="/signup"
            className="btn bg-brand-purple border-0 hover:bg-brand-dark-purple"
          >
            Get Started
          </Link>
        </div>

        <motion.div
          initial={scrolled ? { top: 0 } : { top: "-64px" }}
          animate={scrolled ? { top: 0 } : { top: "-64px" }}
          exit={scrolled ? { top: 0 } : { top: "-64px" }}
          transition={{ duration: 0.1, ease: "easeInOut" }}
          className="absolute w-full h-16 left-0 bg-gradient-to-br from-fuchsia-400 via-brand-blue to-brand-purple drop-shadow-lg"
        ></motion.div>
      </div>
      <div
        id="hero-banner"
        className="bg-gradient-to-br from-fuchsia-400 via-brand-blue to-brand-purple w-full text-brand-white py-48"
      >
        <div
          id="title-container"
          className="flex flex-col items-center justify-center gap-y-8 w-2/3 lg:w-1/2 mx-auto text-center"
        >
          <h2 className="text-2xl lg:text-4xl">
            Task Management Made Delightful
          </h2>
          <p className="text-base lg:text-xl">
            Transform your productivity with BloopTask's intuitive kanban
            boards. Organize, prioritize, and complete your tasks with joy and
            efficiency.
          </p>
          <div className="flex flex-col md:flex-row gap-4 w-full md:w-auto">
            <button className="btn bg-brand-purple border-0 hover:bg-brand-dark-purple">
              Start Organizing
            </button>
            <button className="btn btn-outline hover:bg-brand-blue hover:border-brand-dark-blue">
              Learn More
            </button>
          </div>
        </div>
      </div>
      <div
        id="why-blooptask"
        className="w-full flex flex-col items-center justify-center bg-brand-white text-brand-black py-8 gap-y-6 text-center"
      >
        <div className="text-2xl">Why Choose BloopTask? </div>
        <div>
          Experience the perfect blend of simplicity and power in task
          management
        </div>
        <div
          id="card-container"
          className="grid grid-rows-1 md:grid-rows-2 md:grid-cols-2 xl:grid-rows-1 xl:grid-cols-4 gap-8 "
        >
          {cardContent.map((c) => {
            return (
              <div className="card w-64 shadow-sm bg-white pt-8" key={c.title}>
                <div className="w-32 h-32 rounded-[50%] bg-brand-purple mx-auto"></div>
                <div className="card-body items-center text-center">
                  <h2 className="card-title text-brand-purple">{c.title}</h2>
                  <p>{c.description}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
      <div
        id="ready-to-boost"
        className="w-full flex flex-col justify-center items-center py-16 bg-white text-black gap-y-6 px-6 text-center"
      >
        <div className="text-2xl text-brand-purple">
          Ready to Boost Your Productivity?
        </div>
        <div>
          Join thousands of users who have transformed their workflow with
          BloopTask
        </div>
        <button className="btn btn-info text-white">
          Get Started for Free
        </button>
      </div>
      <div id="footer" className="w-full py-16 bg-brand-dark-purple p-6">
        <div className="w-full xl:w-[1240px] flex flex-wrap flex-col md:flex-row mx-auto gap-y-6">
          <div className="w-full md:w-1/3 flex flex-col gap-y-2 my-2  text-center md:text-left">
            <DropboxImage
              src="https://www.dropbox.com/scl/fi/5rvp0lw5ymrrckk73ixg2/bt-transparent.png?rlkey=489xd0owh8gjbyyaxdpsm74ci&st=oo7ojmxg&dl=0"
              alt="blooptask icon"
              className="w-16 mx-auto md:mx-0"
            />
            <div>Blooptask</div>
            <div>Task Management Made Delightful</div>
            <div>@2025</div>
          </div>
          <div className="w-full md:w-1/3 flex flex-col gap-y-2 my-2  text-center md:text-left">
            <div>Navigation</div>
            <Link to="/">Home</Link>
            <Link to="#">About</Link>
            <Link to="/login">Login</Link>
            <Link to="/signup">Register</Link>
            <Link to="#">Contact us</Link>
          </div>
          <div className="w-full md:w-1/3 flex flex-col gap-y-2 my-2 text-center md:text-left">
            <div>Follow us</div>
            <div className="flex gap-4 mx-auto md:mx-0">
              <div>in</div>
              <div>Fb</div>
              <div>IG</div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Landing;
