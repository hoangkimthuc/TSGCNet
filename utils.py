# *_*coding:utf-8 *_*
import os
import numpy as np
import torch
from torch.autograd import Variable
from tqdm import tqdm
from collections import defaultdict
import pandas as pd

from plyfile import PlyData, PlyElement



def compute_cat_iou(pred,target,iou_tabel):  # pred [B,N,C] target [B,N]
    iou_list = []
    target = target.cpu().data.numpy()
    for j in range(pred.size(0)):
        batch_pred = pred[j]  # batch_pred [N,C]
        batch_target = target[j]  # batch_target [N]
        batch_choice = batch_pred.data.max(1)[1].cpu().data.numpy()  # index of max value  batch_choice [N]
        for cat in np.unique(batch_target):
            # intersection = np.sum((batch_target == cat) & (batch_choice == cat))
            # union = float(np.sum((batch_target == cat) | (batch_choice == cat)))
            # iou = intersection/union if not union ==0 else 1
            I = np.sum(np.logical_and(batch_choice == cat, batch_target == cat))
            U = np.sum(np.logical_or(batch_choice == cat, batch_target == cat))
            if U == 0:
                iou = 1  # If the union of groundtruth and prediction points is empty, then count part IoU as 1
            else:
                iou = I / float(U)
            iou_tabel[cat,0] += iou
            iou_tabel[cat,1] += 1
            iou_list.append(iou)
    return iou_tabel,iou_list

def compute_overall_iou(pred, target, num_classes):
    shape_ious = []
    pred_np = pred.cpu().data.numpy()
    target_np = target.cpu().data.numpy()
    for shape_idx in range(pred.size(0)):
        part_ious = []
        for part in range(num_classes):
            I = np.sum(np.logical_and(pred_np[shape_idx].max(1) == part, target_np[shape_idx] == part))
            U = np.sum(np.logical_or(pred_np[shape_idx].max(1) == part, target_np[shape_idx] == part))
            if U == 0:
                iou = 1 #If the union of groundtruth and prediction points is empty, then count part IoU as 1
            else:
                iou = I / float(U)
            part_ious.append(iou)
        shape_ious.append(np.mean(part_ious))
    return shape_ious

def test_semseg(model, loader, num_classes = 8, gpu=True, generate_ply=False):
    '''
    Input
    :param model:
    :param loader:
    :param num_classes:
    :param pointnet2:
    Output
    metrics: metrics['accuracy']-> overall accuracy
             metrics['iou']-> mean Iou
    hist_acc: history of accuracy
    cat_iou: IoU for o category
    '''
    iou_tabel = np.zeros((num_classes,3))
    metrics = defaultdict(lambda:list())
    hist_acc = []
    for batch_id, (index, points, label_face, label_face_onehot, name, raw_points_face) in tqdm(enumerate(loader), total=len(loader), smoothing=0.9):
        batchsize, num_point, _ = points.size()
        points_face = raw_points_face[0].numpy()
        index_face = index[0].numpy()
        coordinate = points.transpose(2,1)
        normal = points[:, :, 12:]
        centre = points[:, :, 9:12]
        label_face = label_face[:, :, 0]

        coordinate, label_face, centre = Variable(coordinate.float()), Variable(label_face.long()), Variable(centre.float())
        coordinate, label_face, centre = coordinate.cuda(), label_face.cuda(), centre.cuda()

        with torch.no_grad():
               pred = model(coordinate)

        iou_tabel, iou_list = compute_cat_iou(pred,label_face,iou_tabel)
        pred = pred.contiguous().view(-1, num_classes)
        label_face = label_face.view(-1, 1)[:, 0]
        pred_choice = pred.data.max(1)[1]
        correct = pred_choice.eq(label_face.data).cpu().sum()
        metrics['accuracy'].append(correct.item()/ (batchsize * num_point))
        label_face = pred_choice.cpu().reshape(pred_choice.shape[0], 1)
        if generate_ply:
               #label_face=label_optimization(index_face, label_face)
               generate_plyfile(index_face, points_face, label_face, path_in="output/output.ply", path_out="output/output_1.ply")
    iou_tabel[:,2] = iou_tabel[:,0] /iou_tabel[:,1]
    hist_acc += metrics['accuracy']
    metrics['accuracy'] = np.mean(metrics['accuracy'])
    metrics['iou'] = np.mean(iou_tabel[:, 2])
    iou_tabel = pd.DataFrame(iou_tabel,columns=['iou','count','mean_iou'])
    iou_tabel['Category_IOU'] = ["label%d"%(i) for i in range(num_classes)]
    cat_iou = iou_tabel.groupby('Category_IOU')['mean_iou'].mean()
    mIoU = np.mean(cat_iou)

    return metrics, mIoU, cat_iou

def labels_change_color(color_label):
    if color_label.item()==0:
        return [255, 255, 255]
    elif color_label.item()==1:
        return [255, 0, 0]
    elif color_label.item()==2:
        return [255, 125, 0]
    elif color_label.item()==3:
        return [255, 255, 0]
    elif color_label.item()==4:
        return [0, 255, 0]
    elif color_label.item()==5:
        return [0, 255, 255]
    elif color_label.item()==6:
        return [0, 0, 255]
    elif color_label.item()==7:
        return [255, 0, 255]
    else:
        return [0, 0, 0]
    
def generate_plyfile(index_face, point_face, label_face, path_in, path_out):
    """
    Input:
        index_face: index of points in a face [N, 3]
        points_face: 3 points coordinate in a face + 1 center point coordinate [N, 12]
        label_face: label of face [N, 1]
        path_in: path to input PLY file
        path_out: path to save new generated ply file
    Return:
    """    
    with open(path_in, "r") as f:
        with open(path_out, "w") as g:
            # copy all lines from path_in to path_out
            for line in f:
                g.write(line)

            # append new data at the end of path_out
            g.write("\n")        
            for i in range(len(label_face)):  # write new point index for every face
                RGB = labels_change_color(label_face[i])  # Get RGB value according to face label
                g.write(str(3) + " " + str(index_face[i][0]) + " " + str(index_face[i][1]) + " "
                        + str(index_face[i][2]) + " " + str(RGB[0]) + " " + str(RGB[1]) + " "
                        + str(RGB[2]) + " " + str(255) + "\n")

            g.close()
        f.close()










