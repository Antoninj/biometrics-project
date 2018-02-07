# Biometrics project description

The goal is to develop a fingerprint recognition biometric system relying on fingerprint spatial characteristics and carry out a thorough performance evaluation in verification mode.

## Preprocessing

A few preprocessing techniques will be applied to the fingerprint images using the [skimage](http://scikit-image.org) image processing library. More precisely, the preprocessing workflow consists of the following steps :

- Intensity scaling
- Contrast Limited Adaptive Histogram Equalization
- Contrast enhancement
- Gauss smoothing
- Binarization using dynamic thresholding
- Thining

## Feature extraction algorithm

The feature extraction algorithm used for our fingerprint recognition system will be based on the very common crossing number technique (see [1] for more details)

Our source code is similar to the implementation available on the following [GitHub repository](https://github.com/rtshadow/biometrics) with the difference that we will use skimage instead of the PIL library.

A postprocessing algorithm is used to remove false positives in order to increase the matching algorithm performances.

## Matching algorithm

The point matching algorithm relies on the fingerprints spatial characteristics and uses relatives distances between a singular core point and the previously extracted minutiae features. More specifically, we will implement the approach described in [2].

## Performance evaluation

We will assess the perfomance of our system in verification mode using a singe template configuration.

##  Datasets

Our dataset can be found [here](http://www.advancedsourcecode.com/fingerprintdatabase.asp).

## Sources

- [Paper 1][1]

- [Paper 2][2]

[2]:(http://www.iaeng.org/publication/WCE2014/WCE2014_pp466-474.pdf)
[1]:(https://ai2-s2-pdfs.s3.amazonaws.com/b17d/ccc16dc4638ed1a019a6b87a731bd56a069d.pdf)
