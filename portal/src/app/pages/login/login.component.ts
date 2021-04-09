import { Component, OnInit } from '@angular/core';
import { VsService } from "../../services/vsService/vs.service";
import { Router } from '@angular/router';
import * as $ from 'jquery';
import { MessageService } from 'primeng/api';
import { ToastrService } from 'ngx-toastr';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
  providers: [MessageService]
})
export class LoginComponent implements OnInit {

  htmlContent: string = "";

  constructor(private vs: VsService, private router: Router, private messageService: MessageService,private toastr: ToastrService) { };

  ngOnInit() { }

  async login() {
    await this.vs.login($("#inputUsername").val().trim(), $("#inputPassword").val().trim())
      .then(data => {
        localStorage.setItem("accessToken",data.body["access_token"])
        this.vs.whoami().then(data => {
          console.log(data)

          localStorage.setItem("username", data["username"])
          localStorage.setItem("role", data["role"])
          localStorage.setItem("isLogged", "true")
          if (localStorage.getItem("role") == "ADMIN") {
            $("#adminNav").show()
            $("#tenantNav").hide()
          } else {
            $("#adminNav").hide()
            $("#tenantNav").show()
          }
          $("#myNav").show()
          this.router.navigate(["/home"])
        }).catch(data => {
          localStorage.setItem("isLogged", "false")
        }).catch(error => {
          console.log(error)
        })
      })
      .catch(data => {
        if (data.status == 401) {
          this.toastr.error("Username/Password may be incorrect.","Login Error", {positionClass: 'toast-bottom-center', closeButton:true})
        }
        else if (data.status == 0) {
          this.toastr.error("Try later. Something went wrong.","Login Error", {positionClass: 'toast-bottom-center', closeButton:true})
        }
      })

  }


}
