import { TestBed } from '@angular/core/testing';

import { ModalserviceService } from './modalservice.service';

describe('ModalserviceService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: ModalserviceService = TestBed.get(ModalserviceService);
    expect(service).toBeTruthy();
  });
});
