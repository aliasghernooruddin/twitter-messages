export class ResponseModel {
    data: Array<{ id: Number; name: String }>;
    status: Number;

    constructor(data: Array<{ id: Number; name: String }>, status: Number) {
        this.data = data;
        this.status = status;
    }
}