import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { VetsliceinstComponent } from './vetsliceinst.component';

describe('VetsliceinstComponent', () => {
  let component: VetsliceinstComponent;
  let fixture: ComponentFixture<VetsliceinstComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ VetsliceinstComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(VetsliceinstComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
