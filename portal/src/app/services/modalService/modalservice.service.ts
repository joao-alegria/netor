import { Injectable } from '@angular/core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { MainModalComponent } from '../../ modals/main-modal/main-modal.component';
import { VsService } from '../vsService/vs.service';
import { NewTenantModalComponent } from '../../ modals/new-tenant-modal/new-tenant-modal.component';
import { OnboardVsbModalComponent } from '../../ modals/onboard-vsb-modal/onboard-vsb-modal.component';
import { OnboardNstModalComponent } from '../../ modals/onboard-nst-modal/onboard-nst-modal.component';
import { CreateDescriptorModalComponent } from '../../ modals/create-descriptor-modal/create-descriptor-modal.component';
import { InstantiateVsModalComponent } from '../../ modals/instantiate-vs-modal/instantiate-vs-modal.component';
import { ScaleVsModalComponent } from '../../ modals/scale-vs-modal/scale-vs-modal.component';
import { CreateSlaModalComponent } from '../../ modals/create-sla-modal/create-sla-modal.component';
import { ViewSlaModalComponent } from '../../ modals/view-sla-modal/view-sla-modal.component';
import { CreateNsModalComponent } from '../../ modals/create-ns-modal/create-ns-modal.component';
import { ConfirmModalComponent } from '../../ modals/confirm-modal/confirm-modal.component';
import { ModifyNSModalComponent } from '../../ modals/modify-nsmodal/modify-nsmodal.component';
import { InstantiateNsModalComponent } from '../../ modals/instantiate-ns-modal/instantiate-ns-modal.component';
import { OnboardDomainModalComponent } from '../../ modals/onboard-domain-modal/onboard-domain-modal.component';

declare var $: any;


@Injectable({
  providedIn: 'root'
})
export class ModalserviceService {


  constructor(private matDialog: MatDialog, private vs: VsService) { }

  /**
   * Used to identify the class that asked for the modal and add the corresponding buttons and show the modal
   * @param elementRef 
   * @param data 
   */
  openModal(elementRef, data, group) {
    let title = ""
    switch (elementRef.constructor.name) {
      case "NstemplatesComponent":
        title = data.nst.nstName
        break
      case "TenantsComponent":
        if(data.name){
          title=data.name
        }else{
          title = data.username + " - Group: "+group
        }
        break
      default:
        title = data.name
        break

    }

    const dialogConfig = new MatDialogConfig();
    // The user can't close the dialog by clicking outside its body
    dialogConfig.id = "modal-component";
    dialogConfig.height = "80%";
    dialogConfig.width = "80%";
    dialogConfig.data = {
      title: title,
      data: data,
      group: group
    }
    // https://material.angular.io/components/dialog/overview
    const modalDialog = this.matDialog.open(MainModalComponent, dialogConfig);
    modalDialog.afterClosed().toPromise().then(() => {
      elementRef.update()
    })
  }

  openNewTenantModal(elementRef, group) {

    const dialogConfig = new MatDialogConfig();
    // The user can't close the dialog by clicking outside its body
    dialogConfig.id = "new-tenant-modal-component";
    dialogConfig.height = "80%";
    dialogConfig.width = "80%";
    dialogConfig.data = {
      group: group,
    }
    // https://material.angular.io/components/dialog/overview
    const modalDialog = this.matDialog.open(NewTenantModalComponent, dialogConfig);
    modalDialog.afterClosed().toPromise().then(() => {
      elementRef.update()
    })

  }

  openOnboardVsbModal(elementRef) {

    const dialogConfig = new MatDialogConfig();
    // The user can't close the dialog by clicking outside its body
    dialogConfig.id = "onboard-vsb-modal-component";
    dialogConfig.height = "80%";
    dialogConfig.width = "80%";
    dialogConfig.data = {
    }
    // https://material.angular.io/components/dialog/overview
    const modalDialog = this.matDialog.open(OnboardVsbModalComponent, dialogConfig);
    modalDialog.afterClosed().toPromise().then(() => {
      elementRef.update()
    })
  }

  openOnboardNstModal(elementRef) {

    const dialogConfig = new MatDialogConfig();
    // The user can't close the dialog by clicking outside its body
    dialogConfig.id = "onboard-vsb-modal-component";
    dialogConfig.height = "80%";
    dialogConfig.width = "80%";
    dialogConfig.data = {
    }
    // https://material.angular.io/components/dialog/overview
    const modalDialog = this.matDialog.open(OnboardNstModalComponent, dialogConfig);
    modalDialog.afterClosed().toPromise().then((data) => {
      elementRef.update()
    })
  }

  openCreateNsModal(elementRef, nst) {

    const dialogConfig = new MatDialogConfig();
    // The user can't close the dialog by clicking outside its body
    dialogConfig.id = "create-ns-modal-component";
    dialogConfig.height = "80%";
    dialogConfig.width = "80%";
    dialogConfig.data = {
      nst: nst
    }
    // https://material.angular.io/components/dialog/overview
    const modalDialog = this.matDialog.open(CreateNsModalComponent, dialogConfig);
    modalDialog.afterClosed().toPromise().then((data) => {
      elementRef.update()
      elementRef.showToast(data)
    })
  }

