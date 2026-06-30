import numpy as np


def voters_from_csv(file_path: str):
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
        return []

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
    return voters

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


def voters_avg(voters: list):
    '''
    deviding and average scores in voters groups
    '''
    groups = group(voters)
    averaged_groups = []

    for g in groups:
        cand_sums = {}
        cand_counts = {}
        
        # Accumulate total scores and vote counts for each candidate
        for voter in g:
            for cand, score in voter.items():
                cand_sums[cand] = cand_sums.get(cand, 0) + score
                cand_counts[cand] = cand_counts.get(cand, 0) + 1
                
        # Compute the average score per candidate in the current group
        group_avg = {cand: cand_sums[cand] / cand_counts[cand] for cand in cand_sums}
        averaged_groups.append(group_avg)

    return averaged_groups
        


def group(voters: list):
    '''
    Return a set of lists, a list for every group of voters that vote the same cands.
    '''
    groups = []
    
    for voter in voters:
        voter_cands = set(voter.keys())
        
        # Isolated voters (empty ballots) get their own group
        if not voter_cands:
            groups.append((set(), [voter]))
            continue
            
        merged_cands = set(voter_cands)
        merged_voters = [voter]

        # Updated "groups"
        unrelated_groups = []
        
        # For every group, if it's disjoint of the current cands, it added as is to related_groups.
        # Else, we merge it with current voter and add both afterwards.
        for group_cands, group_voters in groups:
            # If there's an intersection in candidates, merge the groups
            if not voter_cands.isdisjoint(group_cands):
                merged_cands |= group_cands
                merged_voters.extend(group_voters)
            else:
                unrelated_groups.append((group_cands, group_voters))
                
        # Add the newly merged group
        unrelated_groups.append((merged_cands, merged_voters))
        groups = unrelated_groups
        
    # Extract only the lists of voters from the internal structure
    return [g_voters for _, g_voters in groups]