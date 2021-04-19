import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { VsService } from "../../services/vsService/vs.service";
import { ModalserviceService } from '../../services/modalService/modalservice.service';
import { MessageService } from 'primeng/api';
import { ToastrService } from 'ngx-toastr';

declare var $: any;

@Component({
  selector: 'app-domains',
  templateUrl: './domains.component.html',
  styleUrls: ['./domains.component.css'],
  providers: [MessageService]
})
export class DomainsComponent implements OnInit {

  objectKeys = Object.keys;
  listData;
  selectedElement
  tenant = true

  constructor(private vs: VsService, private router: Router, private modal: ModalserviceService, private messageService: MessageService, private toastr: ToastrService) {
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
    this.vs.getAllDomains().then(data => {
      console.log(data)
      this.listData = data["data"]
      if (!this.tenant) {
        this.listData.unshift({ control: true, name: "Onboard Domain", domainId: "OnboardDomain" })
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

  onboardDomain(event) {
    event.stopPropagation()
    this.modal.openOnboardDomainModal(this, this.selectedElement)
  }

  async deleteDomain() {
    this.modal.openConfirmModal(this).afterClosed().subscribe(
      async (data) => {
        if (data == true) {
          console.log(this.selectedElement.domainId)
          await this.vs.deleteDomain(this.selectedElement.domainId).catch((message)=>{
            this.toastr.error(message.error,"Domain Deletion Error", {positionClass: 'toast-bottom-center', closeButton:true})
          })
          this.mouseLeftTooltip()
          this.update()
        }
      })
  }

}