  openInstantiateNsModal(elementRef, nst) {

    const dialogConfig = new MatDialogConfig();
    // The user can't close the dialog by clicking outside its body
    dialogConfig.id = "instantiate-ns-modal-component";
    dialogConfig.height = "80%";
    dialogConfig.width = "80%";
    dialogConfig.data = {
      nst: nst
    }
    // https://material.angular.io/components/dialog/overview
    const modalDialog = this.matDialog.open(InstantiateNsModalComponent, dialogConfig);
    modalDialog.afterClosed().toPromise().then((data) => {
      elementRef.update()
      elementRef.showToast(data)
    })
  }

  openCreateDescriptorModal(elementRef, blueprint) {

    const dialogConfig = new MatDialogConfig();
    // The user can't close the dialog by clicking outside its body
    dialogConfig.id = "create-descriptor-modal-component";
    dialogConfig.height = "80%";
    dialogConfig.width = "80%";
    dialogConfig.data = {
      blueprint: blueprint
    }
    // https://material.angular.io/components/dialog/overview
    const modalDialog = this.matDialog.open(CreateDescriptorModalComponent, dialogConfig);
    modalDialog.beforeClosed().toPromise().then((data) => {
      // elementRef.closeModal()
      elementRef.update()
      elementRef.showToast(data)
    })
  }

  openCreateInstantiateVSModal(elementRef, descriptor) {

    const dialogConfig = new MatDialogConfig();
    // The user can't close the dialog by clicking outside its body
    dialogConfig.id = "instance-vs-modal-component";
    dialogConfig.height = "80%";
    dialogConfig.width = "80%";
    dialogConfig.data = {
      descriptor: descriptor
    }
    // https://material.angular.io/components/dialog/overview
    const modalDialog = this.matDialog.open(InstantiateVsModalComponent, dialogConfig);
    modalDialog.beforeClosed().toPromise().then((data) => {
      // elementRef.closeModal()
      elementRef.update()
      elementRef.showToast(data)
    })
  }

  openScaleVSModal(elementRef, vsi) {

    const dialogConfig = new MatDialogConfig();
    // The user can't close the dialog by clicking outside its body
    dialogConfig.id = "scale-vs-modal-component";
    dialogConfig.height = "80%";
    dialogConfig.width = "80%";
    dialogConfig.data = {
      vsi: vsi
    }
    // https://material.angular.io/components/dialog/overview
    const modalDialog = this.matDialog.open(ScaleVsModalComponent, dialogConfig);
    modalDialog.beforeClosed().toPromise().then(() => {
      // elementRef.closeModal()
      elementRef.update()

    })
  }

  openCreateSlaModal(elementRef, group, tenant) {

    const dialogConfig = new MatDialogConfig();
    // The user can't close the dialog by clicking outside its body
    dialogConfig.id = "create-sla-modal-component";
    dialogConfig.height = "80%";
    dialogConfig.width = "80%";
    dialogConfig.data = {
      group: group,
      tenant: tenant
    }
    // https://material.angular.io/components/dialog/overview
    const modalDialog = this.matDialog.open(CreateSlaModalComponent, dialogConfig);
    modalDialog.beforeClosed().toPromise().then(() => {
      // elementRef.closeModal()
      elementRef.update()

    })
  }

  openViewSlaModal(elementRef, group, tenant) {

    const dialogConfig = new MatDialogConfig();
    // The user can't close the dialog by clicking outside its body
    dialogConfig.id = "view-descriptor-modal-component";
    dialogConfig.height = "80%";
    dialogConfig.width = "80%";
    dialogConfig.data = {
      group: group,
      tenant: tenant
    }
    // https://material.angular.io/components/dialog/overview
    const modalDialog = this.matDialog.open(ViewSlaModalComponent, dialogConfig);
    modalDialog.beforeClosed().toPromise().then(() => {
      // elementRef.closeModal()
      elementRef.update()
    })
  }

  openConfirmModal(elementRef) {

    const dialogConfig = new MatDialogConfig();
    // The user can't close the dialog by clicking outside its body
    dialogConfig.id = "confirm-modal-component";
    dialogConfig.height = "20%";
    dialogConfig.width = "40%";
    // https://material.angular.io/components/dialog/overview
    const modalDialog = this.matDialog.open(ConfirmModalComponent, dialogConfig);
    // modalDialog.beforeClosed().toPromise().then((data) => {
    //   console.log(data)
    //   // elementRef.closeModal()
    //   // elementRef.update()
    // })
    return modalDialog
  }

  openModifyNsModal(elementRef, nsi) {

    const dialogConfig = new MatDialogConfig();
    // The user can't close the dialog by clicking outside its body
    dialogConfig.id = "modify-ns-modal-component";
    dialogConfig.height = "80%";
    dialogConfig.width = "80%";
    dialogConfig.data = {
      nsi: nsi
    }
    // https://material.angular.io/components/dialog/overview
    const modalDialog = this.matDialog.open(ModifyNSModalComponent, dialogConfig);
    modalDialog.beforeClosed().toPromise().then(() => {
      // elementRef.closeModal()
      elementRef.update()
    })
    return modalDialog
  }

  openOnboardDomainModal(elementRef, domain) {

    const dialogConfig = new MatDialogConfig();
    // The user can't close the dialog by clicking outside its body
    dialogConfig.id = "onboard-domain-modal-component";
    dialogConfig.height = "80%";
    dialogConfig.width = "80%";
    dialogConfig.data = {
      domain: domain
    }
    // https://material.angular.io/components/dialog/overview
    const modalDialog = this.matDialog.open(OnboardDomainModalComponent, dialogConfig);
    modalDialog.beforeClosed().toPromise().then(() => {
      // elementRef.closeModal()
      elementRef.update()
    })
    return modalDialog
  }

}
