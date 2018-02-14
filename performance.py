# Author: Antonin Jousson
# coding: utf-8

from verify import run_simulation, load_config
from core import match

import argparse
import json
import os
import pandas
import numpy as np
from tqdm import tqdm

def compute_match_scores(results, threshold):
    match_scores = [1 if raw_score >= threshold else 0 for raw_score in results.scores]

def compute_FNMR(match_scores):
    FNMR = 100-compute_FMR(match_scores)
    return FNMR

def compute_FMR(match_scores):
    FMR = (float(sum(match_scores))/(len(match_scores)))*100
    return FMR

if __name__=="__main__":
    config = load_config()
    db = config["db"]

    print("Creating fingerprint matcher...")
    print("Loading template gallery...")
    matcher = match.FingerprintMatcher()
    print("Matching fingerprints...")

    genuine_results = run_simulation(matcher, db, True)
    fraud_results = run_simulation(matcher, db, False)

    FNMR_rates = {}
    FMR_rates = {}
    for threshold in tqdm(np.arange(0.0, 1.0, 0.05)):

        match_scores = [compute_match_scores(results,threshold) for results in [genuine_results,fraud_results]]
        FNMR_rates[threshold] = compute_FNMR(match_scores[0])
        FMR_rates[threshold] = compute_FMR(match_scores[1])

