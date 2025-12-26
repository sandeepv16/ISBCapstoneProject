# Steel Pipe Detection Experiments

## 1. Overview
This document outlines our experiments in training custom object detection models using RTMDet, YOLOv11, and YOLO-NAS frameworks. It details the dataset preparation, training procedures, evaluation metrics, and deployment-ready results.

## 2. Dataset Configuration

### 2.1 Dataset Details
The dataset used for these experiments consists of images and annotations organized for training, validation, and testing. It includes four object classes: `c` (Circle), `h` (Hexagon), `s1` (Square), and `s2` (Rectangle). The dataset is sourced from Roboflow under the project "pim-2chly" (version 14) and adheres to the YOLO annotation format.

### 2.2 Directory Structure
The dataset is organized as follows:
Dataset/
    - ├── train/  
        - ├── images/ 
        - ├── labels/ 
    - ├── val/ │ 
        - ├── images/  
        - ├── labels/ 
    - ├── test/ 
        - ├── images/
        - ├── labels/


Each image file has a corresponding label file (in YOLO format) specifying bounding box coordinates and class labels.

## 3. Training Notebooks

### 3.1 RTMDet Notebook
The RTMDet notebook leverages the MMDetection framework. It includes:
- **Dataset Configuration:** Setting up the dataset paths and annotation format.
- **Hyperparameter Tuning:** Customizing the training pipeline for optimal performance.
- **Training:** Leveraging pre-trained weights for faster convergence.

### 3.2 YOLOv11 Notebook
The YOLOv11 notebook employs the Ultralytics framework, focusing on:
- **Efficient dataset integration** through YAML configuration.
- **Fine-tuning** the YOLOv11 pre-trained model on the custom dataset.
- **Monitoring metrics** such as loss and mean average precision (mAP).

### 3.3 YOLO-NAS Notebook
The YOLO-NAS notebook integrates YOLO-NAS, a modern and scalable framework, and focuses on:
- **Efficient training** with adaptive learning rate schedulers.
- **Utilizing enhanced latency optimization** for real-time applications.
- **Tracking key metrics,** including inference speed and model size.

## 4. Environment Setup

### 4.1 Dependencies
To replicate the experiments, ensure the following libraries and tools are installed:
- **PyTorch** >= 1.8
- **MMDetection** for RTMDet
- **Ultralytics** for YOLOv11
- **YOLO-NAS library**

### 4.2 System Configuration
- **Tesla T4 GPU** (Google Colab) for accelerated training.
- Verified dataset paths and permissions.
- Installed dependencies using `pip` and `conda`.

## 5. Training Procedures

### 5.1 RTMDet Training
1. Load and configure dataset paths for training and validation.
2. Define hyperparameters, including:
   - **Epochs:** 50
   - **Batch Size:** 2, 4, 8, 16
   - **Learning Rate:** 0.001
3. Start training using the MMDetection framework.
4. Track mAP and training loss.

### 5.2 YOLOv11 Training
1. Configure the dataset using a YAML file.
2. Load the pre-trained YOLOv11 model.
3. Fine-tune the model with:
   - **Epochs:** 100
   - **Learning Rate:** 0.001
   - **Batch Size:** 8, 16, 32
4. Track mAP and training loss.

### 5.3 YOLO-NAS Training
1. Integrate the dataset and configure the YOLO-NAS pipeline.
2. Train with adaptive learning rate schedulers.
3. Fine-tune the model with:
   - **Epochs:** 50
   - **Learning Rate:** 0.001
   - **Batch Size:** 2, 4, 6
4. Track mAP and training loss.

## 6. Results
- **RTMDet** achieved robust performance with mAP(50-95) of 10-20%.
- **YOLOv11** demonstrated strong generalization, reaching an mAP(50-95) of 45-50%.
- **YOLO-NAS** excelled in inference speed, achieving an mAP(50-95) of 10-20% with minimal latency.
