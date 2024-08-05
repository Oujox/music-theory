import { Routes } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ExplorerComponent } from './explorer/explorer.component';
import { TreeComponent } from './tree/tree.component';
import { DdComponent } from './dd/dd.component';
import { NavComponent } from './nav/nav.component';
import { DasComponent } from './das/das.component';

export const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'explorer', component: ExplorerComponent },
  { path: '**', redirectTo: 'dashboard' },
];
