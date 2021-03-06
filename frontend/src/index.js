import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter } from "react-router-dom";
import "./index.css";
import Root from "pages/rootRoute";
import "antd/dist/antd.css";
import { AuthProvider } from "context/authentication/store";

ReactDOM.render(
  <BrowserRouter>
    <AuthProvider>
      <Root />
    </AuthProvider>
  </BrowserRouter>,
  document.getElementById("root")
);
