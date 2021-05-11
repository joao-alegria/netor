import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { VsService } from "../../services/vsService/vs.service";
import { ModalserviceService } from '../../services/modalService/modalservice.service';
import { MessageService } from 'primeng/api';
import { ToastrService } from 'ngx-toastr';

declare var $: any;

@Component({
  selector: 'app-nstemplates',
  templateUrl: './nstemplates.component.html',
  styleUrls: ['./nstemplates.component.css'],
  providers: [MessageService]
})
export class NstemplatesComponent implements OnInit {

  objectKeys = Object.keys;
  listData;
  selectedElement
  tenant = true

  constructor(private vs: VsService, private router: Router, private modal: ModalserviceService, private messageService: MessageService,private toastr: ToastrService) {
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
    this.vs.getNSTemplates().then(data => {
      this.listData = data["data"]
      console.log(this.listData)
      if (!this.tenant) {
        this.listData.unshift({ control: true, name: "Onboard NST", nst_id: "OnboardNST" })
      }
    })
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

  onboardNST(event) {
    event.stopPropagation()
    this.modal.openOnboardNstModal(this)
  }

  async deleteNst() {
    this.modal.openConfirmModal(this).afterClosed().subscribe(
      async (data) => {
        if (data == true) {
          await this.vs.deleteNST(this.selectedElement.nst_id).catch((message)=>{
            this.toastr.error(message.error,"Template Deletion Error", {positionClass: 'toast-bottom-center', closeButton: true})
          })
          this.mouseLeftTooltip()
          this.update()
        }
      })
  }

  instantiateNs() {
    this.modal.openCreateNsModal(this, this.selectedElement)
  }

  showToast(message) {
    if (message) {
      this.toastr.success("Success",message, {positionClass: 'toast-bottom-center', closeButton: true}).onTap.subscribe(()=> this.router.navigate(["/", "netslices"]));
    }
  }

}
