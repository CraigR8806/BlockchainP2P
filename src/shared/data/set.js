class GeneralSet {

    constructor() {
        this.map = new Map();
        this[Symbol.iterator] = this.map.values;
    }

    add(item) {
        this.map.set(item.toIdString(), item);
    }

    values() {
        return this.map.values();
    }

    delete(item) {
        return this.map.delete(item.toIdString());
    }

}

class Settable {

    toIdString(){ throw new Error("Implement!"); }

}

module.exports.GeneralSet = GeneralSet;
module.exports.Settable = Settable;