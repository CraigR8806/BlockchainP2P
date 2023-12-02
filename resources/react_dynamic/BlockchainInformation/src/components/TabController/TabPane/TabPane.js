import React from 'react';




function TabPane({Component, ...props}){
    const containerStyle = {
        display: "flex",
        flexDirection: "row",
        alignItems: "flex-start",
        backgroundColor: "darkcyan",
        flexGrow:"1",
        height:"100%",
        overflow:"scroll"
    }

    return (
        <>
            <div style={containerStyle}>
                <Component {...props}/>
            </div>
        </>
    );
}

export { TabPane };