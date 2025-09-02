import { useRef, useState } from "react";
import { FaEye } from "react-icons/fa";
import { FaEyeSlash } from "react-icons/fa";

type AnimInputType = {
  content: string;
  name: string;
  type: string;
  placeholder: string;
  maxLength?: number;
  required?: boolean;
  disabled?: boolean;
  onKeyDown?: (e: React.KeyboardEvent<HTMLInputElement>) => void;
  onChange: (
    e: React.ChangeEvent<HTMLInputElement>,
    ...args: (string | number | boolean)[]
  ) => void;
};

const AnimInput = ({
  content,
  name,
  type,
  placeholder,
  maxLength,
  required = false,
  disabled = false,
  onKeyDown,
  onChange,
}: AnimInputType) => {
  const [showPassword, setShowPassword] = useState(false);

  const refer = useRef<HTMLInputElement>(null);

  const handleClick = () => {
    if (refer.current) {
      refer.current.focus();
    }
  };

  return (
    <>
      <div id="form-input" className="relative w-full mt-6">
        <input
          ref={refer}
          type={
            type === "password" ? (showPassword ? "text" : "password") : type
          }
          name={name}
          className={`peer ${
            disabled ? "bg-slate-200 text-slate-500" : "bg-white text-black"
          } p-1 w-full rounded-lg outline-slate-200 outline-1 outline-offset-1 focus:outline-brand-purple placeholder:text-white`}
          placeholder={placeholder}
          maxLength={maxLength}
          onKeyDown={onKeyDown}
          onChange={onChange}
          required={required}
          disabled={disabled}
        />
        <label
          htmlFor={name}
          className="absolute left-1 -top-5 duration-300 ease-in-out text-brand-purple  text-xs peer-placeholder-shown:top-1 peer-placeholder-shown:text-base peer-placeholder-shown:text-slate-400 peer-focus:-top-5 peer-focus:text-xs peer-focus:text-brand-purple"
          onClick={handleClick}
        >
          {content}
          {required && (
            <span className="text-red-400">
              <strong>*</strong>
            </span>
          )}
        </label>
        {type === "password" && (
          <div
            className="absolute right-2 top-2 cursor-pointer peer-placeholder-shown:hidden"
            onClick={() => setShowPassword(!showPassword)}
          >
            {showPassword ? (
              <FaEyeSlash color="#8c50ff" />
            ) : (
              <FaEye color="#8c50ff" />
            )}
          </div>
        )}
      </div>
    </>
  );
};

export default AnimInput;
