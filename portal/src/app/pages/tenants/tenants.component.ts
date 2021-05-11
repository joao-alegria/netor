import { Component, OnInit } from '@angular/core';
import { VsService } from "../../services/vsService/vs.service";
import { ModalserviceService } from '../../services/modalService/modalservice.service';
import { ToastrService } from 'ngx-toastr';

declare var $: any;

@Component({
  selector: 'app-tenants',
  templateUrl: './tenants.component.html',
  styleUrls: ['./tenants.component.css']
})
export class TenantsComponent implements OnInit {

  objectKeys = Object.keys;
  listData;
  selectedTenant
  selectedGroup

  constructor(private vs: VsService, private modal: ModalserviceService, private toastr: ToastrService) {
    vs.checkLoggedIn()
  }

  ngOnInit() {
    this.update()
  }

  newGroupBtnPressed(e) {
    e.stopPropagation()
    if ($("#newGroupForm").css("display") == "block") {
      $("#newGroupForm").css("display", "none")
      $("#groupName").val("")

    } else {
      $("#newGroupForm").css("display", "block")
    }
  }

  async newGroup(e) {
    e.stopPropagation()
    var data={name:$("#groupName").val()}
    await this.vs.createNewGroup(data).then(()=>{
      $("#newGroupForm").css("display", "none")
      $("#groupName").val("")
  
      this.update()
    }).catch((message)=>{
      this.toastr.error(message.error,"Create Group Error", {positionClass: 'toast-bottom-center', closeButton:true})
    })

  }

  update() {
    this.listData=[]
    this.listData.unshift({ control: true, title: "Create Group", name:"CreateGroup" })
    this.vs.getGroups().then(data => { this.listData = data["data"]; this.listData.unshift({ control: true, title: "Create Group", name:"CreateGroup" });console.log(this.listData) })
  }

  clickEvent(e, tenant, group) {
    e.stopPropagation()

    if ($("#tooltip-span").css("display") == "block") {
      $("#tooltip-span").css("display", "none")
      return
    }
    this.selectedTenant = tenant;
    this.selectedGroup = group;
    let tooltip = $("#tooltip-span");
    tooltip.css("display", "block")
    tooltip.css("position", "fixed")
    tooltip.css("overflow", "hidden")
    let x = e.clientX, y = e.clientY;
    if (this.selectedTenant == null) {
      if (y + 200 > window.screen.height) {
        y = y - 130
      }
    } else {
      if (y + 300 > window.screen.height) {
        y = y - 230
      }
    }
    tooltip.css("top", y - 10 + 'px');
    tooltip.css("left", x - 10 + 'px');
  }

  mouseLeftTooltip() {
    $("#tooltip-span").css("display", "none")
  }

  containerClick() {
    $("#tooltip-span").css("display", "none")
  }

  addTenant(event) {
    event.stopPropagation()
    this.modal.openNewTenantModal(this, this.selectedGroup)
  }

  async deleteGroup(event) {
    event.stopPropagation()
    this.modal.openConfirmModal(this).afterClosed().subscribe(
      async (data) => {
        if (data == true) {
          await this.vs.deleteGroup(this.selectedGroup).catch((message)=>{
            this.toastr.error(message.error,"Group Deletion Error", {positionClass: 'toast-bottom-center', closeButton: true})
          })
          this.update()
        }
      });

  }

  viewMoreInfo() {
    console.log(this.selectedGroup)
    console.log(this.selectedTenant)
    if (this.selectedTenant==null){
      for(let group of this.listData){
        if(group.name==this.selectedGroup){
          this.modal.openModal(this, group, this.selectedGroup)
          return
        }
      }
    }
    this.modal.openModal(this, this.selectedTenant, this.selectedGroup)
  }

  async deleteTenant() {
    this.modal.openConfirmModal(this).afterClosed().subscribe(
      async (data) => {
        if (data == true) {
          await this.vs.deleteGroupTenant(this.selectedGroup, this.selectedTenant.username).catch((message)=>{
            this.toastr.error(message.error,"Tenant Deletion Error", {positionClass: 'toast-bottom-center', closeButton: true})
          })
          this.mouseLeftTooltip()
          this.update()
        }
      });

  }

  viewSLA() {
    this.modal.openViewSlaModal(this, this.selectedGroup, this.selectedTenant)
    this.mouseLeftTooltip()
  }

  onEnter(element) {
    $("#" + element).css("box-shadow", "4px 4px 10px grey")
  }

  onLeave(element) {
    $("#" + element).css("box-shadow", "none")
  }
}
