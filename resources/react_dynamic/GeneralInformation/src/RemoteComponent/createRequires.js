
  const sanitizeDependencies = dependencies =>
    typeof dependencies === "function" ? dependencies() : dependencies || {};
  
  export const createRequires = dependencies => {
    let isSanitized = false;
  
    return name => {
      if (!isSanitized) {
        // note: needs to happen inside the inner function for the laziness to work.
        dependencies = sanitizeDependencies(dependencies);
        isSanitized = true;
      }
  
      if (!(name in dependencies)) {
        throw new Error(
          `Could not require '${name}'. '${name}' does not exist in dependencies.`
        );
      }
  
      return dependencies[name];
    };
  };
  