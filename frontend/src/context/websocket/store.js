import React, { useReducer, createContext, useContext } from "react";

import { initialState, WebSocketReducer } from "./reducer";

const WebSocketContext = createContext();

export const WebSocketProvider = ({ children }) => {
  const [store, dispatch] = useReducer(WebSocketReducer, initialState);
  return (
    <WebSocketContext.Provider value={{ store, dispatch }}>
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocketContext = () => useContext(WebSocketContext);
