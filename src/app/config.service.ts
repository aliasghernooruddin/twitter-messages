import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ResponseModel } from './models';


@Injectable({
    providedIn: 'root'
})

export class ConfigService {
    constructor(private http: HttpClient,) { }

    getSenders() {
        return this.http.get<ResponseModel>('http://localhost:5000/');
    }
}