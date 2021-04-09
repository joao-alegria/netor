import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { VsService } from "../../services/vsService/vs.service";
import { ModalserviceService } from '../../services/modalService/modalservice.service';
import { MessageService } from 'primeng/api';
import { ToastrService } from 'ngx-toastr';

declare var $: any;

@Component({
  selector: 'app-netslices',
  templateUrl: './netslices.component.html',
  styleUrls: ['./netslices.component.css'],
  providers: [MessageService]
})
export class NetslicesComponent implements OnInit {

  objectKeys = Object.keys;
  listData;
  headerList
  selectedElement
  tenant = true
  terminate = true

  constructor(private vs: VsService, private route: ActivatedRoute, private modal: ModalserviceService, private messageService: MessageService,private toastr: ToastrService) {
    vs.checkLoggedIn()
    if (localStorage.getItem("role") == "ADMIN") {
      this.tenant = false
    }
  }

  ngOnInit() {
    this.listData = [];
    this.update()
  }

  update() {
    this.listData=[]
    this.vs.getNetSlices().then(data => { this.listData = data })
  }

  onEnter(element) {
    $("#" + element).css("box-shadow", "4px 4px 10px grey")
  }

  onLeave(element) {
    $("#" + element).css("box-shadow", "none")
  }

  clickEvent(e, element) {
    e.stopPropagation()

    this.selectedElement = element;

    if (this.selectedElement.status == "OFFLINE") {
      this.terminate = false
    } else {
      this.terminate = true
    }

    if ($("#tooltip-span").css("display") == "block") {
      $("#tooltip-span").css("display", "none")
      return
    }

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
      if (y + 160 > window.screen.height) {
        y = y - 80
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

  modifyNS() {
    $("#tooltip-span").css("display", "none")
    this.modal.openModifyNsModal(this, this.selectedElement)
  }

  terminateNS() {
    $("#tooltip-span").css("display", "none")
    this.modal.openConfirmModal(this).afterClosed().subscribe(
      async (data) => {
        if (data == true) {
          await this.vs.terminateNS(this.selectedElement.nsiId).catch((message)=>{
            this.toastr.error(message.error,"Net. Slice Deletion Error", {positionClass: 'toast-bottom-center', closeButton: true})
          })
          this.mouseLeftTooltip()
          this.update()
        }
      });
  }

  instantiateNS() {
    $("#tooltip-span").css("display", "none")
    // this.modal.openConfirmModal(this).afterClosed().subscribe(
    //   async (data) => {
    //     if (data == true) {
    //       await this.vs.instantiateNS(this.selectedElement.nsiId)
    //       this.mouseLeftTooltip()
    //       this.update()
    //     }
    //   });
    this.modal.openInstantiateNsModal(this, this.selectedElement)
  }

  showToast(message) {
    if (message) {
      this.toastr.success("Success",message, {positionClass: 'toast-bottom-center', closeButton: true})
    }
  }
}
