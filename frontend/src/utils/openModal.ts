/**
 * This function is connected with Modal component but can be also used for other component
 * @param id name of the element by id attribute
 */

export const modalOpen = (id: string) => {
  const modal = document.getElementById(id) as HTMLDialogElement | null;
  if (modal) {
    modal.showModal();
  }
};
