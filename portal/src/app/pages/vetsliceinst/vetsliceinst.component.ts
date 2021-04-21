import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { VsService } from "../../services/vsService/vs.service";
import { ModalserviceService } from '../../services/modalService/modalservice.service';
import { ToastrService } from 'ngx-toastr';

declare var $: any;

@Component({
  selector: 'app-vetsliceinst',
  templateUrl: './vetsliceinst.component.html',
  styleUrls: ['./vetsliceinst.component.css']
})
export class VetsliceinstComponent implements OnInit {

  objectKeys = Object.keys;
  listData;
  headerList
  selectedElement
  tenant = true

  constructor(private vs: VsService, private route: ActivatedRoute, private modal: ModalserviceService,private toastr: ToastrService) {
    vs.checkLoggedIn()
    if (localStorage.getItem("role") == "ADMIN") {
      this.tenant = false
    }
  }


  ngOnInit() {
    this.update()
  }

  update() {
    this.listData=[]
    this.vs.getVerticalSlices().then(data => { this.listData = data["data"] })
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
      if (y + 120 > window.screen.height) {
        y = y - 30
      }
    } else {
      if (y + 210 > window.screen.height) {
        y = y - 130
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

  async terminateVs() {
    this.modal.openConfirmModal(this).afterClosed().subscribe(
      async (data) => {
        if (data == true) {
          await this.vs.terminateVSI(this.selectedElement.vsiId).catch((message)=>{
            this.toastr.error(message.error,"Vertical SLice Termination Error", {positionClass: 'toast-bottom-center', closeButton: true})
          })
          this.mouseLeftTooltip()
          this.update()
        }
      })
  }


  async removeVs() {
    this.modal.openConfirmModal(this).afterClosed().subscribe(
      async (data) => {
        if (data == true) {
          await this.vs.deleteVSI(this.selectedElement.vsiId).catch((message)=>{
            this.toastr.error(message.error,"Vertical SLice Deletion Error", {positionClass: 'toast-bottom-center', closeButton: true})
          })
          this.mouseLeftTooltip()
          this.update()
        }
      })
  }

  scaleVs() {
    this.modal.openScaleVSModal(this, this.selectedElement);
    this.mouseLeftTooltip()
  }
}
