import { Component, OnInit, Inject } from '@angular/core';
import { VsService } from '../../services/vsService/vs.service';
import { MessageService } from 'primeng/api';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ToastrService } from 'ngx-toastr';


declare var $: any;

@Component({
  selector: 'app-scale-vs-modal',
  templateUrl: './scale-vs-modal.component.html',
  styleUrls: ['./scale-vs-modal.component.css'],
  providers: [MessageService]
})
export class ScaleVsModalComponent implements OnInit {

  validVSD = []

  constructor(
    public dialogRef: MatDialogRef<ScaleVsModalComponent>,
    @Inject(MAT_DIALOG_DATA) private modalData: any,
    private vs: VsService, private messageService: MessageService,
    private toastr: ToastrService
  ) {
    vs.checkLoggedIn()
    this.getValidVSD()
  }

  ngOnInit() {
  }

  closeModal() {
    this.dialogRef.close();
  }

  getValidVSD() {
    this.vs.getDescriptors().then((data) => {
      for (let vsdIdx in data) {
        if (data[vsdIdx].vsDescriptorId != this.modalData.vsi.vsdId) {
          this.validVSD.push({ name: data[vsdIdx].name, vsdId: data[vsdIdx].vsDescriptorId })
        }
      }
    })
  }

  updateVS() {
    let updateValues = { tenantId: localStorage.getItem("username"), vsiId: this.modalData.vsi.vsiId }

    let vsd = $("#chosenVSD").val()
    let processedText = vsd.split(":")
    let vsdId = processedText[processedText.length - 1].substring(1, 2)

    updateValues["vsdId"] = vsdId

    this.vs.scaleVSI(this.modalData.vsi.vsiId, updateValues).then(()=>{
      this.closeModal()
    }).catch((message)=>{
      this.toastr.error(message.error,"Vertical Slice Scaling Error", {positionClass: 'toast-bottom-center', closeButton: true})
    })

  }

}
