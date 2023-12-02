import React from "react";
import { GeneralInfoPanel } from "./components/GeneralInfoPanel/GeneralInfoPanel";

export const App = ({ peer }) => {
  return <>
          <GeneralInfoPanel peer={peer}></GeneralInfoPanel>
        </>;
};
