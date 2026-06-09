# rgcr_lite

This repository provides a small, convenient wrapper around the RGCR method (Handling Arbitrary Miscalibrations in Ratings) as implemented following the paper:

Jingyan Wang and Nihar B. Shah, "Handling Arbitrary Miscalibrations in Ratings."

This package is intentionally lightweight and meant to make it easy to run the RGCR algorithm on simple input formats.

Important: this project is not published as a pip-installable package. It requires a full repository install (e.g., clone the repository and install any required dependencies manually). In other words, you cannot install it via pip or a similar one-line package manager command.

Main functionality
- rgcr_wrapper(voters_dict): Accepts a list (or other iterable) of voter objects represented as dictionaries mapping candidate identifiers (strings or ints) to scores. Returns a list of candidate identifiers sorted according to the RGCR output ranking.
- rgcr_from_csv(csv_path): Accepts a CSV file path where each row corresponds to a voter. Each row contains alternating candidate name and score fields, e.g.:
	candidate1_name, candidate1_score, candidate2_name, candidate2_score, ...
	The function parses the CSV, calls rgcr_wrapper on the resulting data, and returns the ranked list of candidates.

Example usage

from rgcr_methods import rgcr_wrapper

# Example voters: voter A gives candidate 1 score 2 and candidate 2 score 6,
# voter B gives candidate 2 score 5 and candidate 3 score 10.
voters = [ {1: 2, 2: 6}, {2: 5, 3: 10} ]
print(rgcr_wrapper(voters))  # expected output: [3, 2, 1]

Testing

You can run the project's unit tests using pytest (after installing pytest and any other required test dependencies manually):

pytest

Web demonstration

A convenient web interface and demonstration of the function is available at: https://avitalzer.csariel.xyz/

License and citation

If you use this code in research, please cite the original paper by Wang and Shah.

Contributions

Contributions and issues are welcome. Please open an issue or pull request in the repository.
