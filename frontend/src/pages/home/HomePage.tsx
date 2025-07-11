import { useAuthStore } from "../store/authStore";

const HomePage = () => {
  const { logout } = useAuthStore();

  return (
    <>
      <div>HomePage</div>
      <button className="btn btn-error" onClick={logout}>
        Logout
      </button>
    </>
  );
};

export default HomePage;
