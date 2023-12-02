import React from "react";
import { BlockchainInfoPanel } from "./components/BlockchainInfoPanel";

export const App = ({ peer }) => {
  return <>
          <BlockchainInfoPanel peer={peer}/>
        </>;
};
