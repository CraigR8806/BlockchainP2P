import React from "react";

function BlockInfoPanel({ block = null }) {
  const panelStyle = {
    flexGrow: "1",
    background: "#282c34",
    margin: "20px",
    display: "flex",
    color: "white",
    flexDirection:"column",
    padding:"20px",
    alignItems:"flex-start"
  };

  const getDate = seconds => {
    const date = new Date(0);
    date.setUTCSeconds(seconds);
    return date.toString();
  };

  return (
    <>
      <div style={panelStyle}>
        <h1>Block Index: {block.index}</h1>
        <h3>Block Hash:</h3> {block.hash}
        <h3>Preivous Block Hash:</h3> {block.previous_hash}
        <h3>Date Created:</h3> {getDate(block.timestamp)}
        <h3>Data: </h3>{block.data.data}
      </div>
    </>
  );
}

export { BlockInfoPanel };
