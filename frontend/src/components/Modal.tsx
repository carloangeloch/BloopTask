import React from "react";

type ModalType = {
  id: string;
  className: string;
  children: React.ReactNode;
};

/**
 * This component handles all modal
 *
 * @name id: id attribute name
 * @name className: tailwindcss styles
 * @name children: components inside this modal
 *
 */

const Modal = ({ id, className, children }: ModalType) => {
  return (
    <div className="relative">
      <dialog id={id} className="modal fixed">
        <div className={`modal-box ${className}`}>{children}</div>
      </dialog>
    </div>
  );
};

export default Modal;
