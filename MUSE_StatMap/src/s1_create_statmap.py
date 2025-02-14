import nibabel as nib
import numpy as np
import pandas as pd
from scipy import stats
import os

#'''
#Script to create a statistical map using a list of p values for MUSE ROIs
#'''

###############################################
# Hard coded I/O variables for the example data
#  Users can modify this part to their own data
f_temp = '../templates/Template1_label.nii.gz'                  # Template image with MUSE labels
f_pvals = '../examples/example1/input/list_ROI_pvalues.csv'     # Example list with p values
roi_var = 'Index'           # Column name with MUSE ROI index
sel_var = 'pvalue'          # Column name with the outcome variable
flag_log = True             # Transform values (default: Yes, p values are log-transformed)
flag_reset_neg = True       # Set negative values to 0 (default: Yes)
out_dir = '../examples/example1/output'
###############################################

# Create output dir
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
out_file = os.path.join(out_dir, f'MUSE_StatMap_{sel_var}.nii.gz')

if os.path.exists(out_file):
    print(f'Out file exists, aborting: {out_file}')

else:
    # Read list
    df = pd.read_csv(f_pvals)

    ## Read ROI label image
    nii_roi = nib.load(f_temp)
    img_roi = nii_roi.get_fdata()
    nii_roi.set_data_dtype(float)
    roi_list = np.unique(img_roi)[1:]

    # Select ROIs present in label image
    df = df[df.Index.isin(roi_list)]

    # Create ROI image with values replaced by outcome values
    img_out = img_roi * 0.0
    for i, tmp_row in df.iterrows():
        tmp_ind = tmp_row[roi_var]
        tmp_var = tmp_row[sel_var]
        print(f'Set values for ROI: {tmp_ind}')
        if flag_log:
            tmp_var = -1 * np.log10(tmp_var)
        if flag_reset_neg:
            if tmp_var<0:
                tmp_var = 0
        # Replace ROI voxels by p val
        img_out[img_roi==tmp_ind] = tmp_var

    # Write output image
    out_nii = nib.Nifti1Image(img_out, nii_roi.affine)
    try:
        nib.save(out_nii, out_file)
        print(f'Output image created: {out_file}')
    except:
        print(f'Could not create output image: {out_file}')
        

