/**
 * Validate if the string is an email address type
 * @param email Email String
 * @returns Boolean (true or false)
 */

export const emailValidate = (email: string) => {
  const emailExpr = /\S+@\S+\.\S+/;
  return emailExpr.test(email);
};
