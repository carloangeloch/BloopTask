import { Link } from "react-router-dom";

const Page404 = () => {
  return (
    <>
      <div>Page404</div>
      <Link to="/" className="btn btn-error">
        Go back Home!
      </Link>
    </>
  );
};

export default Page404;
