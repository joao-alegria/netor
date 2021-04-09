import { Component, OnInit, Inject } from '@angular/core';
import { VsService } from '../../services/vsService/vs.service';
import { MessageService } from 'primeng/api';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ToastrService } from 'ngx-toastr';

declare var $: any;

@Component({
  selector: 'app-modify-nsmodal',
  templateUrl: './modify-nsmodal.component.html',
  styleUrls: ['./modify-nsmodal.component.css'],
  providers: [MessageService]
})
export class ModifyNSModalComponent implements OnInit {

  constructor(
    public dialogRef: MatDialogRef<ModifyNSModalComponent>,
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

  async submitNSModification() {
    let dfid = $("#dfId").val()
    let ilid = $("#ilId").val()
    let nsiid = $("#nsiId").val()
    let nstid = $("#nstId").val()
    let vsiid = $("#vsiId").val()
    let data = { dfId: dfid, ilId: ilid, nsiId: nsiid, nstId: nstid, vsiId: vsiid }
    await this.vs.modifyNS(this.modalData.nsi.nsiId, data).then(()=>{
      this.closeModal()
    }).catch((message)=>{
      this.toastr.error(message.error,"Net Slice Modification Error", {positionClass: 'toast-bottom-center', closeButton: true})
    })
  }
}
