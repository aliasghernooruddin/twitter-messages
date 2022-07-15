import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { OutReachResponseModel, SendersResponseModel } from './models';


@Injectable({
    providedIn: 'root'
})

export class ConfigService {
    constructor(private http: HttpClient,) { }

    getSenders() {
        return this.http.get<SendersResponseModel>('http://localhost:5000/senders');
    }

    getOutreachResults(){
        return this.http.get<OutReachResponseModel>('http://localhost:5000/outreach');
    }
}