import { Component, NgZone } from '@angular/core';
import { VsService } from "./services/vsService/vs.service";
import { Router } from '@angular/router';
import * as $ from 'jquery';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  title = 'portal';

  constructor(private vs: VsService, private router: Router, private ngZone: NgZone) {
    // this.vs.whoami().then(data => { localStorage.setItem("role", data["role"]); localStorage.setItem("isLogged", "true"); $("#myNav").show(); this.router.navigate(["/home"]) }).catch(error => { $("#myNav").hide(); this.router.navigate(["/login"]) })
    this.vs.checkLoggedIn()
  }

  logout() {
    localStorage.setItem("isLogged", "false")
    $("#myNav").hide()
    this.router.navigate(["/", "login"])
  }

}
