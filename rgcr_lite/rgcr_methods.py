'''
An easier function for the rgcr function, make it unecessary to use pref-voting objects.
'''
from pref_voting.grade_profiles import GradeProfile
from pref_voting.stochastic_methods import RGCR as rgcr_original
from .helpers import voters_avg, voters_from_csv


def RGCR(voters:list, w=(lambda x: x/(1+x)), curr_cands=None)->list:
	#The major function: Get only essential input and run rgcr on it.
	scores = {value for v in voters for value in v.values()}
	gprofile = GradeProfile(voters, list(scores), candidates=curr_cands)
	return rgcr_original(gprofile, w=w, curr_cands=curr_cands)



def rgcr_from_csv(file_path: str, w=(lambda x: x/(1+x)), curr_cands=None) -> list:
    voters = voters_from_csv(file_path)

    return RGCR(voters, w=w, curr_cands=curr_cands)


def rgcr_avg(voters: list, w=(lambda x: x/(1+x))):
    '''
    This function suppose to solve the problem of the assumption of the original algo
    that there are no cycles in the voting. The method is to devide the voters into groups
    such that there's no candidate that appear in two groups, then compute an average score
    on the cands in every group and run the original algo on it. It isn't efficient as the
    original but work on cycled input.
    '''
    return RGCR(voters_avg(voters), w)

def rgcr_avg_from_csv(file_path: str):
    voters = voters_from_csv(file_path)
    return rgcr_avg(voters)


def rgcr_tuples(voters:list, w=(lambda x: x/(1+x))):
    pass