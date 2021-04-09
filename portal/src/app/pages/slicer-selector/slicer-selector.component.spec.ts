import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SlicerSelectorComponent } from './slicer-selector.component';

describe('SlicerSelectorComponent', () => {
  let component: SlicerSelectorComponent;
  let fixture: ComponentFixture<SlicerSelectorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SlicerSelectorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SlicerSelectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
