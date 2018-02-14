# Author: Antonin Jousson
# coding: utf-8

from verify import run_simulation, load_config
#import scipy.optimize
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

def compute_match_scores(results, threshold):
	match_scores = [1 if raw_score >= threshold else 0 for raw_score in results.scores]
	return match_scores

def compute_FNMR(match_scores):
	FNMR = 100-compute_FMR(match_scores)
	return FNMR

def compute_FMR(match_scores):
	FMR = (float(sum(match_scores))/(len(match_scores)))*100
	return FMR

if __name__=="__main__":
	config = load_config()
	db = config["db"]

	#genuine_results = run_simulation(matcher, db, True)
	#fraud_results = run_simulation(matcher, db, False)
	genuine_results = pd.read_csv("results/results_{}_genuine.csv".format(db),sep='\t', index_col = 0)
	fraud_results = pd.read_csv("results/results_{}_fraud.csv".format(db),sep='\t', index_col = 0)

	thresholds = [round(thresh,2) for thresh in np.arange(0.0, 1.01, 0.01)]
	FNMR_rates= []
	FMR_rates= []
	for threshold in thresholds:
		match_scores = [compute_match_scores(results,threshold) for results in [genuine_results,fraud_results]]
		FNMR_rates.append(compute_FNMR(match_scores[0]))
		FMR_rates.append(compute_FMR(match_scores[1]))

	df = pd.DataFrame({"threshold":thresholds,"FNMR":FNMR_rates,"FMR":FMR_rates})

	ax_1 = df.plot(x="threshold",y =["FMR","FNMR"], kind='line', grid = True)
	fig_1 = ax_1.get_figure()
	fig_1.savefig('results/performance_{}.png'.format(db))

	poly_1 = np.polyfit(df.threshold, df.FMR, deg = 2)
	poly_2 = np.polyfit(df.threshold, df.FNMR, deg = 2)

	df["FMR_fitted"]  = np.polyval(poly_1, df.threshold)
	df["FNMR_fitted"]  = np.polyval(poly_2, df.threshold)

	ax_2 = df.plot(x="threshold",y =["FMR_fitted","FNMR_fitted"], kind='line', grid = True)
	#plt.scatter(0.635, 35.5, marker='x', s=80, zorder=5, linewidth=1.5, color='black')
	fig_2 = ax_2.get_figure()
	fig_2.savefig('results/performance_{}_fitted.png'.format(db))


