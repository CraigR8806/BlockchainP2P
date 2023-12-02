import React from "react";
import { useState, useEffect } from "react";
import { TabSelectionPanel } from "./TabSelectionPanel/TabSelectionPanel";
import { TabPane } from "./TabPane/TabPane";

class Tab {
  constructor(name, component) {
    this.name = name;
    this.component = component;
    this.uuid = crypto.randomUUID();
  }

  getForTabList() {
    return { name: this.name, uuid: this.uuid };
  }
}

function TabController({tabObjs, ...props}) {
  const [selectedTab, setSelectedTab] = useState(tabObjs[0]);
  const [selectedComponent, setSelectedComponent] = useState(() => props => (
    <selectedTab.component {...props} />
  ));

  const tabSelect = uuid => {
    setSelectedTab(tabObjs.find(tab => tab.uuid === uuid));
  };
  useEffect(() => {
    setSelectedComponent(() => props => <selectedTab.component {...props} />);
  }, [selectedTab]);

  const tabs = tabObjs.map(tab => tab.getForTabList());

  return (
    <>
      <TabSelectionPanel tabs={tabs} onClick={tabSelect} />
      <TabPane Component={selectedComponent} {...props} />
    </>
  );
}

export { TabController, Tab };
