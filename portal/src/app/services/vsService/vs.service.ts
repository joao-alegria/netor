import { Injectable, NgZone } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders } from "@angular/common/http";
import { Router } from '@angular/router';

import config from '../../../config';

declare var $: any;

@Injectable({
  providedIn: 'root'
})
export class VsService {

  private endpoints: Object;

  constructor(private http: HttpClient, private router: Router, private ngZone: NgZone) { }

  async login(username: string, password: string) {
    const parameters = new HttpParams()
      .set('grant_type', "password")
      .set('client_id', "portal")
      .set('client_secret', "portal")
      .set('response_type', "code")
      .set('username', username)
      .set('password', password);
    return await this.http.post(config.vsEndpoint + config.login,null,
      {
        params: parameters,
        observe: 'response'
      }
    ).toPromise();
  }

  async whoami() {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.get(config.vsEndpoint + config.whoami, { headers: headers }).toPromise();
  }

  async checkLoggedIn() {
    await $(document).ready(() => this.ngZone.run(() => {
      this.whoami().then(data => {
        localStorage.setItem("role", data["role"])
        localStorage.setItem("username", data["username"])
        if (localStorage.getItem("role") == "ADMIN") {
          $("#adminNav").show()
          $("#tenantNav").hide()
        } else {
          $("#adminNav").hide()
          $("#tenantNav").show()
        }
        $("#myNav").show()
        return data["role"]
      }).catch(error => {
        $("#myNav").hide()
        this.router.navigate(["/", "login"])
      })
    }))
  }

  async getDescriptors() {
    return this.http.get(config.vsEndpoint + config.vsdescriptors, { withCredentials: true }).toPromise();
  }

  async getBlueprints() {
    return this.http.get(config.vsEndpoint + config.vsblueprints, { withCredentials: true }).toPromise();
  }

  async getSpecificBlueprint(vsbId) {
    return this.http.get(config.vsEndpoint + config.vsblueprints+"/"+vsbId, { withCredentials: true }).toPromise();
  }

  async getGroups() {
    return this.http.get(config.vsEndpoint + config.vsgroups, { withCredentials: true }).toPromise();
  }

  async getAllTenants() {
    return this.http.get(config.vsEndpoint + config.vstenants, { withCredentials: true }).toPromise();
  }

  async getAllDomains() {
    return this.http.get(config.vsEndpoint + config.vsdomains, { withCredentials: true }).toPromise();
  }

  async createNewDomain(data) {
    return this.http.post(config.vsEndpoint + config.vsdomains, data, { withCredentials: true }).toPromise();
  }

  async deleteDomain(domain) {
    return this.http.delete(config.vsEndpoint + config.vsdomains+"/"+domain, { withCredentials: true }).toPromise();
  }
  
  async getNSTemplates() {
    return this.http.get(config.vsEndpoint + config.vsnstemplates, { withCredentials: true }).toPromise();
  }

  async getNetSlices() {
    return this.http.get(config.vsEndpoint + config.vsns, { withCredentials: true }).toPromise();
  }

  async getVerticalSlices() {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    let allVerticalSlices = []
    return await this.http.get(config.vsEndpoint + config.vsverticalslices, { headers:headers }).toPromise()
    // .then(async (data) => {
    //   for (let element in data) {
    //     await this.http.get(config.vsEndpoint + config.vsverticalslicesID + "/" + data[element], { withCredentials: true }).toPromise().then((verticalSlice) => {
    //       allVerticalSlices.push(verticalSlice)
    //     })
    //   }
    // });
    // return allVerticalSlices
  }

  async createNewGroup(name) {
    return this.http.post(config.vsEndpoint + config.vsgroups + "/" + name, "", { withCredentials: true }).toPromise();
  }

  async deleteGroup(group) {
    return this.http.delete(config.vsEndpoint + config.vsgroups + "/" + group, { withCredentials: true }).toPromise();
  }

  async createNewGroupTenant(group, data) {
    return this.http.post(config.vsEndpoint + config.vsgroups + "/" + group + "/tenant", data, { withCredentials: true }).toPromise();
  }

  async deleteGroupTenant(group, tenant) {
    return this.http.delete(config.vsEndpoint + config.vsgroups + "/" + group + "/tenant/" + tenant, { withCredentials: true }).toPromise();
  }

  async onboardVSB(data) {
    return this.http.post(config.vsEndpoint + config.vsblueprints, data, { withCredentials: true }).toPromise();
  }

  async onboardNST(data) {
    return this.http.post(config.vsEndpoint + config.vsnst, data, { withCredentials: true }).toPromise();
  }

  async deleteNST(nstId) {
    return this.http.delete(config.vsEndpoint + config.vsnst + "/" + nstId, { withCredentials: true }).toPromise();
  }

  async createNewNS(data) {
    return this.http.post(config.vsEndpoint + config.vsns, data, { withCredentials: true }).toPromise();
  }

  async deleteVSB(blueprintID) {
    return this.http.delete(config.vsEndpoint + config.vsblueprints + "/" + blueprintID, { withCredentials: true }).toPromise();
  }

  async createNewDescriptor(data) {
    return this.http.post(config.vsEndpoint + config.vsdescriptors, data, { withCredentials: true }).toPromise();
  }

  async deleteDescriptor(descriptorId) {
    return this.http.delete(config.vsEndpoint + config.vsdescriptors + "/" + descriptorId, { withCredentials: true }).toPromise();
  }

  async instantiateNewVS(data) {
    // const formData = new FormData();
    // formData.append('timestamp', Date.now().toString())
    // this.http.post("http://10.0.12.120:8082/startTimer/1", formData).toPromise()
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    let response=this.http.post(config.vsEndpoint + config.vsverticalslicesID, data, { headers:headers }).toPromise()
    return response;
  }

  async terminateVSI(vsiId) {
    return this.http.post(config.vsEndpoint + config.vsverticalslicesID + "/" + vsiId + "/terminate", "", { withCredentials: true }).toPromise();
  }

  async deleteVSI(vsiId) {
    return this.http.delete(config.vsEndpoint + config.vsverticalslicesID + "/" + vsiId, { withCredentials: true }).toPromise();
  }

  async scaleVSI(vsiId, data) {
    return this.http.put(config.vsEndpoint + config.vsverticalslicesID + "/" + vsiId, data, { withCredentials: true }).toPromise();
  }

  async createSLA(group, tenant, sla) {
    return this.http.post(config.vsEndpoint + config.vsgroups + "/" + group + "/tenant/" + tenant + "/sla", sla, { withCredentials: true }).toPromise();
  }

  async getSLA(group, tenant) {
    return this.http.get(config.vsEndpoint + config.vsgroups + "/" + group + "/tenant/" + tenant + "/sla", { withCredentials: true }).toPromise();
  }

  async deleteSLA(group, tenant, id) {
    return this.http.delete(config.vsEndpoint + config.vsgroups + "/" + group + "/tenant/" + tenant + "/sla/" + id, { withCredentials: true }).toPromise();
  }

  async modifyNS(nsiId, data) {
    return this.http.put(config.vsEndpoint + config.vsns + "/" + nsiId + "/action/modify", data, { withCredentials: true }).toPromise();
  }

  async terminateNS(nsiId) {
    return this.http.put(config.vsEndpoint + config.vsns + "/" + nsiId + "/action/terminate", { withCredentials: true }).toPromise();
  }

  async instantiateNS(nsiId, data) {
    return this.http.put(config.vsEndpoint + config.vsns + "/" + nsiId + "/action/instantiate", data, { withCredentials: true }).toPromise();
  }
}
