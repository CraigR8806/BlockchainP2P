import React from "react";

function Endpoint({ endpoint }) {
  const endpointContainerStyle = {
    display: "flex",
    flexDirection: "row"
  };

  const endpointColumnStyle = {
    padding: "4px"
  };

  return (
    <>
      <div style={endpointContainerStyle}>
        <div style={endpointColumnStyle}>{endpoint._Endpoint__name}</div>
        <div style={endpointColumnStyle}>{endpoint._Endpoint__uri}</div>
      </div>
    </>
  );
}

export { Endpoint };
