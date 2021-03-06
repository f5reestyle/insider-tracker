import { getLocalStorage } from "utils/useLocalStorage";
export const initialState = {
  jwtToken: getLocalStorage("jwtToken", ""),
  api_key: getLocalStorage("api_key", ""),
};

export const AuthReducer = (prevState, action) => {
  switch (action.type) {
    case "SET_TOKEN":
      return {
        ...prevState,
        jwtToken: action.payload.token,
        api_key: action.payload.api_key,
      };
    case "DELETE_TOKEN":
      return {
        ...prevState,
        jwtToken: "",
        api_key: "",
      };
    default:
      return prevState;
  }
};
export const setToken = (token, key) => ({
  type: "SET_TOKEN",
  payload: { token, key },
});
export const deleteToken = () => ({ type: "DELETE_TOKEN" });
