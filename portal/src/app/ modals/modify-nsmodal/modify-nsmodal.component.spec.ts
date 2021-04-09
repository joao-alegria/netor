import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ModifyNSModalComponent } from './modify-nsmodal.component';

describe('ModifyNSModalComponent', () => {
  let component: ModifyNSModalComponent;
  let fixture: ComponentFixture<ModifyNSModalComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ModifyNSModalComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ModifyNSModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
