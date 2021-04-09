import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OnboardDomainModalComponent } from './onboard-domain-modal.component';

describe('OnboardDomainModalComponent', () => {
  let component: OnboardDomainModalComponent;
  let fixture: ComponentFixture<OnboardDomainModalComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [OnboardDomainModalComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OnboardDomainModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
