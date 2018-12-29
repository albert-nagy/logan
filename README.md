# Logan

Logan is a small log-analysis tool which extracts information about popularity of news articles and their authors from the server log stored in the "news" database.

## Installation

Logan.py runs on Python 2.7 and relies on Psycopg2 and Datetime modules.
```bash
python logan.py
```
It requires a database called "news" set up according to the "newsdata.sql" file. 

## Description

Logan.py lists the answers for 3 questions without taking user input:

- What are the 3 most popular articles of all time?
- What are The most popular authors of all time?
- On which days did more than 1% of the requests lead to errors?

The core of each of the 3 blocks is a SQL query:

The first one counts the occurences of those entries in the server log table which are related to articles listed in the articles table - using the articles' path as a key -, and gives back the 3 articles with the most successful requests (response code starting with "2").

The second query also counts the successful requests in the log table for each article and looks for their author, sums up the downloads for each author and gets the author's name from the authors table.

The third one counts all records and those with status code starting with "4" or "5" (although there were only codes 200 and 404 in the demo database, I left this possibility open) for each day (in order to do this I convert the time column's "timestamptz" format to "date" within the query), then compares both numbers, and if the number of errors is more than 1% of all requests in the log for that day, it lists the date.

After each query, a for cycle prints out the results. Only results of the 3rd query need a minimal post-processing in Python: the date gets converted to the format shown in the task's example and the percent rate gets rounded to 1 decimal.
