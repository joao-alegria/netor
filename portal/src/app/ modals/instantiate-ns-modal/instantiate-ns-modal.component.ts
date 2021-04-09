import { Component, OnInit, Inject } from '@angular/core';
import { VsService } from '../../services/vsService/vs.service';
import { MessageService } from 'primeng/api';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ToastrService } from 'ngx-toastr';

declare var $: any;

@Component({
  selector: 'app-instantiate-ns-modal',
  templateUrl: './instantiate-ns-modal.component.html',
  styleUrls: ['./instantiate-ns-modal.component.css'],
  providers: [MessageService]
})
export class InstantiateNsModalComponent implements OnInit {

  objectKeys = Object.keys;
  tenant
  nsParams = [0]
  nsSubnetsId: string[];

  constructor(
    public dialogRef: MatDialogRef<InstantiateNsModalComponent>,
    @Inject(MAT_DIALOG_DATA) private modalData: any,
    private vs: VsService, private messageService: MessageService,
    private toastr: ToastrService
  ) {
    vs.checkLoggedIn()
    if (localStorage.getItem("role") == "TENANT") {
      this.tenant = localStorage.getItem("username")
    }
    console.log(modalData.nst)
  }

  ngOnInit() {
  }

  closeModal() {
    this.dialogRef.close();
  }

  submitNS() {
    let nsi = { userData: {}, locationConstraints: {} }

    let dfId = $("#dfId").val()
    let ilId = $("#ilId").val()
    let ran = $("#ranEndPointId").val()
    let altitude = $("#altitude").val()
    let latitude = $("#latitude").val()
    let longitude = $("#longitude").val()
    let range = $("#range").val()

    for (let paramNum of this.nsParams) {
      let param = $("#param" + paramNum).val()
      let value = $("#value" + paramNum).val()
      nsi.userData[param] = value
    }


    nsi["dfId"] = dfId
    nsi["ilId"] = ilId
    nsi["ranEndPointId"] = ran
    nsi["nstId"] = this.modalData.nst.nstId
    nsi["nsiId"] = this.modalData.nst.nsiId
    nsi["nsSubnetIds"] = this.nsSubnetsId
    nsi.locationConstraints["altitude"] = altitude
    nsi.locationConstraints["longitude"] = longitude
    nsi.locationConstraints["latitude"] = latitude
    nsi.locationConstraints["range"] = range

    this.vs.instantiateNS(this.modalData.nst.nsiId, nsi).then(()=>{
      this.dialogRef.close("Network Slice Instantiated")
    }).catch((message)=>{
      this.toastr.error(message.error,"Net Slice Instantiation Error", {positionClass: 'toast-bottom-center', closeButton: true})
    })
  }

  myStyle(i) {
    let styles = {
      'border-left': i != 0 ? 'solid 2px #007bff' : '',
      'border-radius': i != 0 ? '10px' : ''
    };

    return styles;
  }

  addParameter() {
    this.nsParams.push(this.nsParams[this.nsParams.length - 1] + 1)
  }

  removeParameter(j) {
    this.nsParams.splice(j, 1);
  }

}
