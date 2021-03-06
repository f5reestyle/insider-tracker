import { getLocalStorage } from "utils/useLocalStorage";
export const initialState = {
    connection : getLocalStorage('connection',false)
  };
  
  export const WebSocketReducer = (prevState, action) => {
    switch (action.type) {
      case "":
        return {
          ...prevState,
          
        };
      case "":
        return {
          ...prevState,
         
        };
      default:
        return prevState;
    }
  };