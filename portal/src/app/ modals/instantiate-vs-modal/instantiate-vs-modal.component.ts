import { Component, OnInit, Inject } from '@angular/core';
import { VsService } from '../../services/vsService/vs.service';
import { MessageService } from 'primeng/api';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ToastrService } from 'ngx-toastr';

declare var $: any;



@Component({
  selector: 'app-instantiate-vs-modal',
  templateUrl: './instantiate-vs-modal.component.html',
  styleUrls: ['./instantiate-vs-modal.component.css'],
  providers: [MessageService]
})
export class InstantiateVsModalComponent implements OnInit {

  objectKeys = Object.keys;
  domainPlacements = [0]
  parameterOptions = { "NONE": "none", "UE Speed": "uUSpeed", "Coverage": "coverage", "UserDensity": "userDensity", "ActivityFactor": "activityFactor", "Reliability": "reliability", "Survival Time": "survivalTime", "Payload Size": "payloadSize", "Connection Density": "connDensity" }
  tenant
  coords
  vnfs=[1]

  constructor(
    public dialogRef: MatDialogRef<InstantiateVsModalComponent>,
    @Inject(MAT_DIALOG_DATA) private modalData: any,
    private vs: VsService, private messageService: MessageService,
    private toastr: ToastrService
  ) {
    vs.checkLoggedIn()
    // if (localStorage.getItem("role") == "TENANT") {
    this.tenant = localStorage.getItem("username")
    // }
    this.modalData={"descriptor":{"name":"test","vsDescriptorId":"1"}}
    console.log(modalData)
  }

  ngOnInit() {
  }

  closeModal() {
    this.dialogRef.close();
  }


  submitVS() {
    let vsi = { }

    let name = $("#name").val()
    let tenant = $("#tenant").val()
    let description = $("#description").val()
    let url = $("#notificationUrl").val()
    let altitude = $("#altitude").val()
    let latitude = $("#latitude").val()
    let longitude = $("#longitude").val()
    let range = $("#range").val()


    // let sliceParameters = {}

    // for (let paramNum of this.nsParams) {
    //   let param = $("#parameter" + paramNum).val()
    //   let value = $("#value" + paramNum).val()
    //   if (param != "NONE") {
    //     sliceParameters[this.parameterOptions[param]] = value
    //   }
    // }

    // if (this.objectKeys(sliceParameters).length > 0) {
    //   vsi.userData["slice_parameters"] = sliceParameters
    // }


    vsi["name"] = name
    vsi["tenantId"] = tenant
    vsi["description"] = description
    vsi["vsdId"] = this.modalData.descriptor.vsDescriptorId.toString()
    // vsi.locationConstraints["altitude"] = altitude
    // vsi.locationConstraints["longitude"] = longitude
    // vsi.locationConstraints["latitude"] = latitude
    // vsi.locationConstraints["range"] = range

    console.log(vsi)

    this.vs.instantiateNewVS(vsi).catch((message)=>{
      this.toastr.error(message.error,"Vertical Slice Instantiation Error", {positionClass: 'toast-bottom-center', closeButton: true})
    })
    this.dialogRef.close("Vertical Slice Instantiated")
  }


  myStyle(i) {
    let styles = {
      'border-left': i != 0 ? 'solid 2px #007bff' : '',
      'border-radius': i != 0 ? '10px' : ''
    };

    return styles;
  }

  addPlacement() {
    this.domainPlacements.push(this.domainPlacements[this.domainPlacements.length - 1] + 1)
  }

  removePlacement(j) {
    this.domainPlacements.splice(j, 1);
  }

  onConfirm(coords) {
    $("#latitude").val(coords[0])
    $("#longitude").val(coords[1])
  }

  checkLocation() {
    let lat = $("#latitude").val()
    let long = $("#longitude").val()
    if (lat != "" && long != "") {
      this.coords = [parseFloat(lat), parseFloat(long)]
    }
  }

}
