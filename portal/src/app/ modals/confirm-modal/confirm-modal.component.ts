import { Component, OnInit, Inject } from '@angular/core';
import { VsService } from '../../services/vsService/vs.service';
import { MessageService } from 'primeng/api';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'app-confirm-modal',
  templateUrl: './confirm-modal.component.html',
  styleUrls: ['./confirm-modal.component.css'],
  providers: [MessageService]
})
export class ConfirmModalComponent implements OnInit {


  constructor(
    public dialogRef: MatDialogRef<ConfirmModalComponent>,
    @Inject(MAT_DIALOG_DATA) private modalData: any,
    private vs: VsService, private messageService: MessageService
  ) {
    vs.checkLoggedIn()
  }

  ngOnInit() {
  }

  closeModal() {
    this.dialogRef.close(false);
  }

  yes() {
    this.dialogRef.close(true)
  }

  no() {
    this.dialogRef.close(false)
  }
}
