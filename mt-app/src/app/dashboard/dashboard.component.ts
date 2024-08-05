import { Component, OnInit } from '@angular/core';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatIconModule } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';

import { GridfieldComponent } from './gridfield/gridfield.component';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
  imports: [
    MatToolbarModule,
    MatIconModule,
    MatGridListModule,
    GridfieldComponent,
  ],
})
export class DashboardComponent implements OnInit {
  title: string = 'Dashboard';
  ngOnInit(): void {}
}
