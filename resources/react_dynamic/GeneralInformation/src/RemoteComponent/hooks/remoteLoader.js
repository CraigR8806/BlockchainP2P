import memoize from "./memoize";
import { useState, useEffect } from 'react';



const defaultRequires = name => {
  throw new Error(
    `Could not require '${name}'. The 'requires' function was not provided.`
  );
};
const createLoadRemoteModule = (requires) => {
    const _requires = requires.requires || defaultRequires;

    return memoize(url =>
        fetch(url)
            .then(res => {
                return res.text();
            })
            .then(data => {
        const exports = {};
        const module = { exports };
        // eslint-disable-next-line no-new-func, no-useless-escape
        const func = new Function("require", "module", "exports", data);//'!function(t,e){for(var n in e)t[n]=e[n]}(exports,function(t){var e={};function n(r){if(e[r])return e[r].exports;var o=e[r]={i:r,l:!1,exports:{}};return t[r].call(o.exports,o,o.exports,n),o.l=!0,o.exports}return n.m=t,n.c=e,n.d=function(t,e,r){n.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:r})},n.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},n.t=function(t,e){if(1&e&&(t=n(t)),8&e)return t;if(4&e&&"object"==typeof t&&t&&t.__esModule)return t;var r=Object.create(null);if(n.r(r),Object.defineProperty(r,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var o in t)n.d(r,o,function(e){return t[e]}.bind(null,o));return r},n.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return n.d(e,"a",e),e},n.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},n.p="",n(n.s=11)}([function(t,e){t.exports=require("react")},function(t,e){t.exports=function(t){return"object"==typeof t?null!==t:"function"==typeof t}},function(t,e,n){t.exports=!n(3)((function(){return 7!=Object.defineProperty({},"a",{get:function(){return 7}}).a}))},function(t,e){t.exports=function(t){try{return!!t()}catch(t){return!0}}},function(t,e,n){var r=n(5).f,o=Function.prototype,u=/^\s*function ([^ (]*)/;"name"in o||n(2)&&r(o,"name",{configurable:!0,get:function(){try{return(""+this).match(u)[1]}catch(t){return""}}})},function(t,e,n){var r=n(6),o=n(7),u=n(10),i=Object.defineProperty;e.f=n(2)?Object.defineProperty:function(t,e,n){if(r(t),e=u(e,!0),r(n),o)try{return i(t,e,n)}catch(t){}if("get"in n||"set"in n)throw TypeError("Accessors not supported!");return"value"in n&&(t[e]=n.value),t}},function(t,e,n){var r=n(1);t.exports=function(t){if(!r(t))throw TypeError(t+" is not an object!");return t}},function(t,e,n){t.exports=!n(2)&&!n(3)((function(){return 7!=Object.defineProperty(n(8)("div"),"a",{get:function(){return 7}}).a}))},function(t,e,n){var r=n(1),o=n(9).document,u=r(o)&&r(o.createElement);t.exports=function(t){return u?o.createElement(t):{}}},function(t,e){var n=t.exports="undefined"!=typeof window&&window.Math==Math?window:"undefined"!=typeof self&&self.Math==Math?self:Function("return this")();"number"==typeof __g&&(__g=n)},function(t,e,n){var r=n(1);t.exports=function(t,e){if(!r(t))return t;var n,o;if(e&&"function"==typeof(n=t.toString)&&!r(o=n.call(t)))return o;if("function"==typeof(n=t.valueOf)&&!r(o=n.call(t)))return o;if(!e&&"function"==typeof(n=t.toString)&&!r(o=n.call(t)))return o;throw TypeError("Can\'t convert object to primitive value")}},function(t,e,n){"use strict";n.r(e);n(4);var r=n(0),o=n.n(r),u=function(t){var e=t.children;return o.a.createElement("h1",null,e)};e.default=function(t){var e=t.name,n=void 0===e?"World":e;return o.a.createElement(u,null,"Hello ",n,"!")}}]));');
        func(_requires, module, exports);
        return module.exports;
        })
    );


}

export const createUseRemoteComponent = (args)=> {
    const loadRemoteModule = createLoadRemoteModule(args);
  
    const useRemoteComponent = (
      url,
      imports = "default"
    ) => {
      const [{ loading, err, component }, setState] = useState({
        loading: true,
        err: undefined,
        component: undefined
      });
  
      useEffect(() => {
        let update = setState;
  
        update({ loading: true, err: undefined, component: undefined });
  
        loadRemoteModule(url)
          .then(module =>
            update({ loading: false, err: undefined, component: module[imports] })
          )
          .catch(err => update({ loading: false, err, component: undefined }));
  
        return () => {
          // invalidate update function for stale closures
          update = () => {
            // this function is left intentionally blank
          };
        };
      }, [url, imports]);
  
      return [loading, err, component];
    };
  
    return useRemoteComponent;
  };



export const createRemoteComponent = (props = {}) => {

    const usRemoteComponent = createUseRemoteComponent(props);
    
    const remoteComponent = function ({
      url,
      fallback = null,
      render,
      ...props
    }) {
        const [loading, err, Component] = usRemoteComponent(url);

        if (loading) {
          return fallback;
        }
    
        if (render) {
          return render({ err, Component });
        }
    
        if (err || !Component) {
          return <div>Unknown Error: {(err || "UNKNOWN").toString()}</div>;
        }
    
        return <Component {...props} />;
      };
    
      return remoteComponent;
  };
