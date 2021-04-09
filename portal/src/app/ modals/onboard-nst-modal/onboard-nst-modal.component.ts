import { Component, OnInit, Inject } from '@angular/core';
import { VsService } from '../../services/vsService/vs.service';
import { MessageService } from 'primeng/api';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { FileSystemFileEntry, NgxFileDropEntry } from 'ngx-file-drop';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-onboard-nst-modal',
  templateUrl: './onboard-nst-modal.component.html',
  styleUrls: ['./onboard-nst-modal.component.css'],
  providers: [MessageService]
})
export class OnboardNstModalComponent implements OnInit {

  nstFiles

  constructor(
    public dialogRef: MatDialogRef<OnboardNstModalComponent>,
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

  nstDropped(event) {
    this.prepareNSTFilesList(event);
  }

  deleteNSTFile(index: number) {
    this.nstFiles.splice(index, 1);
  }

  prepareNSTFilesList(files: Array<any>) {
    this.nstFiles = [];
    for (const item of files) {
      this.nstFiles.push(item);
    }
  }

  async onboardNst() {
    let nst = {}
    let fileContent
    if (this.nstFiles.length > 0) {
      fileContent = await this.getFileContent(this.nstFiles[0])
      nst["nst"] = fileContent
    }

    this.vs.onboardNST(nst).then(()=>{
      this.dialogRef.close()
    }).catch((message)=>{
      this.toastr.error(message.error,"Blueprint Deletion Error", {positionClass: 'toast-bottom-center', closeButton: true})
    })
  }

  async getFileContent(file) {
    let reader = new FileReader()

    return new Promise((resolve, reject) => {
      reader.onerror = () => {
        reader.abort();
        reject(new DOMException("Problem parsing input file."));
      };

      reader.onload = () => {
        resolve(JSON.parse(reader.result.toString()))
      };

      reader.readAsText(file)
    })
  }

}
