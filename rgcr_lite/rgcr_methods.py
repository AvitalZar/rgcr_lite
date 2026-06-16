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

def rgcr_from_csv(file_path: str, w=(lambda x: x/(1+x)), curr_cands=None) -> list:
    import csv

    with open(file_path, mode='r', encoding='utf-8') as infile:
        sample = infile.read(1024)
        infile.seek(0)

        try:
            dialect = csv.Sniffer().sniff(sample)
            reader = csv.reader(infile, dialect)
        except csv.Error:
            reader = csv.reader(infile)

        rows = list(reader)

    if not rows:
        return RGCR([], w=w, curr_cands=curr_cands)

    # First row is header: empty cell, then reviewer names
    reviewer_names = [col.strip() for col in rows[0][1:]]
    num_reviewers = len(reviewer_names)

    # Build a dict per reviewer: {item: score}
    reviewer_votes = [{} for _ in range(num_reviewers)]

    for row in rows[1:]:
        if not row:
            continue
        item = row[0].strip()
        if not item:
            continue

        for i, score_str in enumerate(row[1:num_reviewers + 1]):
            score_str = score_str.strip()
            if not score_str:
                continue
            try:
                score = float(score_str)
                reviewer_votes[i][item] = int(score) if score.is_integer() else score
            except ValueError:
                continue

    # Drop reviewers who gave no scores
    voters = [rv for rv in reviewer_votes if rv]

    print(voters)
    return RGCR(voters, w=w, curr_cands=curr_cands)