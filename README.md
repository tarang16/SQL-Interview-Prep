# SQL Interview Prep

SQL notes, cheat sheets and interview question banks for data analyst interview preparation. The main piece is a **200-question bank on the Farmers Market database**, built from real table data, with a full answer key.

## Contents

| Folder | What's inside |
|---|---|
| [`farmers-market/`](farmers-market) | 200 SQL interview questions and answers on the Farmers Market database, the table data as CSVs, and a one-click MySQL setup script |
| [`farmers-market/earlier-250-question-bank/`](farmers-market/earlier-250-question-bank) | An earlier 250-question bank (on a synthetic version of the same schema) with its answer key and the question-writing brief |
| [`notes/`](notes) | Session notes, the SQL cheat sheet, standard functions, GROUP BY / aggregation, self joins, pivot / unpivot, percentiles and correlation |
| [`question-banks/`](question-banks) | Practice sets and interview question banks: CASE, derived columns, subqueries, joins, LeetCode-style questions and advanced questions |
| [`window-functions/`](window-functions) | Window function cheat sheet, NTILE, LEAD / LAG, and assignment questions with solutions |

## Farmers Market question bank

| File | Use it for |
|---|---|
| `Farmers_Market_200_SQL_Questions_Only.pdf` | Practising (questions only) |
| `Farmers_Market_200_SQL_Questions_with_Answers.pdf` / `.docx` / `.md` | Checking answers |
| `farmers_market_setup.sql` | Creating the `farmers_market` database with all 9 tables in MySQL Workbench |
| `csv/` | The raw table data |

**Topics covered (everything before JOINs):**
- SELECT and derived columns; WHERE with AND / OR / NOT; IN; BETWEEN; LIKE
- String functions: CONCAT, INSTR, LEFT / RIGHT, SUBSTRING, SUBSTRING_INDEX, TRIM, LENGTH vs CHAR_LENGTH, REPLACE, REVERSE
- NULL handling: COALESCE, IFNULL, NULLIF
- CASE and SUM(CASE); numeric and date functions
- Aggregates; GROUP BY / HAVING; LIMIT / OFFSET; order of execution
- Subqueries, statistics (median, mode, z-scores, correlation) and interview logic puzzles

None of the answers use window functions or CTEs.

**Quick start**
1. Open `farmers-market/farmers_market_setup.sql` in MySQL Workbench and run the whole script.
2. Work through `Farmers_Market_200_SQL_Questions_Only.pdf`.
3. Check your answers in `Farmers_Market_200_SQL_Questions_with_Answers.pdf`.

> The table data was copied from InterviewBit's "Exploring the farmer's market" problem, which cuts long results short. Some tables are partial, so results on InterviewBit's full data will differ from the numbers quoted in the answers.

**Rebuilding the documents:** edit the `.md` file, then run `python build_docs.py` inside `farmers-market/`. This needs `markdown`, `python-docx`, and Google Chrome for the PDF.
