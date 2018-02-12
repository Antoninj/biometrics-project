# Biometrics project description

The goal is to develop a fingerprint recognition biometric system relying on fingerprint spatial characteristics and carry out a thorough performance evaluation in verification mode.

## Preprocessing

A few preprocessing techniques will be applied to the fingerprint images using the [skimage](http://scikit-image.org) image processing library. More precisely, the preprocessing workflow consists of the following steps :

- Intensity scaling
- Contrast enhancement
- Contrast Limited Adaptive Histogram Equalization
- Gauss smoothing
- Binarization using dynamic thresholding
- Thinning

## Feature extraction algorithm

The feature extraction algorithm used for our fingerprint recognition system will be based on the very common crossing number technique (see the course slides for more details on how the algorithm works)

Our source code is similar to the implementation available on the following [GitHub] with the difference that we will use skimage instead of the PIL library.

A postprocessing algorithm building upon the crossing number technique is used to remove false positives in order to increase the matching algorithm performances.

## Matching algorithm

The point matching algorithm relies on the fingerprints spatial characteristics and uses relatives distances between a singular core point and the minutiae features. More specifically, we will implement the approach described in this [paper][1].

## Performance evaluation

We will assess the perfomance of our system in verification mode using the single template configuration.

##  Dataset

Our dataset consits of 128 png fingerprint scans that can be found [here][dataset].

## Sources

- [Paper 1][1]

- [Dataset][dataset]

- [GitHub]

[GitHub]:https://github.com/rtshadow/
[1]:http://www.iaeng.org/publication/WCE2014/WCE2014_pp466-474.pdf
[dataset]:http://www.advancedsourcecode.com/fingerprintdatabase.asp
