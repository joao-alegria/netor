import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { InstantiateNsModalComponent } from './instantiate-ns-modal.component';

describe('InstantiateNsModalComponent', () => {
  let component: InstantiateNsModalComponent;
  let fixture: ComponentFixture<InstantiateNsModalComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ InstantiateNsModalComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(InstantiateNsModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
