import { Component, OnInit, Inject } from '@angular/core';
import { VsService } from '../../services/vsService/vs.service';
import { MessageService } from 'primeng/api';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { FileSystemFileEntry, NgxFileDropEntry } from 'ngx-file-drop';
import { ToastrService } from 'ngx-toastr';


declare var $: any;

@Component({
  selector: 'app-onboard-vsb-modal',
  templateUrl: './onboard-vsb-modal.component.html',
  styleUrls: ['./onboard-vsb-modal.component.css'],
  providers: [MessageService]
})
export class OnboardVsbModalComponent implements OnInit {

  vnfNumbers = [0]
  appNumbers = [0]
  rulesNumbers = [[0]]
  actionsNumbers = [[0]]
  vsbFiles = []
  nsdFiles = []
  nstFiles = []

  constructor(
    public dialogRef: MatDialogRef<OnboardVsbModalComponent>,
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

  vsbDropped(event) {
    this.prepareVSBFilesList(event);
  }

  deleteVSBFile(index: number) {
    this.vsbFiles.splice(index, 1);
  }

  prepareVSBFilesList(files: Array<any>) {
    this.vsbFiles = [];
    for (const item of files) {
      this.vsbFiles.push(item);
    }
  }

  nsdDropped(event) {
    this.prepareNSDFilesList(event);
  }

  deleteNSDFile(index: number) {
    this.nsdFiles.splice(index, 1)
  }

  prepareNSDFilesList(files: Array<any>) {
    for (const item of files) {
      item.progress = 0;
      this.nsdFiles.push(item);
    }
  }

  nstDropped(event) {
    this.prepareNSTFilesList(event);
  }

  deleteNSTFile(index: number) {
    this.nstFiles.splice(index, 1)
  }

  prepareNSTFilesList(files: Array<any>) {
    for (const item of files) {
      item.progress = 0;
      this.nstFiles.push(item);
    }
  }


  async onboardVsb() {
    let blueprint = {}
    let fileContent
    if (this.vsbFiles.length > 0) {
      fileContent = await this.getFileContent(this.vsbFiles[0])
      blueprint["vs_blueprint"] = fileContent
    }

    if (this.nsdFiles.length > 0) {
      blueprint["nsds"] = []

      for (let file of this.nsdFiles) {
        fileContent = await this.getFileContent(file)
        blueprint["nsds"].push(fileContent)
      }
    }

    if (this.nstFiles.length > 0) {
      blueprint["nsts"] = []

      for (let file of this.nstFiles) {
        fileContent = await this.getFileContent(file)
        blueprint["nsts"].push(fileContent)
      }
    }


    for (let vnfNumber of this.vnfNumbers) {
      let name = $("#vnfname" + vnfNumber).val()
      let version = $("#vnfversion" + vnfNumber).val()
      let provider = $("#vnfprovider" + vnfNumber).val()
      let checksum = $("#vnfchecksum" + vnfNumber).val()
      let path = $("#vnfpath" + vnfNumber).val()
      if (name == "") {
        break
      } else {
        if (blueprint["vnf_packages"] == null) {
          blueprint["vnf_packages"] = [{ name: name, version: version, provider: provider, checksum: checksum, vnf_package_path: path }]
        } else {
          blueprint["vnf_packages"].push({ name: name, version: version, provider: provider, checksum: checksum, vnf_package_path: path })
        }
      }
    }

    for (let appNumber of this.appNumbers) {
      let name = $("#appname" + appNumber).val()
      let version = $("#appversion" + appNumber).val()
      let provider = $("#appprovider" + appNumber).val()
      let checksum = $("#appchecksum" + appNumber).val()
      let path = $("#apppath" + appNumber).val()
      if (name == "") {
        break
      } else {
        if (blueprint["mec_app_packages"] == null) {
          blueprint["mec_app_packages"] = [{ name: name, version: version, provider: provider, checksum: checksum, mec_package_path: path }]
        } else {
          blueprint["mec_app_packages"].push({ name: name, version: version, provider: provider, checksum: checksum, mec_package_path: path })
        }
      }
    }

    for (let ruleNumber in this.rulesNumbers) {
      let nsdid = $("#ruleNSDid" + ruleNumber).val()
      let nstid = $("#ruleNstId" + ruleNumber).val()
      let nsdversion = $("#ruleNSDversion" + ruleNumber).val()
      let nsflavourid = $("#ruleNSflavourid" + ruleNumber).val()
      let instlevelid = $("#ruleinstlevelid" + ruleNumber).val()
      let userInput = []
      for (let inputNumber in this.rulesNumbers[ruleNumber]) {
        let paramid = $("#ruleparamid" + ruleNumber + "_" + inputNumber).val()
        let parammin = $("#ruleparammin" + ruleNumber + "_" + inputNumber).val()
        let parammax = $("#ruleparammax" + ruleNumber + "_" + inputNumber).val()
        userInput.push({ parameter_id: paramid, min_value: parseInt(parammin), max_value: parseInt(parammax) })
      }
      if (nsdid == "") {
        break
      } else {
        if (blueprint["translation_rules"] == null) {
          blueprint["translation_rules"] = [{ nsd_id: nsdid, nsd_version: nsdversion, nst_id: nstid, ns_flavour_id: nsflavourid, ns_instantiation_level_id: instlevelid, input: userInput }]
        } else {
          blueprint["translation_rules"].push({ nsd_id: nsdid, nsd_version: nsdversion, ns_flavour_id: nsflavourid, ns_instantiation_level_id: instlevelid, input: userInput })
        }
      }
    }

    for (let actionNumber in this.actionsNumbers) {
      let actionId = $("#actionId" + actionNumber).val()
      let actionName = $("#actionName" + actionNumber).val()
      let actionParameters = []
      for (let parameterNumber in this.actionsNumbers[actionNumber]) {
        let paramid = $("#actionparamid" + actionNumber + "_" + parameterNumber).val()
        let paramname = $("#actionparamname" + actionNumber + "_" + parameterNumber).val()
        let paramtype = $("#actionparamtype" + actionNumber + "_" + parameterNumber).val()
        let paramdefault = $("#actionparamdefault" + actionNumber + "_" + parameterNumber).val()
        actionParameters.push({ parameter_id: paramid, parameter_name: paramname, parameter_type: paramtype, parameter_default_value: paramdefault })
      }
      if (actionId == "") {
        break
      } else {
        if (blueprint["available_actions"] == null) {
          blueprint["available_actions"] = [{ action_id: actionId, action_name: actionName, parameters: actionParameters }]
        } else {
          blueprint["available_actions"].push({ action_id: actionId, action_name: actionName, parameters: actionParameters })
        }
      }
    }

    console.log(blueprint)
    await this.vs.onboardVSB(blueprint).then(()=>{
      this.closeModal()
    }).catch((message)=>{
      this.toastr.error(message.error,"Blueprint Onboard Error", {positionClass: 'toast-bottom-center'})
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

  async getPlainFileContent(file) {
    let reader = new FileReader()
    let filename = file.name

    return new Promise((resolve, reject) => {
      reader.onerror = () => {
        reader.abort();
        reject(new DOMException("Problem parsing input file."));
      };

      reader.onload = () => {
        console.log(reader.result.toString());
      };

      reader.readAsText(file)
    })
  }


  addVNFForm() {
    this.vnfNumbers.push(this.vnfNumbers[this.vnfNumbers.length - 1] + 1)
  }

  addAPPForm() {
    this.appNumbers.push(this.appNumbers[this.appNumbers.length - 1] + 1)
  }

  addRuleForm() {
    this.rulesNumbers.push([0])
  }

  addActionForm() {
    this.actionsNumbers.push([0])
  }

  addInputParameterForm(index) {
    this.rulesNumbers[index].push(this.rulesNumbers[index][this.rulesNumbers[index].length - 1] + 1)
  }

  addActionParameterForm(index) {
    this.actionsNumbers[index].push(this.actionsNumbers[index][this.actionsNumbers[index].length - 1] + 1)
  }

  myStyle(i) {
    let styles = {
      'border-left': i != 0 ? 'solid 2px #ffa500' : '',
      'border-radius': i != 0 ? '10px' : ''
    };

    return styles;
  }

  removeVNF(i) {
    this.vnfNumbers.splice(i, 1);
  }

  removeAPP(i) {
    this.appNumbers.splice(i, 1);
  }

  removeRule(i) {
    this.rulesNumbers.splice(i, 1);
  }

  removeAction(i) {
    this.actionsNumbers.splice(i, 1);
  }

  removeActionParameter(i, j) {
    this.actionsNumbers[i].splice(j, 1);
  }

  removeParameter(i, j) {
    this.rulesNumbers[i].splice(j, 1);
  }
}