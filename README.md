# Two-Stream Graph Convolutional Network for Intra-Oral Scanner Image Segmentation

## Instructions for running the training script and visualize results
1. Create conda env
```bash
conda env create -f env.yml
conda activate TSGCNet
pip install -r requirements.txt
```
2. Run the training scripts
```bash
python train.py --num_epochs=30
```
3. Visualize result
```bash
python visualization.py
```
Below is the result after training 1, 20, and 30 epochs and Label (ground truth image of teeth segmentation)

### Label
![alt text](https://github.com/hoangkimthuc/TSGCNet/blob/main/output/label.png?raw=true)

### Result after training 1 epoch
![alt text](https://github.com/hoangkimthuc/TSGCNet/blob/main/output/output_1epoch.png?raw=true)

### Result after training 20 epochs
![alt text](https://github.com/hoangkimthuc/TSGCNet/blob/main/output/output_20epoch.png?raw=true)

### Result after training 30 epochs
![alt text](https://github.com/hoangkimthuc/TSGCNet/blob/main/output/output_30epoch.png?raw=true)

## Prequisites
* python 3.7.4
* pytorch 1.4.0
* numpy 1.19.0
* plyfile 0.7.1

## Introduction
This work is the pytorch implementation of **TSGCN**, which has been published in IEEE Transactions on Medical Imaging (https://ieeexplore.ieee.org/abstract/document/9594785/) and CVPR 2021 (https://openaccess.thecvf.com/content/CVPR2021/html/Zhang_TSGCNet_Discriminative_Geometric_Feature_Learning_With_Two-Stream_Graph_Convolutional_Network_CVPR_2021_paper.html).
#

## Usage
To train the TSGCN, please put the trainning data and testing data into data/train and data/test, respectively. Then, you can start to train a TSGCN model by following command.

```shell
python train.py
```
#
## Citation
If you find our work useful in your research, please cite:
* Y. Zhao et al., "Two-Stream Graph Convolutional Network for Intra-Oral Scanner Image Segmentation," in IEEE Transactions on Medical Imaging, vol. 41, no. 4, pp. 826-835, April 2022, doi: 10.1109/TMI.2021.3124217.
* Zhang L, Zhao Y, Meng D, et al. TSGCNet: Discriminative Geometric Feature Learning with Two-Stream Graph Convolutional Network for 3D Dental Model Segmentation[C]//Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2021: 6699-6708.
