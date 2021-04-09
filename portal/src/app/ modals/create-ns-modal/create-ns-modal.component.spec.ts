import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateNsModalComponent } from './create-ns-modal.component';

describe('CreateNsModalComponent', () => {
  let component: CreateNsModalComponent;
  let fixture: ComponentFixture<CreateNsModalComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CreateNsModalComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateNsModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
