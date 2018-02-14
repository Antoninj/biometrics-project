# Author: Antonin Jousson
# coding: utf-8

from core import match
import argparse
import json
import os
import pandas

def load_config():
	with open("config/config.json") as cfg:
		config = json.load(cfg)
	return config

def parse_input_files(db):
	path = "data/test_data/{}".format(db)
	return [path+"/"+filename for filename in os.listdir(path)]

def compute_scores(matcher, filepaths, genuine  ):
	scores = [matcher.verify_identity(path, genuine) for path in filepaths]
	return scores

def run_simulation(matcher, db, genuine):
	input_filepaths = parse_input_files(db)
	raw_scores = compute_scores(matcher, input_filepaths, genuine)
	raw_scores = [round(score,3) for score in raw_scores]
	results = {"scores":raw_scores}
	results = pandas.DataFrame(data = results)
	return results

if __name__=="__main__":
	parser = argparse.ArgumentParser(description = "Script to test the fingerprint recognition system in verification mode")

	config = load_config()
	db = config["db"]

	parser.add_argument("-db", "--database", help = "Test data database", type = str, default = db)
	parser.add_argument("-s", "--save", help = "Save performance metrics", action='store_true')
	parser.add_argument("-i", "--imposter", help = "Input image is genuine or not", action = "store_false", default = True)

	args = parser.parse_args()
	db = args.database
	identity_bool = args.imposter

	print("Creating fingerprint matcher...")
	print("Loading template gallery...")
	matcher = match.FingerprintMatcher()
	print("Matching fingerprints...")
	verification_results = run_simulation(matcher, db, identity_bool)
	print("Matching done !")

	print("Computing performance metrics...")

	if identity_bool:
		identity = "genuine"
	else:
		identity = "fraud"

	if args.save:
		print("Saving results...")
		output_file = "results/results_{}_{}.csv".format(db, identity)
		verification_results.to_csv(output_file, sep='\t', encoding='utf-8')

