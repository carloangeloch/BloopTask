import { Link } from "react-router-dom";

const Landing = () => {
  return (
    <>
      <div>Welcome to BlooTask</div>
      <Link to="/login" className="btn btn-success">
        Login
      </Link>
      <Link to="/signup" className="btn btn-accent">
        Create Account
      </Link>
    </>
  );
};

export default Landing;
