import React from "react";
import { EndpointPanel } from "../EndpointPanel/EndpointPanel";
import { PeerInfoPanel } from "../PeerInfoPanel/PeerInfoPanel";
import { TabController, Tab } from "../TabController/TabController";
import { PeerConfigPanel } from "../PeerConfigPanel/PeerConfigPanel";

function GeneralInfoPanel({
  peer = {
    _Peer__name: "Test Name",
    _Peer__connection: {
      _Connection__host: "node1.sara.ent.com",
      _Connection__port: "32001"
    }
  }
}) {
  const containerStyle = {
    display: "flex",
    flexDirection: "row",
    alignItems: "flex-start",
    padding: "20px",
    flexGrow: "1"
  };

  const tabObjs = [
    new Tab("Peer Information", PeerInfoPanel),
    new Tab("Peer Configuration", PeerConfigPanel),
    new Tab("Endpoints", EndpointPanel),
];

  return (
    <>
      <div style={containerStyle}>
        <TabController tabObjs={tabObjs} peer={peer}></TabController>
      </div>
    </>
  );
}

export { GeneralInfoPanel };
