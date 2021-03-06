import Axios from "axios";
import { setToken, deleteToken } from "./reducer";
import { setLocalStorage } from "utils/useLocalStorage";

export async function storeWebAndContext(dispatch, token, key) {
  dispatch(setToken(token, key));
  setLocalStorage("jwtToken", token);
  setLocalStorage("api_key", key);
}

export async function deleteWebAndContext(dispatch) {
  dispatch(deleteToken());
  setLocalStorage("jwtToken", "");
  setLocalStorage("api_key", "");
}
