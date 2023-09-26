module.exports = class Event {
    constructor(eventType, eventInfo, requestor) {
        this.eventType = eventType;
        this.eventInfo = eventInfo;
        this.requestor = requestor;
    }
}