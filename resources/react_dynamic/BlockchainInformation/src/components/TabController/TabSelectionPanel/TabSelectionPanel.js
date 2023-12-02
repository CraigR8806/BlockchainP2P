import React from "react";
import { useState } from "react";

function TabSelectionPanel({ tabs = [], onClick = () => {} }) {
  const [selected, setSelected] = useState(tabs[0].uuid);
  const [hovered, setHovered] = useState(0);

  function getTabStyle(uuid) {
    const isHovered = hovered === uuid;
    const isSelected = selected === uuid;

    const backgroundColor = isSelected
      ? `#282c34`
      : hovered === uuid
      ? `darkslategrey`
      : `rgb(77, 85, 101)`;

    const boxShadowStyleObj = {
      horizLength: (isSelected ? "-1" : "3") + "px",
      verticalLength: (isSelected ? "-1" : "3") + "px",
      blur: "2px",
      spread: "1px",
      color: isSelected ? "darkcyan" : "#333",
      inset: isHovered && !isSelected ? "" : "inset"
    };

    const boxShadowStyle =
      isSelected || isHovered
        ? boxShadowStyleObj.horizLength +
          " " +
          boxShadowStyleObj.verticalLength +
          " " +
          boxShadowStyleObj.blur +
          " " +
          boxShadowStyleObj.spread +
          " " +
          boxShadowStyleObj.color +
          " " +
          boxShadowStyleObj.inset
        : `none`;

    return {
      background: backgroundColor,
      padding: "10px",
      fontSize: "larger",
      display: "flex",
      borderRadius: `30px`,
      marginRight: "10px",
      marginBottom: "5px",
      marginLeft:"5px",
      paddingLeft: "15px",
      boxShadow: boxShadowStyle
    };
  }

  function tabSelected(uuid) {
    setSelected(uuid);
    onClick(uuid);
  }

  const tabSelectionPanelStyle = {
    display: "flex",
    flexDirection: "column",
    width: "18%",
    height: "100%",
    overflowY: "scroll"
  };

  return (
    <div style={tabSelectionPanelStyle}>
      {tabs.map(tab => {
        return (
          <div
            key={tab.uuid}
            style={getTabStyle(tab.uuid)}
            onClick={() => tabSelected(tab.uuid)}
            onMouseEnter={() => setHovered(tab.uuid)}
            onMouseLeave={() => setHovered(0)}
          >
            {tab.name}
          </div>
        );
      })}
    </div>
  );
}

export { TabSelectionPanel };
