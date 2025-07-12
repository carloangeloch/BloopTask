export const emailValidate = (email: string) => {
  const emailExpr = /\S+@\S+\.\S+/;
  return emailExpr.test(email);
};
