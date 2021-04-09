import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { InstantiateVsModalComponent } from './instantiate-vs-modal.component';

describe('InstantiateVsModalComponent', () => {
  let component: InstantiateVsModalComponent;
  let fixture: ComponentFixture<InstantiateVsModalComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ InstantiateVsModalComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(InstantiateVsModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
