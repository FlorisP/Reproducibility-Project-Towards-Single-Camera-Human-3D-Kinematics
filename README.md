# Group 95: Reproducibility Project Towards Single Camera Human 3D-Kinematics (WORK-IN-PROGRESS)

## Course Info

CS4240 Deep Learning (2022/2023 Q3)  
TU Delft

Supervisor:  
Xucong Zhang, xucong.zhang@tudelft.nl 

Students:  
Farhad Azimzade 4788206, F.Azimzade@student.tudelft.nl  
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

Results to reproduce: Augment the testing data to check for robustness of the model

This blog aims to reproduce the deep learning research by Bittner, M., et al. (2023) on markerless estimation of 3D Kinematics (3DKE). 3D human kinematics relates to measuring joint angles between different parts of the human body. These joint angles are vital for professional physicians to give precise advice to, for example, athletes to perform better in their respective sport. This information can also aid in diagnosing neurodegenerative diseases more efficiently. Accurately analysing joint angles of a subject requires extensive training of the human evaluator, as it involves fine distinctions in the visual erception of the subject, as well as some expert knowledge. As such, efforts have been made in automating the process of such kinematics analysis.

One such approach is the multi-step 3D kinematics, whereby [add short description of the method]. Applied to a dataset of videos of various human subjects, the multi-step approach has already been shown to be highly performant in the estimation of human kinematics.

In the paper by Bittner et al., an alternative to the multi-step approach for human kinematics is presented, which involves direct application of Deep Learning in an end-to-end fashion on the video dataset to estimate human kinematics. The algorithm presented in this paper shows great potential for usage in combination with mobile phones, and has been shown to be an improved approach compared to the multi-step approach. 

The algorithm presented in this paper uses deep learning algorithm which directly learns from a video to joint angles and scales using deep neural networks. 


## Theory
The method presented in this paper, simplified, goes as follows: it takes videos from a single camera as input and directly estimates joint angles. This is done by using a convolutional neural network (CNN) for each individual frame for instantaneous kinematic estimations, and then using a sequential neural network with temporal relations to relate the instantaneous kinematic estimations with the temporal relations of the frames to refine the output. The general method is shown in the following image: 

![image](https://user-images.githubusercontent.com/90697657/231532244-a248c755-4e45-47dc-8c8c-24591de86579.png)

A standard pre-trained ResNeXt-50 is used as the convolutional backbone, with three different sequential networks tested. These sequential networks are LSTM, TCN and a Transformer. 

The overall objective function is 

$$
L = \lambda_1L_{joint} + \lambda_2L_{marker} + \lambda_3L_{body} + \lambda_4L_{angle}
$$,

with $\lambda_1$, $\lambda_2$, $\lambda_3$, $\lambda_4$ as weights of the losses. 

The training requirements are the joint angle and the scales of individual bones, a rotation matrix of the pelvis to the ground as well as the marker positions corresponding to them. Joint angles are generated using the OpenSim software. The resulting ground truth values are the calculated joint angles, the scaling factors and the virtual marker positions.

The ResNetXt algorithm used has the following hyperparameters: 
 - Adam optimizer with weight decay of 0.001
 - Batch size = 64
 - Learning rate = exponentially decays in two steps from 5 × 10−4 to 3.33 × 10−5 over 28 epochs and from 3.33 × 10−6 to 10−6 over 2 epochs

The sequential and convolutional networks have lambda values of:
 - $\lambda_1$ = 1.0
 - $\lambda_2$ = 2.0
 - $\lambda_3$ = 0.1
 - $\lambda_4$ = 0.06

These values were determined experimentally by the authors of the paper.

## Installation
### Requirements
Installation requirements to run the algorithm presented by the paper are the following:

 - Python 3.8.0 
 - PyTorch 1.11.0
 - OpenSim 4.3+        

The authors of the paper created an environment file with the necessary libraries to install. 

## Dataset
The 3DKE algorithm was trained and tested on the BML-MoVi Database (https://www.biomotionlab.ca/movi/). The database coontains 90 actors performing 20 different kind of everyday movements, and also a random movement. The motions of the actor's body parts were captured using inertial measurement units, combined with a Qualisys optical motion capture system (https://www.qualisys.com/). Two camera mounting positions are used, PG1 and PG2. The camera view captured by PG1 is the frontal- and PG2 as the sagittal camera view. The ground truth virtual markers were generated by the 3D mesh representations of the Qualisys data that is provided in the AMASS dataset. AMASS is a large database of human motion unifying different optical marker-based motion capture datasets by representing them within a common framework and parameterization. AMASS is readily useful for animation, visualization, and generating training data for deep learning (https://amass.is.tue.mpg.de/). 


## Method
The reproduction project was aimed at exploring the robustness of the D3KE method to input data augmentation. In particular, we would like to evaluate the performance of the D3KE algorithm on an augmented testing data set.

Data augmentation we considered were flipping, resizing, cropping, altering the brightness, changing the contrast of the frames in the input videos. Such augmentation is usually applied to the training set, as part of inducing robustness toward certain changes of the input. In fact, augmentation of the training data was performed in the training of the original D3KE model, as is stated in the paper.

Data augmentation can also allow the training dataset to effectively increase in size. When applied to images, a mirrored image of a cat is still a cat. Applying mirroring to videos of people, however, changes things when the model is created of the person in the video. A mirrored video of someone moving their left arm will show someone moving their right arm. Augmenting the test set and thereby creating 'new' testing data will exploit several aspects of the algorithm.

Testing the algorithm will give insights into its generalisability. A previous study, by Recht B. et al. has shown that presenting different ImageNet classifiers with new but comparable testing data, decreases the accuracy, indicating that the test set has been used too much to develop the algorithm. 

This study will aim to do something similar, but with videos. By presenting augmented versions of the original test set, the algorithm's generalisability will be explored. 

## Problems Encountered

### Issues with Cloud Computing:

Given that the original research project made extensive use of GPUs for developing the model, deploying GPUs for the reproduction appeared to be a reasonable step. In order to achieve this, a popular cloud computing platform, Google Cloud, was decided upon. The general plan involved running a virtual machine with access to GPUs on the cloud to augment the data and re-test the model on the augmented data. However, there have certain roadblocks we have run into with respect to this approach.

Firstly, the allocation of physical resources on Google Cloud turned out to be more challenging than expected. It has taken a while to arrive at a server that met the needs, despite our requirements being relatively limited.

Secondly, there have been issues when attempting to build the project on the cloud virtual machien instance. In particular, certain packages prescribed in the conda environment file could not be installed by conda.
- installing the necessary software (conda env, opensim, etc.)

### Issues with Data Preparation:

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
