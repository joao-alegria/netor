import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OnboardVsbModalComponent } from './onboard-vsb-modal.component';

describe('OnboardVsbModalComponent', () => {
  let component: OnboardVsbModalComponent;
  let fixture: ComponentFixture<OnboardVsbModalComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OnboardVsbModalComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OnboardVsbModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
