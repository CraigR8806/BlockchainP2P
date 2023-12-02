/**
 * Entrypoint of the Remote Component.
 */
import { App } from "./App";
import React from 'react';

function AppLocal({}){

    const style = {
        display:"flex",
        width:"1330px",
        height:"805px",
        border:"3px",
        backgroundColor:"#4d5565",
        borderColor:"darkcyan",
        color:"darkgrey",
        borderStyle:"solid",
        margin:"10px",
        padding:"10px"
    }

    const backgroundStyle = {
        width:"100vw",
        height:"100vh",
        display:"flex",
        flexDirection:"row-reverse",
        alignItems:"flex-end",
        backgroundColor:"#282c34",

    }
    HTMLElement.prototype.stopScroll = function(){
        this.scroll({top:this.scrollTop+1});
    }

    document.getElementsByTagName("body")[0].style = "margin:0px";
    document.getElementsByTagName('body')[0].stopScroll();

    return (
        <div style={backgroundStyle}>
            <div style={style}>
                <App></App>
            </div>
        </div>
    )
}

export default AppLocal;
