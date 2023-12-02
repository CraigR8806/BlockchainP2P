/**
 * webpack-dev-server entry point for debugging.
 * This file is not bundled with the library during the build process.
 */
import { RemoteComponent } from "./RemoteComponent/RemoteComponent.js";
import React from "react";
import ReactDOM from "react-dom/client";
import LocalComponent from "./testing_index.js";

// different paths for localhost vs s3
const url =
  process.env.NODE_ENV === "development" ? "/dist/main.js" : "main.js";

const node = document.getElementById("app");

const Component = props =>
  process.env.NODE_ENV === "development"
    ? <LocalComponent {...props} />
    : <RemoteComponent url={url} {...props} />; // prettier-ignore

const App = () => (
  <>
    <Component name="Meep" />
  </>
);

const root = ReactDOM.createRoot(node);
root.render(<App />);
