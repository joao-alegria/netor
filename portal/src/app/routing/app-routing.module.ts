import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from '../pages/home/home.component';
import { LoginComponent } from '../pages/login/login.component';
import { LoadingComponent } from '../elements/loading/loading.component';
import { TenantsComponent } from '../pages/tenants/tenants.component';
import { BlueprintsComponent } from '../pages/blueprints/blueprints.component';
import { DescriptorsComponent } from '../pages/descriptors/descriptors.component';
import { NetslicesComponent } from '../pages/netslices/netslices.component';
import { VetsliceinstComponent } from '../pages/vetsliceinst/vetsliceinst.component';
import { NstemplatesComponent } from '../pages/nstemplates/nstemplates.component';
import { DomainsComponent } from '../pages/domains/domains.component';



const routes: Routes = [
  { path: 'tenants', component: TenantsComponent },
  { path: 'domains', component: DomainsComponent },
  { path: 'home', component: HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'loading', component: LoadingComponent },
  { path: 'blueprints', component: BlueprintsComponent },
  { path: 'descriptors', component: DescriptorsComponent },
  { path: 'nstemplates', component: NstemplatesComponent },
  { path: 'netslices', component: NetslicesComponent },
  { path: 'vsinstances', component: VetsliceinstComponent },
  { path: '', redirectTo: "home", pathMatch: "full" }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
