import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { VsService } from '../../services/vsService/vs.service';
import { MessageService } from 'primeng/api';
import { ModalserviceService } from '../../services/modalService/modalservice.service';
import { TranslationService } from '../../services/translationService/translation.service';


declare var $: any;

@Component({
  selector: 'app-modal',
  templateUrl: './main-modal.component.html',
  styleUrls: ['./main-modal.component.css'],
  providers: [MessageService]
})
export class MainModalComponent implements OnInit {

  content = "";
  vnfNumbers = [0]
  appNumbers = [0]
  rulesNumbers = [[0]]

  constructor(
    public dialogRef: MatDialogRef<MainModalComponent>,
    @Inject(MAT_DIALOG_DATA) private modalData: any,
    private vs: VsService, private modal: ModalserviceService, private messageService: MessageService, private translator: TranslationService
  ) {
    vs.checkLoggedIn()
  }

  ngOnInit() {
    $(document).ready(() => {
      this.auxShowDetailWriteToTable(this.modalData.data, 0)
    })

  }

  auxShowDetailWriteToTable(element, indents) {
    for (let key in element) {
      if (typeof (element[key]) != "object") {
        // if (indents == 0) {
        $("#modalContent").append("<div class='row'><div class='col-sm-" + indents + "'></div><b>" + this.translator.translate(key) + "</b> : " + element[key] + "</div>")
        // }
        // else { $("#modalContent").append("<div class='row'><div class='col-sm-" + indents + "'></div>" + this.translator.translate(key) + " : " + element[key] + "</div>") }
      } else {
        if (indents == 0) {
          $("#modalContent").append("<div class='row'><div class='col-sm-" + indents + "'></div><b>" + this.translator.translate(key) + ":</b></div>");
        } else {
          $("#modalContent").append("<div class='row'><div class='col-sm-" + indents + "'></div><b>" + this.translator.translate(key) + ":</b></div>")
        }
        if (Array.isArray(element[key])) {
          for (let arrayElement of element[key]) {
            if (typeof (arrayElement) != "object") {
              $("#modalContent").append("<div class='row'><div class='col-sm-" + (indents + 1) + "'></div>" + arrayElement + "</div>")
            } else {
              this.auxShowDetailWriteToTable(arrayElement, indents + 1)
            }
          }
        } else {

          this.auxShowDetailWriteToTable(element[key], indents + 1)
        }
      }
    }
  }

  closeModal() {
    this.dialogRef.close();
  }


}
