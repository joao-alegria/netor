import { Component, OnInit, Inject } from '@angular/core';
import { VsService } from '../../services/vsService/vs.service';
import { MessageService } from 'primeng/api';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import {COMMA, ENTER} from '@angular/cdk/keycodes';
import {MatChipInputEvent} from '@angular/material/chips';
import { ToastrService } from 'ngx-toastr';

declare var $: any;

@Component({
  selector: 'app-create-descriptor-modal',
  templateUrl: './create-descriptor-modal.component.html',
  styleUrls: ['./create-descriptor-modal.component.css'],
  providers: [MessageService]
})
export class CreateDescriptorModalComponent implements OnInit {
  objectKeys = Object.keys;

  preferredProviders: string[]=[];
  notPreferredProviders: string[]=[];
  prohibitedProviders: string[]=[];

  visible = true;
  selectable = true;
  removable = true;
  addOnBlur = true;
  readonly separatorKeysCodes: number[] = [ENTER, COMMA];


  addPreferred(event: MatChipInputEvent): void {
    const input = event.input;
    const value = event.value;

    // Add our fruit
    if ((value || '').trim()) {
      this.preferredProviders.push(value.trim());
    }

    // Reset the input value
    if (input) {
      input.value = '';
    }
  }

  removePreferred(layer): void {
    const index = this.preferredProviders.indexOf(layer);

    if (index >= 0) {
      this.preferredProviders.splice(index, 1);
    }
  }

  addNonPreferred(event: MatChipInputEvent): void {
    const input = event.input;
    const value = event.value;

    // Add our fruit
    if ((value || '').trim()) {
      this.notPreferredProviders.push(value.trim());
    }

    // Reset the input value
    if (input) {
      input.value = '';
    }
  }

  removeNonPreferred(layer): void {
    const index = this.notPreferredProviders.indexOf(layer);

    if (index >= 0) {
      this.notPreferredProviders.splice(index, 1);
    }
  }

  addProhibited(event: MatChipInputEvent): void {
    const input = event.input;
    const value = event.value;

    // Add our fruit
    if ((value || '').trim()) {
      this.prohibitedProviders.push(value.trim());
    }

    // Reset the input value
    if (input) {
      input.value = '';
    }
  }

  removeProhibited(layer): void {
    const index = this.prohibitedProviders.indexOf(layer);

    if (index >= 0) {
      this.prohibitedProviders.splice(index, 1);
    }
  }

  nsParams = [0]
  // parameterOptions = { "NONE": "none", "UE Speed": "uUSpeed", "Coverage": "coverage", "UserDensity": "userDensity", "ActivityFactor": "activityFactor", "Reliability": "reliability", "Survival Time": "survivalTime", "Payload Size": "payloadSize", "Connection Density": "connDensity" }

  constructor(
    public dialogRef: MatDialogRef<CreateDescriptorModalComponent>,
    @Inject(MAT_DIALOG_DATA) private modalData: any,
    private vs: VsService, private messageService: MessageService,
    private toastr: ToastrService
  ) {
    vs.checkLoggedIn()
    this.getNsdTopology()
  }

  async getNsdTopology(){
    console.log(this.modalData.blueprint)
    // await this.vs.getSpecificBlueprint(this.modalData.blueprint.vsBlueprintId).then((data)=>{
    //   console.log(data)
    // })
    await this.vs.getNSTemplates().then((data)=>{
      console.log(data)
    })
  }

  ngOnInit() {
  }

  closeModal() {
    this.dialogRef.close();
  }

  submitDescriptor() {
    let vsd = { vsd: { qosParameters: {}, serviceConstraints: [], sla: {}, sliceServiceParameters: {} }, tenantId: localStorage.getItem("username") }

    let name = $("#name").val()
    let version = $("#version").val()
    if(this.modalData.blueprint.vsBlueprint.parameters){
      for (let param of this.modalData.blueprint.vsBlueprint.parameters) {
        vsd.vsd.qosParameters[param.parameterId] = $("#" + param.parameterName).val()
      }
    }
    let sliceServiceType = $("#sliceServiceType").val()
    let manType = $("#manType").val()
    let isPublic = $("#isPublic").prop("checked")
    let priority = $("#priority").val()
    let isSharable = $("#isSharable").prop("checked")
    let includesSharedElems = $("#includesSharedElems").prop("checked")
    let serviceCreationTime = $("#serviceCreationTime").val()
    let coverageArea = $("#coverageArea").val()
    let isLowCost = $("#isLowCost").prop("checked")
    let sliceType = $("#sliceType").val().toLowerCase()

    vsd.vsd.sliceServiceParameters["type"] = sliceType
    let sliceParameters = {}

    for (let paramNum of this.nsParams) {
      let param = $("#parameter" + paramNum).val()
      let value = $("#value" + paramNum).val()
      if (param != "NONE") {
        sliceParameters[param] = value
      }
    }

    if (this.objectKeys(sliceParameters).length > 0) {
      for (let key in sliceParameters) {
        vsd.vsd.sliceServiceParameters[key] = sliceParameters[key]
      }
    }

    vsd["isPublic"] = isPublic
    vsd.vsd["vsBlueprintId"] = this.modalData.blueprint.vsBlueprintId.toString()
    vsd.vsd["name"] = name
    vsd.vsd["version"] = version
    vsd.vsd["sst"] = sliceServiceType
    vsd.vsd["managementType"] = manType
    vsd.vsd.serviceConstraints.push({ priority: priority, sharable: isSharable, canIncludeSharedElements: includesSharedElems, preferredProviders: this.preferredProviders, nonPreferredProviders: this.notPreferredProviders, prohibitedProviders: this.prohibitedProviders })
    vsd.vsd.sla["serviceCreationTime"] = serviceCreationTime == "NO REQUIREMENTS" ? "UNDEFINED" : serviceCreationTime
    vsd.vsd.sla["availabilityCoverage"] = coverageArea == "NO REQUIREMENTS" ? "UNDEFINED" : coverageArea
    vsd.vsd.sla["lowCostRequired"] = isLowCost

    this.vs.createNewDescriptor(vsd).then(()=>{this.dialogRef.close("Descriptor Created.");}).catch((message)=>{
      this.toastr.error(message.error,"Blueprint Deletion Error", {positionClass: 'toast-bottom-center', closeButton: true})
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
