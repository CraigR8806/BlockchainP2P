import React from "react";

import { Block } from "./Block";
import { useState, useEffect } from "react";
import { useInterval } from "./UseInterval";
import { BlockInfoPanel } from "./BlockInfoPanel";

function BlockchainInspectionPanel({ peer, maxBlocksShown = 12 }) {
  const hostport =
    "https://" +
    peer._Peer__connection._Connection__host +
    ":" +
    peer._Peer__connection._Connection__port;

  const [shownBlocks, setShownBlocks] = useState([]);
  const [chainLength, setChainLength] = useState(-1);
  const [chainViewRange, setChainViewRange] = useState({ start: 0, end: 0 });
  const [chainView, setChainView] = useState([]);
  const [chainArray, setChainArray] = useState([]);
  const [basePosition, setBasePosition] = useState(10);
  const [selectedBlock, setSelectedBlock] = useState(null);
  const [makingBlockRequest, setMakingBlockRequest] = useState(true);
  const [inBottomZone, setInBottomZone] = useState(false);
  const [inTopZone, setInTopZone] = useState(false);
  const [atTop, setAtTop] = useState(false);
  const [atBottom, setAtBottom] = useState(false);
  const [lastScrollPosition, setLastScrollPosotion] = useState(0);

  useInterval(() => {
    fetch(hostport + "/chain/length")
      .then(res => res.json())
      .then(data => {
        setChainLength(data);
        if (chainViewRange.start == 0 && chainViewRange.end == 0) {
          setChainViewRange({
            start: 0,
            end: data <= maxBlocksShown ? data : maxBlocksShown
          });
        }
      });
  }, 1000);

  useEffect(() => {
    if (!makingBlockRequest || chainViewRange.end - chainViewRange.start <= 0)
      return;
    const url =
      hostport +
      "/chain/blocks?start=" +
      chainViewRange.start +
      "&end=" +
      chainViewRange.end;
    fetch(url)
      .then(res => res.json())
      .then(data => setChainView(data))
      .then(() => setMakingBlockRequest(false));
  }, [hostport, chainViewRange, makingBlockRequest]);

  const edgeStyle = {
    display: "flex",
    width: "5px",
    background: "black",
    minHeight: "20px"
  };

  const onBlockSelect = block => {
    setSelectedBlock(block);
  };

  useEffect(() => {
    if (chainView.length == 0) return;
    const tmpArray = [];
    for (let i = 0; i < chainView.length - 1; i++) {
      tmpArray.push(
        <Block
          onBlockSelect={onBlockSelect}
          key={chainView[i].hash}
          block={chainView[i]}
        />
      );
      tmpArray.push(<div key={i + chainView[i].hash} style={edgeStyle}></div>);
    }
    tmpArray.push(
      <Block
        onBlockSelect={onBlockSelect}
        key={chainView[chainView.length - 1].hash}
        block={chainView[chainView.length - 1]}
      />
    );
    setChainArray(tmpArray);
  }, [chainView, basePosition]);

  
  const chainPanelStyle = {
    display: "flex",
    width: "20%",
    flexDirection: "column",
    alignItems: "center",
    overflow: "scroll",
    marginTop: "20px",
    marginLeft: "20px",
    marginBottom: "20px",
    padding: "10px",
    overflow: "scroll",
    background: "#282c34"
  };

  const blockchainInspectionPanelStyle = {
    display: "flex",
    flexDirection: "row",
    flexGrow: "1",
    overflow: "hidden",
    height: "100%"
  };


  const onScroll = e => {
    if (makingBlockRequest) return;
    let tag = e.currentTarget;
    let direction = e.deltaY/Math.abs(e.deltaY);
    setLastScrollPosotion(tag.scrollTop);

    

    setInBottomZone(
      !inBottomZone &&
        tag.scrollTop >= (tag.scrollHeight - tag.offsetHeight) * 0.85
    );
    setInTopZone(
      !inTopZone &&
        tag.scrollTop <= (tag.scrollHeight - tag.offsetHeight) * 0.15
    );

    let start = 0;
    let end = 0;
    let shouldMakeBlockRequest = false;
    if (direction == -1) {
      if (inTopZone && !atTop) {
        start = chainView[0].index - maxBlocksShown / 2;
        end = start + maxBlocksShown;
        shouldMakeBlockRequest = true;
        setInBottomZone(false);
      }
    } else {
      if (inBottomZone && !atBottom) {
        start = chainView[0].index + maxBlocksShown / 2;
        end = start + maxBlocksShown;
        shouldMakeBlockRequest = true;
        setInTopZone(false);
      }
    }
    if (shouldMakeBlockRequest) {
      start = start >= 0 ? start : 0;
      end = end < chainLength ? end : chainLength - 1;
      setChainViewRange({ start: start, end: end });
      setAtTop(start == 0);
      setAtBottom(end == chainLength - 1);
      setMakingBlockRequest(true);
    }
  };

  return (
    <>
      <div style={blockchainInspectionPanelStyle}>
        <div onWheel={onScroll} style={chainPanelStyle}>
          {chainArray.map(entry => {
            return entry;
          })}
        </div>
        {selectedBlock && <BlockInfoPanel block={selectedBlock}/>}
      </div>
    </>
  );
}

export { BlockchainInspectionPanel };
