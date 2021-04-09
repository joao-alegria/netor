import { BrowserModule } from '@angular/platform-browser';
import { NgModule, CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';

import { ToastModule } from 'primeng/toast';
import { ChipsModule } from 'primeng/chips';

import { AppRoutingModule } from './routing/app-routing.module';
import { NetworkDiagramComponent } from './elements/network-diagram/network-diagram.component';
import { HttpClientModule } from '@angular/common/http';
import { AppComponent } from './app.component';
import { HomeComponent } from './pages/home/home.component';
import { LoginComponent } from './pages/login/login.component';
import { LoadingComponent } from './elements/loading/loading.component';
import { TenantsComponent } from './pages/tenants/tenants.component';
import { BlueprintsComponent } from './pages/blueprints/blueprints.component';
import { DescriptorsComponent } from './pages/descriptors/descriptors.component';
import { NetslicesComponent } from './pages/netslices/netslices.component';
import { VetsliceinstComponent } from './pages/vetsliceinst/vetsliceinst.component';
import { MainModalComponent } from './ modals/main-modal/main-modal.component';
import { ModalserviceService } from './services/modalService/modalservice.service';

import { MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { NgxFileDropModule } from 'ngx-file-drop';
import { NewTenantModalComponent } from './ modals/new-tenant-modal/new-tenant-modal.component';
import { OnboardVsbModalComponent } from './ modals/onboard-vsb-modal/onboard-vsb-modal.component';
import { CreateDescriptorModalComponent } from './ modals/create-descriptor-modal/create-descriptor-modal.component';
import { InstantiateVsModalComponent } from './ modals/instantiate-vs-modal/instantiate-vs-modal.component';
import { ScaleVsModalComponent } from './ modals/scale-vs-modal/scale-vs-modal.component';
import { CreateSlaModalComponent } from './ modals/create-sla-modal/create-sla-modal.component';
import { ViewSlaModalComponent } from './ modals/view-sla-modal/view-sla-modal.component';
import { NstemplatesComponent } from './pages/nstemplates/nstemplates.component';
import { DomainsComponent } from './pages/domains/domains.component';
import { OnboardNstModalComponent } from './ modals/onboard-nst-modal/onboard-nst-modal.component';
import { OnboardDomainModalComponent } from './ modals/onboard-domain-modal/onboard-domain-modal.component';
import { CreateNsModalComponent } from './ modals/create-ns-modal/create-ns-modal.component';
import { ConfirmModalComponent } from './ modals/confirm-modal/confirm-modal.component';
import { ModifyNSModalComponent } from './ modals/modify-nsmodal/modify-nsmodal.component';
import { InstantiateNsModalComponent } from './ modals/instantiate-ns-modal/instantiate-ns-modal.component';
import { MapComponent } from './elements/map/map.component';
import { SlicerSelectorComponent } from './pages/slicer-selector/slicer-selector.component';
import {MatCommonModule, MatInputModule, MatChipsModule} from '@angular/material';
import { FormsModule } from '@angular/forms';
import { NoopAnimationsModule, BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatIconModule} from '@angular/material/icon';
import { ToastrModule } from 'ngx-toastr';


@NgModule({
  declarations: [
    NetworkDiagramComponent,
    AppComponent,
    HomeComponent,
    LoginComponent,
    LoadingComponent,
    TenantsComponent,
    BlueprintsComponent,
    DescriptorsComponent,
    NetslicesComponent,
    VetsliceinstComponent,
    MainModalComponent,
    NewTenantModalComponent,
    OnboardVsbModalComponent,
    CreateDescriptorModalComponent,
    InstantiateVsModalComponent,
    ScaleVsModalComponent,
    CreateSlaModalComponent,
    ViewSlaModalComponent,
    NstemplatesComponent,
    DomainsComponent,
    OnboardNstModalComponent,
    OnboardDomainModalComponent,
    CreateNsModalComponent,
    ConfirmModalComponent,
    ModifyNSModalComponent,
    InstantiateNsModalComponent,
    MapComponent,
    SlicerSelectorComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    HttpClientModule,
    ToastModule,
    MatDialogModule,
    NgxFileDropModule,
    ChipsModule,
    FormsModule, 
    NoopAnimationsModule, 
    MatChipsModule, 
    MatInputModule,
    MatCommonModule,
    MatIconModule,
    ToastrModule.forRoot({
      maxOpened: 1,
      autoDismiss: true
    })
  ],
  providers: [CookieService, ModalserviceService],
  bootstrap: [AppComponent],
  entryComponents: [
    MainModalComponent, NewTenantModalComponent, OnboardVsbModalComponent, CreateDescriptorModalComponent, InstantiateVsModalComponent, ScaleVsModalComponent, CreateSlaModalComponent, ViewSlaModalComponent, OnboardNstModalComponent, OnboardDomainModalComponent, CreateNsModalComponent, ConfirmModalComponent, ModifyNSModalComponent, InstantiateNsModalComponent
  ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA]
})
export class AppModule { }
