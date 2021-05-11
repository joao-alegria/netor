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
    return this.http.get(config.vsEndpoint + config.whoami, { headers:headers }).toPromise();
  }

  async checkLoggedIn() {
    await $(document).ready(() => this.ngZone.run(() => {
      this.whoami().then(data => {
        localStorage.setItem("role", data["data"]["role"])
        localStorage.setItem("username", data["data"]["username"])
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
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.get(config.vsEndpoint + config.vsdescriptors, { headers:headers }).toPromise();
  }

  async getBlueprints() {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.get(config.vsEndpoint + config.vsblueprints, { headers:headers }).toPromise();
  }

  async getSpecificBlueprint(vsbId) {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.get(config.vsEndpoint + config.vsblueprints+"/"+vsbId, { headers:headers }).toPromise();
  }

  async getGroups() {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.get(config.vsEndpoint + config.vsgroups, { headers:headers }).toPromise();
  }

  async getAllTenants() {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.get(config.vsEndpoint + config.vstenants, { headers:headers }).toPromise();
  }

  async getAllDomains() {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.get(config.vsEndpoint + config.vsdomains, { headers:headers }).toPromise();
  }

  async createNewDomain(data) {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.post(config.vsEndpoint + config.vsdomains, data, { headers:headers }).toPromise();
  }

  async deleteDomain(domain) {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.delete(config.vsEndpoint + config.vsdomains+"/"+domain, { headers:headers }).toPromise();
  }
  
  async getNSTemplates() {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.get(config.vsEndpoint + config.vsnstemplates, { headers:headers }).toPromise();
  }

  async getNetSlices() {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.get(config.vsEndpoint + config.vsns, { headers:headers }).toPromise();
  }

  async getVerticalSlices() {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    let allVerticalSlices = []
    return await this.http.get(config.vsEndpoint + config.vsverticalslices, { headers:headers }).toPromise()
    // .then(async (data) => {
    //   for (let element in data) {
    //     await this.http.get(config.vsEndpoint + config.vsverticalslicesID + "/" + data[element], { headers:headers }).toPromise().then((verticalSlice) => {
    //       allVerticalSlices.push(verticalSlice)
    //     })
    //   }
    // });
    // return allVerticalSlices
  }

  async createNewGroup(data) {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.post(config.vsEndpoint + config.vsgroups, data, { headers:headers }).toPromise();
  }

  async deleteGroup(group) {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.delete(config.vsEndpoint + config.vsgroups + "/" + group, { headers:headers }).toPromise();
  }

  async createNewGroupTenant(data) {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.post(config.vsEndpoint + config.vstenants, data, { headers:headers }).toPromise();
  }

  async deleteGroupTenant(group, tenant) {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.delete(config.vsEndpoint + config.vstenants + "/" + tenant, { headers:headers }).toPromise();
  }

  async onboardVSB(data) {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.post(config.vsEndpoint + config.vsblueprints, data, { headers:headers }).toPromise();
  }

  async onboardNST(data) {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.post(config.vsEndpoint + config.vsnst, data, { headers:headers }).toPromise();
  }

  async deleteNST(nstId) {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    const parameters=new HttpParams().set('nst_id', nstId);
    return this.http.delete(config.vsEndpoint + config.vsnst, { params:parameters,headers:headers }).toPromise();
  }

  async createNewNS(data) {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.post(config.vsEndpoint + config.vsns, data, { headers:headers }).toPromise();
  }

  async deleteVSB(blueprintID) {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    const parameters=new HttpParams().set('vsb_id', blueprintID);
    return this.http.delete(config.vsEndpoint + config.vsblueprints, { params:parameters, headers:headers }).toPromise();
  }

  async createNewDescriptor(data) {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.post(config.vsEndpoint + config.vsdescriptors, data, { headers:headers }).toPromise();
  }

  async deleteDescriptor(descriptorId) {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    const parameters=new HttpParams().set('vsd_id', descriptorId);
    return this.http.delete(config.vsEndpoint + config.vsdescriptors,{params:parameters ,headers:headers}).toPromise();
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
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.post(config.vsEndpoint + config.vsverticalslicesID + "/" + vsiId + "/terminate", "", { headers:headers }).toPromise();
  }

  async deleteVSI(vsiId) {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.delete(config.vsEndpoint + config.vsverticalslicesID + "/" + vsiId, { headers:headers }).toPromise();
  }

  async scaleVSI(vsiId, data) {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.put(config.vsEndpoint + config.vsverticalslicesID + "/" + vsiId, data, { headers:headers }).toPromise();
  }

  async createSLA(group, tenant, sla) {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.post(config.vsEndpoint + config.vsgroups + "/" + group + "/tenant/" + tenant + "/sla", sla, { headers:headers }).toPromise();
  }

  async getSLA(group, tenant) {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.get(config.vsEndpoint + config.vsgroups + "/" + group + "/tenant/" + tenant + "/sla", { headers:headers }).toPromise();
  }

  async deleteSLA(group, tenant, id) {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.delete(config.vsEndpoint + config.vsgroups + "/" + group + "/tenant/" + tenant + "/sla/" + id, { headers:headers }).toPromise();
  }

  async modifyNS(nsiId, data) {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.put(config.vsEndpoint + config.vsns + "/" + nsiId + "/action/modify", data, { headers:headers }).toPromise();
  }

  async terminateNS(nsiId) {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.put(config.vsEndpoint + config.vsns + "/" + nsiId + "/action/terminate", { headers:headers }).toPromise();
  }

  async instantiateNS(nsiId, data) {
    const headers=new HttpHeaders().set('Authorization', 'Bearer '+localStorage.getItem("accessToken"));
    return this.http.put(config.vsEndpoint + config.vsns + "/" + nsiId + "/action/instantiate", data, { headers:headers }).toPromise();
  }
}
