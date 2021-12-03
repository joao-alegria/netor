#!/bin/bash
cd base && COPYFILE_DISABLE=1 tar -cvz -f ../outputs/interdomain_vnf_2.tar.gz interdomain_vnf_2
COPYFILE_DISABLE=1 tar -cvz -f ../outputs/interdomain_slice_ns_2_Domain_1.tar.gz interdomain_slice_ns_2_Domain_1
COPYFILE_DISABLE=1 tar -cvz -f ../outputs/interdomain_slice_ns_2_Domain_2.tar.gz interdomain_slice_ns_2_Domain_2
cp interdomain_nsst_nst_2_Domain_1.yml ../outputs/interdomain_nsst_nst_2_Domain_1.yml
cp interdomain_nsst_nst_2_Domain_2.yml ../outputs/interdomain_nsst_nst_2_Domain_2.yml