import { Component } from '@angular/core';
import { ConfigService } from './config.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {

  title = 'twitter-messages';
  displayedColumns: string[] = ['id', 'name'];
  displayedColumns1: string[] = ['handle', 'date', 'response'];
  dataSource: Array<{ id: Number; name: String }> = [];
  dataSource1: Array<{ date: Date; handle: String, response: Boolean }> = [];

  constructor(private configService: ConfigService) {
    this.fetchSenders()
    this.fetchOutreachResults()
  }

  fetchSenders() {
    this.configService.getSenders().subscribe(res => {
      this.dataSource = res.senders
    })
  }

  fetchOutreachResults() {
    this.configService.getOutreachResults().subscribe(res => {
      console.log(res.outreach)
      this.dataSource1 = res.outreach
    })
  }
}
