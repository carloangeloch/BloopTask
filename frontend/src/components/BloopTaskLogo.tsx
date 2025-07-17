import DropboxImage from "./DropboxImage";

type btType = {
  className: string;
};
const BloopTaskLogo = ({ className }: btType) => {
  return (
    <>
      <DropboxImage
        src="https://www.dropbox.com/scl/fi/5rvp0lw5ymrrckk73ixg2/bt-transparent.png?rlkey=489xd0owh8gjbyyaxdpsm74ci&st=oo7ojmxg&dl=0"
        alt="blooptask icon"
        className={className}
      />
    </>
  );
};

export default BloopTaskLogo;
