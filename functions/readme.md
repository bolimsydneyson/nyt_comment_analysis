# Data Cleaning and User-Defined Functions

## Codes and Examples


1. `comment_edit.py`

This file contains all user defined functions used for scraping the New York Times news articles. To use this set of user defined functions, one must have the New York Times developer API that has community (beta version) API enabled.

The New York Times API has limits, so functions in `comment_edit.py` have pause intervals within the API limit. If one plans to use this, make sure to check your API limit and edit the pause interval at `url_call()` function.


2. `name_classify.py`

Contains data cleaning and logical process describing how each first name becomes classified as male, female, or unknown (i.e. gender neutral names). Names come from the U.S. Social Security bureau. The bureau has a record of all baby's first names registered that year, with gender specification. Since the research aims to classify the New York Times readers' gender using their first names, ages 18-65 were used (year of birth from 1955 to 2002). There are total of 66,852 names (22,625 male names, 42091 female names, 2136 neutral names). To be classified to a gender, 80% or more of the people with that name belongs to a gender.
