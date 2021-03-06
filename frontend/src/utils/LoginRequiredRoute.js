import React from "react";
import { useAuthContext } from "context/authentication/store";
import { Route, Redirect } from "react-router-dom";

export default function LoginRequiredRoute({
  component: Component,
  ...kwargs
}) {
  const { store } = useAuthContext();
  const isAuthenticated = store.jwtToken.length > 0;

  return (
    <Route
      {...kwargs}
      render={(props) => {
        if (isAuthenticated) {
          return <Component {...props} />;
        } else {
          return (
            <Redirect
              to={{
                pathname: "/accounts/login",
                state: { from: props.location },
              }}
            />
          );
        }
      }}
    />
  );
}
