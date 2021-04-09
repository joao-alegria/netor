import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NetslicesComponent } from './netslices.component';

describe('NetslicesComponent', () => {
  let component: NetslicesComponent;
  let fixture: ComponentFixture<NetslicesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NetslicesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NetslicesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
