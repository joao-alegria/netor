import { Component, OnInit, Inject } from '@angular/core';
import { VsService } from '../../services/vsService/vs.service';
import { MessageService } from 'primeng/api';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ToastrService } from 'ngx-toastr';

declare var $: any;


@Component({
  selector: 'app-new-tenant-modal',
  templateUrl: './new-tenant-modal.component.html',
  styleUrls: ['./new-tenant-modal.component.css'],
  providers: [MessageService]
})
export class NewTenantModalComponent implements OnInit {

  constructor(
    public dialogRef: MatDialogRef<NewTenantModalComponent>,
    @Inject(MAT_DIALOG_DATA) private modalData: any,
    private vs: VsService, private messageService: MessageService,
    private toastr: ToastrService
  ) {
    vs.checkLoggedIn()
  }

  ngOnInit() {
  }


  closeModal() {
    this.dialogRef.close();
  }

  passwordConfirmCheck(event) {
    if (event.key == "Enter") {
      this.submitTenant()
    } else {
      if ($("#inputPassword").val() != $("#inputPasswordConfirm").val() + event.key) {
        $("#inputPasswordConfirm").css("color", "red")
      } else {
        $("#inputPasswordConfirm").css("color", "green")
      }
    }
  }

  async submitTenant() {
    let username = $("#inputUsername").val()
    let password = $("#inputPassword").val()

    let remoteHost = $("#inputRemoteHost").val()
    let remoteUsername = $("#inputRemoteUsername").val()
    let remotePassword = $("#inputRemotePassword").val()
    if (password != $("#inputPasswordConfirm").val()) {
      this.messageService.add({ severity: 'warn', summary: 'Password confirmation must match with Password.' });
    } else {
      let tmp = []
      if ($("#typeTenant").val() == "REMOTE") {
        tmp.push({ host: remoteHost, remoteTenantName: remoteUsername, remoteTenantPwd: remotePassword })
      }

      await this.vs.createNewGroupTenant(this.modalData.group, { username: username, password: password, remoteTenantInfos: tmp }).then(()=>{
        this.closeModal()
      }).catch((message)=>{
        this.toastr.error(message.error,"Tenant Creation Error", {positionClass: 'toast-bottom-center', closeButton: true})
      })

    }
  }

  changeTypeTenant() {
    switch ($("#typeTenant").val()) {
      case "LOCAL":
        $("#remoteTenantType").css("display", "none")
        break
      case "REMOTE":
        $("#remoteTenantType").css("display", "block")
        break
    }
  }
}
