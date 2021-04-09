import { Component, OnInit, Inject } from '@angular/core';
import { VsService } from '../../services/vsService/vs.service';
import { MessageService } from 'primeng/api';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ToastrService } from 'ngx-toastr';

declare var $: any;

@Component({
  selector: 'app-create-ns-modal',
  templateUrl: './create-ns-modal.component.html',
  styleUrls: ['./create-ns-modal.component.css'],
  providers: [MessageService]
})
export class CreateNsModalComponent implements OnInit {

  constructor(
    public dialogRef: MatDialogRef<CreateNsModalComponent>,
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

  submitNS() {
    let ns = {}

    let name = $("#name").val()
    let description = $("#description").val()
    let nst = $("#nstId").val()



    ns["name"] = name
    ns["description"] = description
    ns["nstId"] = this.modalData.nst.nstId

    this.vs.createNewNS(ns).then(()=>{
      this.dialogRef.close("Network Slice Template Uploaded.")
    }).catch((message)=>{
      this.toastr.error(message.error,"Net Slice Creation Error", {positionClass: 'toast-bottom-center', closeButton: true})
    })
  }

}
