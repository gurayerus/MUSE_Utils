#! /bin/bash

timg='../templates/Template1.nii.gz'
limg='../templates/Template1_label.nii.gz'
pimg='../examples/example1/output/MUSE_StatMap_pvalue.nii.gz'

fsleyes $timg $limg -cm Random -a 50 ${pimg} -dr 2 3 -cm Red-Yellow -a 50

