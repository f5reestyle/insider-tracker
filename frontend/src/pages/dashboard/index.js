// import React, { useState } from "react";
// import { useAuthContext } from "context/authentication/store";
// import { WebSocketProvider } from "context/websocket/store";
// export default function Dashboard() {
//   const [stocklist, setStocklist] = useState(["AAPL", "BINANCE:BTCUSDT"]);

//   return <WebSocketProvider></WebSocketProvider>;
// }
import React, {
  useState,
  useCallback,
  useMemo,
  useRef,
  useEffect,
} from "react";
import { useAuthContext } from "context/authentication/store";
import useWebsocket, { ReadyState } from "react-use-websocket";
import Axios from "axios";
export default function Dashboard() {
  // TODO : stock list fetch
  const [stocklist, setStocklist] = useState([]);
  const { store } = useAuthContext();
  const { jwtToken, api_key } = store;
  const [socketUrl, setSocketUrl] = useState({
    django: "http://localhost:8000",
    finhub: `wss://ws.finnhub.io?token=${api_key}`,
  });
  const { sendMessage, lastMessage, readyState } = useWebsocket(
    socketUrl.finhub
  );
  useEffect(() => {
    Axios.get('http://localhost:8000/latestfilings');
  }, []);
  return <div></div>;
}
