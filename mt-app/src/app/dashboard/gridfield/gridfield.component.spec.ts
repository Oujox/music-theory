import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GridfieldComponent } from './gridfield.component';

describe('GridfieldComponent', () => {
  let component: GridfieldComponent;
  let fixture: ComponentFixture<GridfieldComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GridfieldComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GridfieldComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
