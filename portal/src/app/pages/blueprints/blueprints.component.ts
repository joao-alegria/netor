import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { VsService } from "../../services/vsService/vs.service";
import { ModalserviceService } from '../../services/modalService/modalservice.service';
import { MessageService } from 'primeng/api';
import { ToastrService } from 'ngx-toastr';

declare var $: any;

@Component({
  selector: 'app-blueprints',
  templateUrl: './blueprints.component.html',
  styleUrls: ['./blueprints.component.css'],
  providers: [MessageService]
})
export class BlueprintsComponent implements OnInit {

  objectKeys = Object.keys;
  listData;
  selectedElement
  tenant = true

  constructor(private vs: VsService, private router: Router, private modal: ModalserviceService, private messageService: MessageService, private toastr: ToastrService) {
    this.vs.checkLoggedIn()
    if (localStorage.getItem("role") == "ADMIN") {
      this.tenant = false
    }
  }

  ngOnInit() {
    this.update()
  }

  update() {
    this.listData=[]
    if (!this.tenant) {
      this.listData.unshift({ control: true, name: "Onboard VSB" , vs_blueprint_id:"onboardVSB"})
    }
    this.vs.getBlueprints().then(data => {
      this.listData = data["data"]
      if (!this.tenant) {
        this.listData.unshift({ control: true, name: "Onboard VSB" , vs_blueprint_id:"onboardVSB"})
      }
      console.log(this.listData)
    })
  }


  onboardVSB(event) {
    event.stopPropagation()
    this.modal.openOnboardVsbModal(this)
  }

  onEnter(element) {
    $("#" + element).css("box-shadow", "4px 4px 10px grey")
  }

  onLeave(element) {
    $("#" + element).css("box-shadow", "none")
  }

  clickEvent(e, element) {
    e.stopPropagation()

    if ($("#tooltip-span").css("display") == "block") {
      $("#tooltip-span").css("display", "none")
      return
    }
    this.selectedElement = element;
    let tooltip = $("#tooltip-span");
    tooltip.css("display", "block")
    tooltip.css("position", "fixed")
    tooltip.css("overflow", "hidden")
    let x = e.clientX, y = e.clientY;
    if (!this.tenant) {
      if (y + 160 > window.screen.height) {
        y = y - 80
      }
    } else {
      if (y + 110 > window.screen.height) {
        y = y - 30
      }
    }
    tooltip.css("top", y - 10 + 'px');
    tooltip.css("left", x - 10 + 'px');
  }

  mouseLeftTooltip() {
    $("#tooltip-span").css("display", "none")
  }

  viewMoreInfo() {
    $("#tooltip-span").css("display", "none")
    this.modal.openModal(this, this.selectedElement, null)
  }

  containerClick() {
    $("#tooltip-span").css("display", "none")
  }

  createDescriptor() {
    this.modal.openCreateDescriptorModal(this, this.selectedElement)
    this.mouseLeftTooltip()
  }

  async deleteBlueprint() {
    this.modal.openConfirmModal(this).afterClosed().subscribe(
      async (data) => {
        if (data == true) {
          await this.vs.deleteVSB(this.selectedElement.vs_blueprint_id).catch((message)=>{
            this.toastr.error(message.error,"Blueprint Deletion Error", {positionClass: 'toast-bottom-center', closeButton: true})
          })
          this.mouseLeftTooltip()
          this.update()
        }
      });
  }

  showToast(message) {
    if (message) {
      this.toastr.success("Success",message, {positionClass: 'toast-bottom-center', closeButton: true}).onTap.subscribe(()=> this.router.navigate(["/", "descriptors"]));
    }
  }

}
