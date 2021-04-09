import { Component, OnInit, Inject } from '@angular/core';
import { VsService } from '../../services/vsService/vs.service';
import { MessageService } from 'primeng/api';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import {COMMA, ENTER} from '@angular/cdk/keycodes';
import {MatChipInputEvent} from '@angular/material/chips';
import { ToastrService } from 'ngx-toastr';

declare var $: any;

@Component({
  selector: 'app-onboard-domain-modal',
  templateUrl: './onboard-domain-modal.component.html',
  styleUrls: ['./onboard-domain-modal.component.css'],
  providers: [MessageService]
})
export class OnboardDomainModalComponent implements OnInit {

  

  layersAgreeList:string[]=[];
  ownedLayers=[0]
  visible = true;
  selectable = true;
  removable = true;
  addOnBlur = true;
  readonly separatorKeysCodes: number[] = [ENTER, COMMA];


  add(event: MatChipInputEvent): void {
    const input = event.input;
    const value = event.value;

    console.log(input)
    console.log(value)

    // Add our fruit
    if ((value || '').trim()) {
      this.layersAgreeList.push(value.trim());
    }

    console.log()

    // Reset the input value
    if (input) {
      input.value = '';
    }
  }

  remove(layer): void {
    const index = this.layersAgreeList.indexOf(layer);

    if (index >= 0) {
      this.layersAgreeList.splice(index, 1);
    }
  }

