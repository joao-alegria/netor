import { TestBed } from '@angular/core/testing';

import { VsService } from './vs.service';

describe('VsService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: VsService = TestBed.get(VsService);
    expect(service).toBeTruthy();
  });
});
