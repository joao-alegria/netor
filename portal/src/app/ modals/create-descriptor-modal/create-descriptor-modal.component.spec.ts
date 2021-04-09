import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateDescriptorModalComponent } from './create-descriptor-modal.component';

describe('CreateDescriptorModalComponent', () => {
  let component: CreateDescriptorModalComponent;
  let fixture: ComponentFixture<CreateDescriptorModalComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CreateDescriptorModalComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateDescriptorModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
