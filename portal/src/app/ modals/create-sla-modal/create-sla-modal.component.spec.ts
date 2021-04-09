import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateSlaModalComponent } from './create-sla-modal.component';

describe('CreateSlaModalComponent', () => {
  let component: CreateSlaModalComponent;
  let fixture: ComponentFixture<CreateSlaModalComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CreateSlaModalComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateSlaModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
