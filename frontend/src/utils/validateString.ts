/**
 * Validated if string uses alphabet, numbers, underscore and hypen/dash only
 * @param name String to validate
 * @returns Boolean (true or false)
 */
export const validateString = (name: string) => {
  const regex = /^[a-zA-Z0-9_-]/;
  return regex.test(name);
};
