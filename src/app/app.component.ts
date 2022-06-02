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
  dataSource: Array<{ id: Number; name: String }> = [];

  constructor(private configService: ConfigService) {
    this.fetchSenders()
  }

  fetchSenders() {
    this.configService.getSenders().subscribe(res => {
      this.dataSource = res.data
    })
  }
}
