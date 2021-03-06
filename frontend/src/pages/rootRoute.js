import React from "react";
import { Route } from "react-router-dom";
import AppLayout from "components/AppLayout";
import AccountRoutes from "./accounts";
import CustomedDashboard from "./dashboard/CustomedDashboard";
import Dashboard from "./dashboard";
import LoginRequiredRoute from "utils/LoginRequiredRoute";
import About from "./About";

function Root() {
  return (
    <AppLayout>
      <LoginRequiredRoute exact path="/" component={Dashboard} />

      <Route exact path="/about" component={About} />
      <Route path="/accounts" component={AccountRoutes} />
    </AppLayout>
  );
}

export default Root;
