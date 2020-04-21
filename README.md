# Thesis
This is github repository for Sydney Bolim Son's master's thesis

------------------------------------------------------
## Section 1. Research Question & Hypothesis

This research proposes to analyze comments in New York Times finance section to provide additional literature on gender-based differences to finance.

The research hypothesizes that women are tend to participate less, and even if they do participate, their participation is less appreciated compared to men. Through this, the research aims to depict societal bias about women's participation in finance.

To prove the hypothesis, the research will utilize comments from the New York Times Business section and focus on three key variables:
1) Number of total recommendation (dependent variable, a proxy measure for 'acceptance')
2) Gender (independent variable, use comment handle as proxy for gender, use nltk library for male/female names; abbreviations(i.e. MLK) are noted as neutral)
3) NYTimes endorsement (independent variable, proxy for comment 'quality')<br/>
   Link to comment information is available [here](https://help.nytimes.com/hc/en-us/articles/115014792387-Comments)<br/>
	NYT Picks are a selection of comments that represent a range of views and are judged the most interesting or thoughtful. In some cases, NYT Picks may be selected to highlight comments from a particular region, or readers with first-hand knowledge of an issue.
4) How fast the person has commented (utilize timestamp)
5) Overall popularity of the article (use total number of comments)

------------------------------------------------------
## Section 2. API documentation for NYT comment section

#### Article comments
With the Community API, you can get readers' article comments.
https://api.nytimes.com/svc/community/v3/user-content/url.json?api-key={your-key}&offset=0&url=https%3A%2F%2Fwww.nytimes.com%2F2019%2F06%2F21%2Fscience%2Fgiant-squid-cephalopod-video.html

#### Article replies
And replies to those comments.
https://api.nytimes.com/svc/community/v3/user-content/replies.json?api-key={your-key}&url=https%3A%2F%2

#### Base URI
https://api.nytimes.com/svc/community/v3

#### Scope
NYTimes.com user-generated content, currently comments on articles.

#### HTTP method
GET

#### Response formats
JSON

To use the Community API, you must sign up for an API key. **Usage is limited to 4,000 requests per day and 10 requests per minute (rate limits are subject to change).** Please read and agree to the API Terms of Use and the Attribution Guidelines before you proceed.

#### Pagination
**Use the offset query parameter to paginate thru the results, 25 comments at a time. Use offset=0 to get the first 25 comments, offset=25 to get the next 25 comments, ...**

The url.json endpoint returns top-level comments and the first three replies. The totalParentCommentsFound field has the total number of top-level comments. Use that to determine how many comments you need to paginate thru.

In the comment node, the replyCount indicates how many replies there are to that top-level comment. If there are more than three, use the replies.json endpoint, the comment sequence and offset query parameter to paginate thru replies, 25 at a time.

You can sort the comment list by **newest first, oldest first, or comments with most reader recommendations first (sort=newest, oldest, or reader).**

#### Responses
The Community API is RESTful. It uses response codes to indicate the API status (200 - OK, 401 - invalid key, 429 - rate limit reached, ...).

#### Data Returned
Date fields are in Unix/UTC format.

------------------------------------------------------
## Section 3. User defined functions for analysis

Check functions folder
