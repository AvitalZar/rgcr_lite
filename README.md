# RGCR Wrapper

A simple and convenient Python wrapper for the **RGCR** (Rank-Grounded Calibration for Ratings) method, implemented based on the paper: 
*"Handling Arbitrary Miscalibrations in Ratings"* by Jingyan Wang and Nihar B. Shah. [https://arxiv.org/pdf/1806.05085]

---

> [!IMPORTANT]
> **Manual Installation Required** > This package cannot be installed via `pip` or other package managers. To use it, clone or download this repository directly into your project directory.

---

## Core Functions

The library provides two primary functions:

* **`RGCR(voters_data)`**: Accepts a list of dictionaries representing voters and their ratings, processes the calibration, and returns a ranked list of candidates.
* **`rgcr_from_csv(file_path)`**: Accepts a path to a CSV file where each row represents a voter (formatted as `Candidate Name, score, Candidate Name, score, ...`, a voter per line). It parses the file, executes the wrapper, and returns the sorted list of candidates.

---

## Usage Example

```python
from rgcr_methods import rgcr_wrapper

# Example input: A list of dictionaries mapping candidates to ratings
voters_data = [
    {1: 2, 2: 6},
    {2: 5, 3: 10}
]

print(rgcr_wrapper(voters_data))
# Output: [3, 2, 1]
```

---

## Running Tests
You can run the built-in test suite to verify the methods using pytest. Make sure you have it installed:

```Bash

pip install pytest
pytest test.py
Web Interface & Demo
```

---

For a hands-on demonstration and an easy-to-use interface, visit the live web app:
🔗 [https://avitalzer.csariel.xyz/](https://avitalzer.csariel.xyz/)
