'''
An easier function for the rgcr function, make it unecessary to use pref-voting objects.
'''
from pref_voting.grade_profiles import GradeProfile
from pref_voting.stochastic_methods import RGCR as rgcr_original
import numpy as np


def RGCR(voters:list, w=(lambda x: x/(1+x)), curr_cands=None)->list:
	#The major function: Get only essential input and run rgcr on it.
	scores = {value for v in voters for value in v.values()}
	gprofile = GradeProfile(voters, list(scores), candidates=curr_cands)
	return rgcr_original(gprofile, w=w, curr_cands=curr_cands)


def create_random_voters_list(num_of_voters=5, num_of_cands=20, reviewing_prob=0.3, seed=None):
	np.random.seed(seed)
	candidates = list(range(num_of_cands))
	voters = []
	for _ in range(num_of_voters):
		voter = {}
		val = 0
		for c in candidates:
			if np.random.rand() < reviewing_prob:
				voter[c] = val + np.random.randint(0, 10)+1
				val = voter[c]
		voters.append(voter)
#	logger.debug("Created random legal graph with %s", voters)
	return voters


import csv

def rgcr_from_csv(file_path: str, w=(lambda x: x/(1+x)), curr_cands=None) -> list:
	voters = []
	
	with open(file_path, mode='r', encoding='utf-8') as infile:

		sample = infile.read(1024)
		infile.seek(0)

		try:
			dialect = csv.Sniffer().sniff(sample)
			reader = csv.reader(infile, dialect)
		except csv.Error:
			reader = csv.reader(infile)
		
		for row_num, row in enumerate(reader, 1):
			voter_votes = {}
			print(f"Row {row_num}: {row} (Length: {len(row)})")
			for i in range(0, len(row), 2):
				if i + 1 < len(row):
					cand = row[i].strip()
					score_str = row[i+1].strip()
					
					if cand and score_str:
						try:
							score = float(score_str)
							voter_votes[cand] = int(score) if score.is_integer() else score
						except ValueError:
							continue
			
			if voter_votes:
				print("appending")
				voters.append(voter_votes)
	
	print(voters)
	return RGCR(voters, w=w, curr_cands=curr_cands)
