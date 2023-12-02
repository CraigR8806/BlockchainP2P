import React from 'react';
import { TabController, Tab } from "./TabController/TabController";
import { BlockchainDetailsPanel } from './BlockchainDetailsPanel/BlockchainDetailsPanel';
import { BlockchainInspectionPanel } from './BlockchainInspectionPanel/BlockchainInspectionPanel';
import { BlockchainBlockCreatePanel } from './BlockchainBlockCreatePanel/BlockchainBlockCreatePanel';


function BlockchainInfoPanel({
    peer = {
      _Peer__name: "Test Name",
      _Peer__connection: {
        _Connection__host: "node1.sara.ent.com",
        _Connection__port: "32001"
      }
    }
  }){

    const containerStyle = {
        display: "flex",
        flexDirection: "row",
        alignItems: "flex-start",
        padding: "20px",
        flexGrow: "1"
      };
    
      const tabObjs = [
        new Tab("Details", BlockchainDetailsPanel),
        new Tab("Inspection", BlockchainInspectionPanel),
        new Tab("Block Create", BlockchainBlockCreatePanel)
    ];
    
      return (
        <>
          <div style={containerStyle}>
            <TabController tabObjs={tabObjs} peer={peer}></TabController>
          </div>
        </>
      );



}

export { BlockchainInfoPanel };