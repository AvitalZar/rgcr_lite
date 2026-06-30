'''
Tests took from the test in pref_voting for the original method.
'''

#from pref_voting.stochastic_methods import RGCR
from pref_voting.grade_profiles import GradeProfile
from rgcr_lite.rgcr_methods import *
from rgcr_lite.helpers import *
import networkx as nx
import pytest
import numpy as np
import logging

logging.getLogger("RGCR").setLevel(logging.NOTSET)
logging.getLogger("test").setLevel(logging.INFO)

def random_ordinal_ranking(gprofile:GradeProfile, curr_cands=None):
	x = gprofile.to_ranking_profile().majority_graph().to_networkx()
	return list(nx.topological_sort(x))

def mean_estimator(gprofile:GradeProfile, curr_cands=None):
	if curr_cands is None:
		curr_cands = gprofile.candidates
	return sorted(curr_cands, key=lambda c: gprofile.avg(c) if gprofile.has_grade(c) else 0, reverse=True)

def median_estimator(gprofile:GradeProfile, curr_cands=None):
	if curr_cands is None:
		curr_cands = gprofile.candidates
	return sorted(curr_cands, key=lambda c: gprofile.median(c) if gprofile.has_grade(c) else 0, reverse=True)


logger = logging.getLogger("test")

def is_topological_order(profile, ranking):
	G = profile.to_ranking_profile().majority_graph().to_networkx()
	if len(ranking) != len(G.nodes) or set(ranking) != set(G.nodes):
		logger.error("is_top_ord: Ranking does not contain the same candidates as the graph. len(ranking)=%g, len(G.nodes)=%g", len(ranking), len(G.nodes))
		logger.error("is_top_ord: Ranking candidates: %s, all candidates: %s", ranking, list(G.nodes))
		return False
		
	# שמירת המיקום של כל צומת ברשימה
	index_map = {node: i for i, node in enumerate(ranking)}
	
	# בדיקה שעבור כל קשת, צומת המקור מופיע לפני צומת היעד
	for u, v in G.edges():
		if index_map[u] > index_map[v]:
			logger.error("is_top_ord: Edge (%s, %s) violates the topological order.", u, v)
			return False
	logger.info("is_top_ord: Ranking is a valid topological order.")
	return True


def test_topological_order():
	for i in range(1,100,10):
		n = np.random.rand() * 5*i
		voters = create_random_voters_list(num_of_voters=int(n),num_of_cands=i)
		scores = list({value for v in voters for value in v.values()})
		gprofile = GradeProfile(voters, list(scores))
		logger.info("Test topological order with %g candidates and %g voters", i, int(n))
		ranking = RGCR(voters)
		assert is_topological_order(gprofile, ranking)

@pytest.mark.parametrize("voters, expected_sol, expected_prob", [
	([{1: 7}, {2: 3}], [1, 2], 0.9),
	([{1: 4, 2: 8}, {2: 6, 3: 2}], [2, 1, 3], 5/6),
	([{1: 3, 2: 4, 5: 5}, {1: 5, 3: 6}, {4: 2, 5: 10}, {2: 7, 6: 10}], [6,5,4,3,2,1], 7/198)
])
def test_probability(voters, expected_sol, expected_prob): #test approximation to the probability, only for small inputs.
	prob = 0
	trials = 10000
	for _ in range(trials):
		solution = RGCR(voters)
		if solution == expected_sol:
			prob += 1
	assert abs(prob/trials - expected_prob) < 0.05


@pytest.mark.parametrize("estimator", [random_ordinal_ranking, mean_estimator, median_estimator])
def test_strict_uniform_dominance(estimator):
	rgcr_success = 0
	another_estimator_success = 0
	trials = 1000
	for i in range(1, trials):
		voters_num = 10
		items = np.random.randint(voters_num, voters_num*3)
		cands_list = list(range(items))
		voters_list = create_random_voters_list(num_of_voters=voters_num, num_of_cands=items)
		scores = list({value for v in voters_list for value in v.values()})
		gprofile = GradeProfile(voters_list, list(scores), candidates=cands_list)
		rgcr_ranking = RGCR(voters_list, curr_cands=cands_list)
		another_ranking = estimator(gprofile)
		if rgcr_ranking == cands_list[::-1]: # the true order is always 0 < 1 < ...
			logger.info("RGCR found the true order in trial %g", i)
			rgcr_success += 1
		else:
			if i % 100 == 0: # log only every 100 trials to avoid cluttering the logs
				logger.debug("RGCR did not find the true order in trial %g. RGCR ranking: %s", i, rgcr_ranking)
		if another_ranking == cands_list[::-1]:
			logger.info("Another estimator found the true order in trial %g", i)
			another_estimator_success += 1
		else:
			if i % 100 == 0: # log only every 100 trials to avoid cluttering the logs
				logger.debug("Another estimator did not find the true order in trial %g. Another ranking: %s", i, another_ranking)
	assert rgcr_success > another_estimator_success


@pytest.mark.parametrize("file", ["voterss.csv"])
def test_rgcr_from_csv(file):
	assert rgcr_from_csv(file) == ['c','b','a']