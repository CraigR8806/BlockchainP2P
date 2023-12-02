import React from 'react';



function Block({block, onBlockSelect}) {


    const blockStyle = {
        width:"50%",
        minHeight:"15%",
        maxHeight:"15%",
        background:"cadetblue",
        color:"white",
        padding:"8px",
        display:"flex",
        flexDirection:"column",
        alignItems:"flex-start"
    }
    const hashStyle = {
        display:"flex",
        height:"100%",
        flexGrow:"1",
        alignItems:"center",
    }

    const onClick = () => {
        onBlockSelect(block);
    }
    

    const shortenedHash = block.hash.substring(0, 10) + "...";

    return (
        <>
            <div onClick={onClick} style={blockStyle}>
                {block.index}
                <div style={hashStyle}>
                    {shortenedHash}
                </div>
            </div>
        </>
    );
}

export { Block };