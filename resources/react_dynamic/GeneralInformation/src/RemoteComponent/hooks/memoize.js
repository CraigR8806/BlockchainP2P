const memoize = func => {
    const cache = {};
    return key => {
      if (key in cache === false) {
        cache[key] = func(key);
      }
      return cache[key];
    };
  };
  
  export default memoize;