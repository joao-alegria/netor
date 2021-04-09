import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ScaleVsModalComponent } from './scale-vs-modal.component';

describe('ScaleVsModalComponent', () => {
  let component: ScaleVsModalComponent;
  let fixture: ComponentFixture<ScaleVsModalComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ScaleVsModalComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ScaleVsModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
