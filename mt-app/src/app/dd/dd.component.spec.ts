import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DdComponent } from './dd.component';

describe('DdComponent', () => {
  let component: DdComponent;
  let fixture: ComponentFixture<DdComponent>;

  beforeEach(() => {
    fixture = TestBed.createComponent(DdComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should compile', () => {
    expect(component).toBeTruthy();
  });
});
