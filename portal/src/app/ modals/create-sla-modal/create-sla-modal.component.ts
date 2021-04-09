import { Component, OnInit, Inject } from '@angular/core';
import { VsService } from '../../services/vsService/vs.service';
import { MessageService } from 'primeng/api';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ToastrService } from 'ngx-toastr';

declare var $: any;

@Component({
  selector: 'app-create-sla-modal',
  templateUrl: './create-sla-modal.component.html',
  styleUrls: ['./create-sla-modal.component.css'],
  providers: [MessageService]
})
export class CreateSlaModalComponent implements OnInit {

  constraints = [1]
  scope: string;
  showLocation = false

  constructor(
    public dialogRef: MatDialogRef<CreateSlaModalComponent>,
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

  async submitSLA() {
    let operationalState = $("#operationalState").val()

    let sla = { tenant: this.modalData.tenant.username, slaStatus: operationalState, slaConstraints: [] }
    for (let idx in this.constraints) {
      let scope = $("#scope").val()
      let vram = $("#vRAM" + this.constraints[idx]).val()
      let vCPU = $("#vCPU" + this.constraints[idx]).val()
      let vStorage = $("#vStorage" + this.constraints[idx]).val()

      if (scope == "MEC_RESOURCE") {
        sla.slaConstraints.push({ location: $("#location").val(), scope: scope, maxResourceLimit: { memoryRAM: vram, vCPU: vCPU, diskStorage: vStorage } });
      } else {
        sla.slaConstraints.push({ scope: scope, maxResourceLimit: { memoryRAM: vram, vCPU: vCPU, diskStorage: vStorage } });
      }

    }

    await this.vs.createSLA(this.modalData.group, this.modalData.tenant.username, sla).then(()=>{
      this.closeModal()
    }).catch((message)=>{
      this.toastr.error(message.error,"SLA Creation Error", {positionClass: 'toast-bottom-center', closeButton: true})
    })
  }

  addConstraint() {
    this.constraints.push(this.constraints.length)
  }

  onScopeChange() {
    if ($("#scope").val() == "MEC_RESOURCE") {
      this.showLocation = true
    } else {
      this.showLocation = false
    }
  }

  myStyle(i) {
    let styles = {
      'border-left': i != 0 ? 'solid 2px #007bff' : '',
      'border-radius': i != 0 ? '10px' : ''
    };

    return styles;
  }

  removeSla(i) {
    this.constraints.splice(i, 1);
  }
}
