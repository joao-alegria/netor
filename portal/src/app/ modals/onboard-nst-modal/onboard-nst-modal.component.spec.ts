import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OnboardNstModalComponent } from './onboard-nst-modal.component';

describe('OnboardNstModalComponent', () => {
  let component: OnboardNstModalComponent;
  let fixture: ComponentFixture<OnboardNstModalComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [OnboardNstModalComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OnboardNstModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
