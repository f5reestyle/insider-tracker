import React, { useReducer, createContext, useContext } from "react";
import useLocalStorage from "utils/useLocalStorage";
import { initialState, AuthReducer } from "./reducer";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [store, dispatch] = useReducer(AuthReducer, initialState);
  return (
    <AuthContext.Provider value={{ store, dispatch }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuthContext = () => useContext(AuthContext);

// Action Creators
