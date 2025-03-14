# # Fetch Papers Pubmed
# A Python program to fetch research papers from PubMed, filter for non-academic authors affiliated with pharmaceutical or biotech companies, and save results in CSV format.
#
# ## Installation
# Install Poetry:
# ```bash
# pip install poetry
# ```
# Install dependencies:
# ```bash
# poetry install
# ```
#
# ## Usage
# ```bash
# poetry run get-papers-list "cancer research" -f results.csv -d
# ```
#
# ## Dependencies
# - requests: To handle API requests.
# - argparse: For command-line argument parsing.