  constructor(
    public dialogRef: MatDialogRef<OnboardDomainModalComponent>,
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

  async onboardDomain() {
    let domainId = $("#domainId").val()
    let domainName = $("#domainName").val()
    let domainDescription = $("#domainDescription").val()
    let domainAdmin = $("#domainAdmin").val()
    let domainStatus = $("#domainStatus").val()

    let domainInterUrl = $("#domainInterUrl").val()
    let domainInterPort = parseInt($("#domainInterPort").val())
    let domainInterAuth = $("#domainInterAuth").prop("checked")
    let domainInterType = $("#domainInterType").val()

    let domainAgreeId= $("#domainAgreeId").val()


    let request={domainId:domainId, name:domainName, description:domainDescription, owner: localStorage.username, admin:domainAdmin, domainStatus:domainStatus, domainInterface:{url:domainInterUrl, port:domainInterPort, auth:domainInterAuth, interfaceType:domainInterType}, ownedLayers:[]}

    for (let layer of this.ownedLayers){
      let domainLayerId=$("#domainLayerId"+layer).val()
      let domainLayerType=$("#domainLayerType"+layer).val()
      let domainLayerDriverType=$("#domainLayerDriverType"+layer).val()
      let data={domainLayerId:domainLayerId, domainLayerType:domainLayerType,type:domainLayerDriverType}

      switch(domainLayerDriverType){
        case "NFVO":
          data["manoNbiType"]=$("#domainLayerManoNbiType"+layer).val()
          break
        case "NSP":
          data["nspNbiType"]=$("#domainLayerNspNbiType"+layer).val()
          data["ranEnabled"]=$("#domainLayerRanEnabled"+layer).val()
          break
        case "VERTICAL":
          data["dspType"]=$("#domainLayerDspType"+layer).val()
          break
        case "OSM_NFVO":
          data["username"]=$("#domainLayerOsmNfvoUsername"+layer).val()
          data["password"]=$("#domainLayerOsmNfvoPassword"+layer).val()
          data["project"]=$("#domainLayerOsmNfvoProject"+layer).val()
          break
        case "NEUTRAL_HOSTING_NSP":
          data["userId"]=$("#domainLayerNeutralNspUser"+layer).val()
          data["tenantId"]=$("#domainLayerNeutralNspTenant"+layer).val()
          break
        case "OSM_NSP":
          data["project"]=$("#domainLayerOsmNspUsername"+layer).val()
          data["project"]=$("#domainLayerOsmNspPassword"+layer).val()
          data["project"]=$("#domainLayerOsmNspProject"+layer).val()
          data["project"]=$("#domainLayerOsmNspVim"+layer).val()
          break
        case "SONATA_NSP":
          data["username"]=$("#domainLayerSonataNspUsername"+layer).val()
          data["password"]=$("#domainLayerSonataNspPassword"+layer).val()
          break
        case "EVE_PORTAL_DSP":
          data["rbacUrl"]=$("#domainLayerEveRbacUrl"+layer).val()
          data["catalogueUrl"]=$("#domainLayerEveCatalogueUrl"+layer).val()
          data["elcmUrl"]=$("#domainLayerEveElcmUrl"+layer).val()
          data["username"]=$("#domainLayerEveUsername"+layer).val()
          data["password"]=$("#domainLayerEvePassword"+layer).val()
          break
      }

      request.ownedLayers.push(data)
    }

    await this.vs.createNewDomain(request).then(()=>{
      this.dialogRef.close("Domain Created.");
    }).catch((message)=>{
      this.toastr.error(message.error,"Domain Creation Error", {positionClass: 'toast-bottom-center', closeButton:true})
    })
  }

  myStyle(i) {
    let styles = {
      'border-left': i != 0 ? 'solid 2px #007bff' : '',
      'border-radius': i != 0 ? '10px' : ''
    };

    return styles;
  }

  addLayer() {
    this.ownedLayers.push(this.ownedLayers[this.ownedLayers.length - 1] + 1)
  }

  removeLayer(i) {
    this.ownedLayers.splice(i, 1);
  }

  driverTypeChange(event, i){
    switch(event.target.value){
      case "NFVO":
        $("#nfvo"+i).css("display", "block")
        for (let option of ['nsp','vertical','osmNfvo','nhpNsp','osmNsp','sonataNsp', 'eve']){
          $("#"+option+i).css("display", "none")
        }
        break
      case "NSP":
        $("#nsp"+i).css("display", "block")
        for (let option of ['nfvo','vertical','osmNfvo','nhpNsp','osmNsp','sonataNsp', 'eve']){
          $("#"+option+i).css("display", "none")
        }
        break
      case "VERTICAL":
        $("#vertical"+i).css("display", "block")
        for (let option of ['nsp','nfvo','osmNfvo','nhpNsp','osmNsp','sonataNsp', 'eve']){
          $("#"+option+i).css("display", "none")
        }
        break
      case "OSM_NFVO":
        $("#osmNfvo"+i).css("display", "block")
        for (let option of ['nsp','nfvo','vertical','nhpNsp','osmNsp','sonataNsp', 'eve']){
          $("#"+option+i).css("display", "none")
        }
        break
      case "NEUTRAL_HOSTING_NSP":
        $("#nhpNsp"+i).css("display", "block")
        for (let option of ['nsp','nfvo','osmNfvo','verical','osmNsp','sonataNsp', 'eve']){
          $("#"+option+i).css("display", "none")
        }
        break
      case "OSM_NSP":
        $("#osmNsp"+i).css("display", "block")
        for (let option of ['nsp','nfvo','osmNfvo','nhpNsp','vertical','sonataNsp', 'eve']){
          $("#"+option+i).css("display", "none")
        }
        break
      case "SONATA_NSP":
        $("#sonataNsp"+i).css("display", "block")
        for (let option of ['nsp','nfvo','osmNfvo','nhpNsp','osmNsp','vertical', 'eve']){
          $("#"+option+i).css("display", "none")
        }
        break
      case "EVE_PORTAL_DSP":
        $("#eve"+i).css("display", "block")
        for (let option of ['nsp','nfvo','osmNfvo','nhpNsp','osmNsp','sonataNsp', 'vertical']){
          $("#"+option+i).css("display", "none")
        }
        break
    }
  }

  checkNumber(event) {
    if ((event.keyCode > 47 && event.keyCode< 58) || event.keyCode==9|| event.keyCode==8 ) {}
    else{
      return false
    }
  }

}
