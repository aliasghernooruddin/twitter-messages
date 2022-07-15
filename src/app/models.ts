export class SendersResponseModel {
    senders: Array<{ id: Number; name: String }>;
    status: Number;

    constructor(senders: Array<{ id: Number; name: String }>, status: Number) {
        this.senders = senders;
        this.status = status;
    }
}

export class OutReachResponseModel {
    outreach: Array<{ date: Date; handle: String, response: Boolean }>;
    status: Number;

    constructor(outreach: Array<{ date: Date; handle: String, response: Boolean }>, status: Number) {
        this.outreach = outreach
        this.status = status
    }
}