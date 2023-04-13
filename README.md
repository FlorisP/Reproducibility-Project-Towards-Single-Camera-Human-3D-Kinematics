# Group 95: Reproducibility Project Towards Single Camera Human 3D-Kinematics (WORK-IN-PROGRESS)

## Course Info

CS4240 Deep Learning (2022/2023 Q3)  
TU Delft

Supervisor:  
Xucong Zhang, xucong.zhang@tudelft.nl 

Students:  
Farhad Azimzade ??????, F.Azimzade@student.tudelft.nl  
Adriaan Keurhorst, 4550994, A.F.Keurhorst@student.tudelft.nl  
Floris Pauwels, 4606000, F.Pauwels@student.tudelft.nl


## Table of Contents

- [Towards single camera human 3D-kinematics Sources](#towards-single-camera-human-3d-kinematics-sources)
- [Project Overview](#project-overview)
- [Installation](#installation)
  * [Requirements](#requirements)
- [Problems Encountered](#problems-encountered)
- [Dataset](#dataset)
- [Method](#method)
  * [Models/architecture](#models-architecture)
  * [Preprocessing](#preprocessing)
  * [Training](#training)
- [Results](#results)
- [Conclusion](#conclusion)
- [Criteria](#criteria)
  * [Individual Contribution](#individual-contribution)
- [References](#references)

## Towards single camera human 3D-kinematics Sources
Paper
https://www.mdpi.com/1424-8220/23/1/341

Github
https://github.com/bittnerma/Direct3DKinematicEstimation



## Project Overview
Topics: Biomemenic model, OpenSim, Human Pose

Results to reproduce: Replace the model in the paper to generate new baselines

This blog aims to reproduce the deep learning research by Bittner, M., et al. (2023) about markerless estimation of 3D Kinematics. 3D human kinematics relates to measuring joint angles between different parts of the body. These joint angles are vital for professional physicians to give precise advice to, for example, athletes to perform better in their respective field. To accurately see these joint angles as a human, you need to be well trained to notice small offsets in joint angles between body segments. A multi-step approach, in combination with videos of patients, has already been shown to be very useful in the estimation of human kinematics, but still contain consistent sources of errors. The multi-step approach for human kinematics is challenged in this paper, which suggests that using Deep Learning to estimate human kinematics is a more sensible way to go forward.

The algorithm presented in this paper uses deep learning algorithm which directly learns from a video to joint angles, and scales using deep neural networks. 


## Theory
The method presented in this paper, simplified, goes as follows: it takes videos from a single camera as input and directly estimates joint angles. This is done by using a convolutional neural network (CNN) for each individual frame for instantaneous kinematic estimations, and then using a sequential neural network with temporal relations to relate the instantaneous kinematic estimations with the temporal relations of the frames to refine the output. The general method is shown in the following image: 

![image](https://user-images.githubusercontent.com/90697657/231532244-a248c755-4e45-47dc-8c8c-24591de86579.png)

A standard pre-trained ResNeXt-50 is used as the convolutional backbone, with three different sequential networks tested. These sequential networks are LSTM, TCN and a Transformer. 

The overall objective function is 

L = λ1Ljoint + λ2Lmarker + λ3Lbody + λ4Langle,

with λ1, λ2, λ3, λ4 as weights of the losses. 

The training requirements are the joint angle and the scales of individual bones, a rotation matrix of the pelvis to the ground as well as the marker positions corresponding to them. Joint angles are generated using the OpenSim software. The resulting ground truth values are the calculated joint angles, the scaling factors and the virtual marker positions.

The ResNetXt algorithm used has the following hyperparameters: 
 - Adam optimizer with weight decay of 0.001
 - Batch size = 64
 - Learning rate = exponentially decays in two steps from 5 × 10−4 to 3.33 × 10−5 over 28 epochs and from 3.33 × 10−6 to 10−6 over 2 epochs

The sequential and convolutional networks have lambda values of:
 - λ1 = 1.0
 - λ2 = 2.0
 - λ3 = 0.1
 - λ4 = 0.06

These values were determined experimentally by the authors of the paper.

## Installation
### Requirements
Installation requirements to run the algorithm presented by the paper are the following:

 - Python 3.8.0 
 - PyTorch 1.11.0
 - OpenSim 4.3+        

## Problems Encountered

Problems in the cloud:

Problems during data preparation

## Dataset

## Method
### Models/architecture
### Preprocessing
### Training

## Results

## Conclusion

## Criteria
Replicated: A full implementation from scratch without using any pre-existing code.  
Reproduced: Existing code was evaluated.  
Hyperparams check: Evaluating sensitivity to hyperparameters.  
New data: Evaluating different datasets to obtain similar results.  
New algorithm variant: Evaluating a slightly different variant.  
New code variant: Rewrote or ported existing code to be more efficient/readable.  
Ablation study: Additional ablation studies.  

### Individual Contribution

## References
