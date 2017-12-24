# Biometrics project description 

The goal is to develop a fingerprint recognition biometric system and carry out a thorough performance evaluation in verification mode on 3 (to be confirmed) different datasets.

Eventually and if proven robust enough, the system might be integrated as an alternative ticketing solution into the ROMA ATAC public transportation system.

## Preprocessing 

A few preprocessing steps will be applied to the fingerprint images using the [skimage](http://scikit-image.org) image processing library.
More precisely 4 main preprocessing techniques will be applied in order to enhance the quality of the images :

- Intensity scaling + Contrast Limited Adaptive Histogram Equalization 
- Gauss smoothing
- Binarization using dynamic thresholding
- Thining 

## Feature extraction algorithm

The feature extraction algorithm used for our fingerprint recognition system will be based on the crossing number minutiae extraction technique.

The minutiae extraction algorithm source code will likely be implemented by engineering together some of the code available on the following [GitHub repository](https://github.com/rtshadow/biometrics).

## Matching algorithm 

We will implement a point matching algorithm using the previously extracted minutiae features.

## Performance evaluation

We will assess the perfomance of our system in verification mode using the all-against-all strategy in both single and multi template settings.

##  Datasets

We will use 3 different datasets that can be found [here](http://www.advancedsourcecode.com/fingerprintdatabase.asp).

## Sources

- [Article 1](http://biometrics.cse.msu.edu/Publications/Fingerprint/RossJainReisman_HybridFpMatcher_PR03.pdf)

- [Article 2](https://ai2-s2-pdfs.s3.amazonaws.com/b17d/ccc16dc4638ed1a019a6b87a731bd56a069d.pdf)
