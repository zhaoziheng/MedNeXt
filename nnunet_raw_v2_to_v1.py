import json
import os
import shutil

V2_RAW_PATH = '/mnt/hwfile/medai/zhaoziheng/SAM/nnUNet_data/nnUNet_raw'
MedNeXt_RAW_PATH = '/mnt/hwfile/medai/zhaoziheng/SAM/nnUNet_data/nnUNet_MedNeXt_raw'

def json_transfer(v2_dataset_name='Datasetxxx_xxx'):
    # 1. add a line：
    # "training":[{"image":"./imagesTr/prostate_16.nii.gz","label":"./labelsTr/prostate_16.nii.gz"}, ...],
    # "test": ["./imagesTs/prostate_08.nii.gz", ...]
    
    source_dir = f'{V2_RAW_PATH}/{v2_dataset_name}'
    target_dir = f'{MedNeXt_RAW_PATH}/{v2_dataset_name}'.replace('Dataset', 'Task')
    # Copy source to target
    # Ensure all files in source_dir exist in target_dir
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            s = os.path.join(root, file)
            d = os.path.join(target_dir, os.path.relpath(s, source_dir))
            # skip labelsPred of nnUNets
            if 'imagesTr' in d or 'labelsTr' in d or 'imagesTs' in d or 'labelsTs' in d:
                if not os.path.exists(os.path.dirname(d)):
                    os.makedirs(os.path.dirname(d))
                shutil.copy2(s, d)
    print(f'Copy {source_dir} to {target_dir}')
    
    with open(f'{V2_RAW_PATH}/{v2_dataset_name}/dataset.json', 'r') as f:
        data_json = json.load(f)
    
    training = []
    test = []
    for case in os.listdir(f'{V2_RAW_PATH}/{v2_dataset_name}/labelsTr'):    # img0039.nii.gz
        training.append({
            "image":f'{V2_RAW_PATH}/{v2_dataset_name}/imagesTr/{case}',
            "label":f'{V2_RAW_PATH}/{v2_dataset_name}/labelsTr/{case}'
            })
    
    for image_name in os.listdir(f'{V2_RAW_PATH}/{v2_dataset_name}/labelsTs'):
        test.append(f'{V2_RAW_PATH}/{v2_dataset_name}/imagesTs/{image_name}')
    
    # 2. change channel_names to modality
    
    data_json['training'] = training
    data_json['test'] = test
    data_json['numTest'] = len(test)
    data_json['modality'] = data_json['channel_names']
    del data_json['channel_names']
    
    # 3. change labels from {"background":"0", ...} to {"0":"background", ...}
    new_labels = {v:k for k,v in data_json['labels'].items()}
    data_json['labels'] = new_labels
    
    mednext_dataset_name = v2_dataset_name.replace('Dataset', 'Task')
    with open(f'{MedNeXt_RAW_PATH}/{mednext_dataset_name}/dataset.json', 'w') as f:
        json.dump(data_json, f, indent=4)
        
    print(f'Create {MedNeXt_RAW_PATH}/{mednext_dataset_name}/dataset.json')

if __name__ == '__main__':
    # 3D nnunet v2 raw_data --> 3D nnunet v1 raw_data
    
    json_transfer('Dataset017_CHAOSCT')