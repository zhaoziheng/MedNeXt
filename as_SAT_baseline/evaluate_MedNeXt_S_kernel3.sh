export nnUNet_raw_data_base="/mnt/hwfile/medai/zhaoziheng/SAM/nnUNet_data"
export nnUNet_preprocessed="/mnt/hwfile/medai/zhaoziheng/SAM/nnUNet_data/nnUNet_MedNeXt_preprocessed"
export RESULTS_FOLDER="/mnt/hwfile/medai/zhaoziheng/SAM/nnUNet_data/nnUNet_MedNeXt_results"

srun1g \
mednextv1_predict \
-i '/mnt/hwfile/medai/zhaoziheng/SAM/nnUNet_data/nnUNet_MedNeXt_raw/Task016_BTCV/imagesTs' \
-o '/mnt/hwfile/medai/zhaoziheng/SAM/nnUNet_data/nnUNet_MedNeXt_raw/Task016_BTCV/labelsPred_MedNeXt_S_kernel3' \
-chk '/mnt/hwfile/medai/zhaoziheng/SAM/nnUNet_data/nnUNet_MedNeXt_results/nnUNet/3d_fullres/Task016_BTCV/nnUNetTrainerV2_MedNeXt_S_kernel3__nnUNetPlansv2.1_trgSp_1x1x1/fold_0/model_best' \
-t 16 \
-m 3d_fullres \
-f 0 \
-tr nnUNetTrainerV2_MedNeXt_S_kernel3 \
-p nnUNetPlansv2.1_trgSp_1x1x1 \
--disable_tta

srun0g \
python /mnt/petrelfs/zhaoziheng/Knowledge-Enhanced-Medical-Segmentation/MedNeXt/as_SAT_baseline/evaluate_MedNeXt_S_kernel3.py \
--dataset 'Task016_BTCV'