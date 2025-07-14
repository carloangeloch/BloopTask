import { Link } from "react-router-dom";
import DropboxImage from "../../components/DropboxImage";

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
  return (
    <>
      <div
        id="landing-header"
        className="w-full fixed flex flex-row justify-between items-center py-2 px-4 "
      >
        <div className="flex items-center gap-x-2">
          <DropboxImage
            src="https://www.dropbox.com/scl/fi/5rvp0lw5ymrrckk73ixg2/bt-transparent.png?rlkey=489xd0owh8gjbyyaxdpsm74ci&st=oo7ojmxg&dl=0"
            alt="blooptask icon"
            className="w-8"
          />
          BloopTask
        </div>
        <div className="flex gap-x-4">
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
      </div>
      <div
        id="hero-banner"
        className="bg-gradient-to-br from-fuchsia-400 via-brand-blue to-brand-purple w-full text-brand-white py-48"
      >
        <div
          id="title-container"
          className="flex flex-col items-center justify-center gap-y-8 w-1/2 mx-auto text-center"
        >
          <h2 className="text-4xl">Task Management Made Delightful</h2>
          <p className="text-xl">
            Transform your productivity with BloopTask's intuitive kanban
            boards. Organize, prioritize, and complete your tasks with joy and
            efficiency.
          </p>
          <div className="flex flex-row gap-4">
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
        className="w-full flex flex-col items-center justify-center bg-brand-white text-brand-black py-8 gap-y-6"
      >
        <div className="text-2xl">Why Choose BloopTask? </div>
        <div>
          Experience the perfect blend of simplicity and power in task
          management
        </div>
        <div id="card-container" className="grid grid-cols-4 gap-8 ">
          {cardContent.map((c) => {
            return (
              <div className="card w-64 shadow-sm bg-white pt-8">
                <div className="w-32 h-32 rounded-[50%] bg-brand-purple mx-auto"></div>
                {/* <figure className="px-10 pt-10">
                  <img src={c.image} alt="Shoes" className="rounded-xl" />
                </figure> */}
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
        className="w-full flex flex-col justify-center items-center py-16 bg-white text-black gap-y-6"
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
      <div id="footer" className="w-full py-16 bg-brand-dark-purple">
        <div className="w-[1240px] grid grid-cols-3 gap-4 mx-auto">
          <div className="flex flex-col gap-y-2">
            <DropboxImage
              src="https://www.dropbox.com/scl/fi/5rvp0lw5ymrrckk73ixg2/bt-transparent.png?rlkey=489xd0owh8gjbyyaxdpsm74ci&st=oo7ojmxg&dl=0"
              alt="blooptask icon"
              className="w-16"
            />
            <div>Blooptask</div>
            <div>Task Management Made Delightful</div>
            <div>@2025</div>
          </div>
          <div className="flex flex-col gap-y-2">
            <div>Navigation</div>
            <Link to="/">Home</Link>
            <Link to="#">About</Link>
            <Link to="/login">Login</Link>
            <Link to="/signup">Register</Link>
            <Link to="#">Contact us</Link>
          </div>
          <div className="flex flex-col gap-y-2">
            <div>Follow us</div>
            <div className="flex gap-4">
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
