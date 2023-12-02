import React from 'react';
import { useState } from 'react';



function BlockchainBlockCreatePanel({peer}) {

    const hostport =
        "https://" +
        peer._Peer__connection._Connection__host +
        ":" +
        peer._Peer__connection._Connection__port;

    const [blockData, setBlockData] = useState("")

    function submitIt(){
        fetch(hostport + "/chain/new_block_data", {
            // mode:"cors",
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                block_data: blockData,
            })
        })
    }

    const submitBtnStyle = {
        background:"green",
        color:"white"
    }

    return (
        <>
            <input onChange={e => setBlockData(e.target.value)} />
            <div style={submitBtnStyle} onClick={submitIt}>Submit</div>
        </>
    );
}

export { BlockchainBlockCreatePanel };