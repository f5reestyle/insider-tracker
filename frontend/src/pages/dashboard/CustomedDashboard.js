import React, { useState } from "react";
import { useAuthContext } from "context/authentication/store";
export default function Dashboard() {
  const [stocklist, setStocklist] = useState(["AAPL", "BINANCE:BTCUSDT"]);
  const { store } = useAuthContext();
  const { jwtToken, api_key } = store;

  const socket = new WebSocket(`wss://ws.finnhub.io?token=${api_key}`);

  socket.addEventListener("open", function (event) {
    stocklist.map((stock) => {
      socket.send(JSON.stringify({ type: "subscribe", symbol: stock }));
    });
  });
  socket.addEventListener("message", function (event) {
    console.log(event.data);
  });
  var unsubscribe = function (symbol) {
    socket.send(JSON.stringify({ type: "unsubscribe", symbol: symbol }));
  };
  return (
    <div>
      just dashboard
      <button onclick={unsubscribe("AAPL")}>AAPL</button>
      <button onclick={unsubscribe("BINANCE:BTCUSDT")}>BINANCE:BTCUSDT</button>
    </div>
  );
}
