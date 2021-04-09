import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NstemplatesComponent } from './nstemplates.component';

describe('NstemplatesComponent', () => {
  let component: NstemplatesComponent;
  let fixture: ComponentFixture<NstemplatesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NstemplatesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NstemplatesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
