type DropboxImageType = {
  src: string;
  alt: string;
  className: string;
};

const DropboxImage = ({ src, alt, className }: DropboxImageType) => {
  return (
    <>
      <img
        src={String(src)
          .replace("www.dropbox", "dl.dropboxusercontent")
          .replace("&dl=0", "")}
        alt={alt}
        className={className}
      />
    </>
  );
};

export default DropboxImage;
