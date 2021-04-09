import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NewTenantModalComponent } from './new-tenant-modal.component';

describe('NewTenantModalComponent', () => {
  let component: NewTenantModalComponent;
  let fixture: ComponentFixture<NewTenantModalComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NewTenantModalComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NewTenantModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
