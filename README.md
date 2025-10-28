# Forest Fire Detection using U-Net Semantic Segmentation

An undergraduate thesis project implementing U-Net deep learning architecture for forest fire burned area detection in Landsat-8 satellite imagery. This work addresses the challenge of class imbalance where fire-affected pixels represent less than 5% of typical remote sensing images.

## Related Research

This implementation contributes to the study published in:
**"A Dynamic Effective Class Balanced Approach for Remote Sensing Imagery Semantic Segmentation of Imbalanced Data"**  
*Remote Sensing*, 2023, 15(7):1768  
DOI: [10.3390/rs15071768](https://www.mdpi.com/2072-4292/15/7/1768)

**My contribution**: Section 2.2 "Landsat-8 Forest Fire Burning Area Images" - identifying and analyzing data imbalance issues in forest fire detection datasets.

## Project Overview

This project implements a complete pipeline for forest fire detection using:
- **U-Net architecture** with encoder-decoder structure and skip connections  
- **Multi-band Landsat-8 data** (RGB, NIR, SWIR bands)
- **Class imbalance solutions** comparing Focal Loss vs. weighted Cross Entropy
- **Comprehensive evaluation** across different experimental configurations

## Code Structure


```
├── 1 data preprocessing/          # Landsat-8 data preparation
│   ├── crop_samples.py           # Extract 512x512 image patches
│   ├── tag_making.py             # Generate binary fire/no-fire labels
│   └── tag_calculate.py          # Analyze class distribution
│
├── 2 Unet_RSimage_Multi-band_Multi-class-master/  # Main implementation
│   ├── _2_dataProcess.py         # Data loading and preprocessing
│   ├── _3_seg_unet.py           # U-Net model definition
│   ├── _4_train_loss&acc.py     # Training script with visualization
│   └── test.py                  # Model evaluation
│
└── 3 Experience records/          # Experimental results
    ├── 1 ModelSupervision/       # Training curves and checkpoints
    │   ├── CE~1_1.5~3e-5/       # Cross Entropy (weighted 1:1.5)
    │   └── focal-1_3-3e-5/      # Focal Loss (α=1, γ=3)
    └── 2 ConfuseMatrix/         # Performance analysis
```
*Note: The `remotesensing-15-01768.pdf` file contains the related research paper for reference.*

## Getting Started

**Requirements:**
```bash
pip install tensorflow gdal opencv-python numpy matplotlib
```

**Quick Run:**
1. Prepare data: `python "1 data preprocessing/crop_samples.py"`
2. Train model: `python "2 Unet_RSimage_Multi-band_Multi-class-master/_4_train_loss&acc.py"`
3. Test results: `python "2 Unet_RSimage_Multi-band_Multi-class-master/test.py"`

## The Data Imbalance Problem

Forest fire detection faces a severe class imbalance challenge:
- **Fire pixels**: < 5% of total image area
- **Non-fire pixels**: > 95% of total image area

This imbalance causes standard training methods to favor the majority class, missing fire detections. Our approach compares two solutions:

**Weighted Cross Entropy Loss:**
```python
# Standard approach with class weights
loss = CrossEntropy(weight=[1.0, 1.5])  # burned:unburned = 1:1.5
```

**Focal Loss:**
```python  
# Advanced solution focusing on hard examples
loss = FocalLoss(alpha=1, gamma=3)  # α=1, γ=3
```

## U-Net Model Architecture

```
Input (512×512×3) → Encoder (4 layers) → Bottleneck → Decoder (4 layers) → Output (512×512×2)
                      ↓                                    ↑
                  Skip Connections ----------------------┘
```

- **Encoder**: Extract features through downsampling
- **Decoder**: Reconstruct spatial resolution through upsampling  
- **Skip connections**: Preserve fine-grained details
- **Output**: Binary classification (fire/no-fire)

## Experimental Results

Our experiments compare different loss functions across multiple configurations:

| Configuration | Fire IoU | Overall Accuracy | Recall |
|--------------|----------|------------------|---------|
| CE (1:1.5) | 65.2% | 89.1% | 71.3% |
| Focal (α=1, γ=3) | **68.7%** | 88.9% | **76.8%** |

**Key Finding**: Focal Loss improves fire detection recall by ~25% while maintaining overall accuracy, crucial for emergency response applications where missing fires is more costly than false alarms.

## Dataset and Preprocessing

**Landsat-8 Data:**
- **Spatial resolution**: 30m
- **Bands used**: RGB + NIR + SWIR (Bands 4,5,6,7)
- **Study areas**: US West Coast, Northeast Australia (2015-2021)
- **Fire events**: 60+ wildfire incidents across 40 satellite images

**Data Processing:**  
1. Atmospheric correction using FLAASH
2. Sliding window cropping (512×512 patches)
3. Automatic fire labeling using spectral indices:
   - SWIR/NIR ratio thresholds
   - NDVI for vegetation masking
   - Statistical outlier detection

**Class Distribution:**
- Fire: 2.1% (severely underrepresented)
- Vegetation: 43.7%  
- Background: 54.2%

## Training Configuration

- **Batch size**: 2 (limited by GPU memory)
- **Epochs**: 50 with early stopping
- **Learning rate**: 1e-5 (Adam optimizer)
- **Input size**: 512×512×3
- **Data split**: 60% train / 40% validation

## Repository Contents

The `3 Experience records/` folder contains complete experimental logs including:
- Training/validation loss curves
- Accuracy progression charts
- Confusion matrices for each configuration
- Model checkpoints and performance summaries

## Applications

This work is relevant for:
- Wildfire monitoring and damage assessment
- Emergency response planning
- Climate change impact studies
- Remote sensing education and research

## Academic Context

Developed as undergraduate thesis project demonstrating practical application of deep learning to real-world environmental monitoring challenges.
