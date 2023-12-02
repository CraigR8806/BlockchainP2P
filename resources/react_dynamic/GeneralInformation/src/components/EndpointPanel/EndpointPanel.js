import React from "react";
import { Endpoint } from "./Endpoint/Endpoint";
import { useState, useEffect } from "react";

function EndpointPanel({ peer }) {
  const [endpoints, setEndpoints] = useState([]);

  const url =
    "https://" +
    peer._Peer__connection._Connection__host +
    ":" +
    peer._Peer__connection._Connection__port +
    "/diag/node/endpoints";

  const endpointPanelStyle = {
    display: "flex",
    flexDirection: "column",
    alignItems: "flex-start",
    backgroundColor: "darkcyan",
    flexGrow:"1",
    height:"100%"
  };

  useEffect(() => {
    fetch(url)
      .then(res => res.json())
      .then(data => setEndpoints(data.endpoints));
  }, [url]);

  return (
    <div style={endpointPanelStyle}>
      {endpoints &&
        endpoints.map(endpoint => {
          return <Endpoint endpoint={endpoint}></Endpoint>;
        })}
    </div>
  );
}

export { EndpointPanel };
