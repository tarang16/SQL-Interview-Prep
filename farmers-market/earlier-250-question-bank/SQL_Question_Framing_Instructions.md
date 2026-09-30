# Instructions: Writing SQL Practice Questions

Use this file as the brief whenever new SQL practice questions are needed, whether on the Farmers Market database or another dataset. Give it to Claude (or any author) together with the dataset and the list of topics.

---

## 1. Audience & Purpose

- Students are preparing for **data analyst / SQL interviews**.
- The questions should test **real interview depth**: traps, edge cases, reasoning and multi-step logic.
- They should still **read like basic or everyday questions**. The wording stays simple and friendly even when the logic is hard.
- **Never write difficulty labels** anywhere in the file: no "Easy", "Medium", "Hard", "Intermediate", "Advanced", "Tricky", "Bonus" or ⭐ ratings. Section titles name the topic only.

## 2. Scope Control

Only use the topics the user asks for. The default set used so far:

| Group | Concepts |
|---|---|
| Querying | SELECT, column aliases, derived (calculated) columns, constant columns |
| Filtering | WHERE, AND, OR, NOT, IN / NOT IN, BETWEEN / NOT BETWEEN, LIKE / NOT LIKE, IS NULL |
| String functions | CONCAT, INSTR, LEFT, RIGHT, SUBSTRING, TRIM (LEADING / TRAILING / BOTH), LENGTH, REVERSE |
| Numeric | ROUND (incl. negative decimals), arithmetic operators `+ - * / % DIV` |
| Others | DISTINCT, CASE (simple and searched, in SELECT / WHERE / ORDER BY) |

**Allowed helpers** (to support the main topics, never the focus of a question): `ORDER BY`, `LIMIT`, `UPPER`, `LOWER`, `REPLACE`, `REPEAT`, `LTRIM`/`RTRIM`, `TRUNCATE`, `CHAR_LENGTH` (for comparison questions only).

**Not allowed** unless the user adds them: JOINs, GROUP BY / HAVING, aggregate functions (COUNT, SUM, AVG…), subqueries, CTEs, window functions, date functions (DATEDIFF, DAYNAME…), LPAD/RPAD, SUBSTRING_INDEX, COALESCE/IFNULL (except in "how would you handle this?" discussion).

→ Every question must be answerable from **one table**.

## 3. SQL Dialect

- Default: **MySQL 8**, since LEFT, RIGHT, INSTR, REVERSE and CONCAT all exist there with standard behaviour.
- Say the dialect at the top of the question file.
- MySQL behaviour worth testing:
  - Default collation is case-insensitive, so `'large' = 'Large'` and `LIKE 'a%'` matches 'Alice'.
  - Trailing spaces depend on the collation's pad attribute: MySQL 8's default `utf8mb4_0900_ai_ci` is NO PAD (`'abc ' = 'abc'` is FALSE), while older collations such as `utf8mb4_general_ci` are PAD SPACE (TRUE). `LIKE` never ignores trailing spaces.
  - Implicit string↔number conversion: `'01234' = 1234` is TRUE, and `'12.5abc'` becomes 12.5.
  - `||` is logical OR by default, not string concatenation.
  - `SUBSTRING(s, 0, n)` returns an empty string. A negative start counts from the end.
  - `CONCAT` with any NULL argument returns NULL.
  - `NOT IN (…, NULL)` returns no rows.
  - `BETWEEN high AND low` returns no rows. BETWEEN on strings compares character by character.
  - `ROUND` on exact decimals rounds half away from zero (`ROUND(-2.5) = -3`).
  - `DISTINCT` + `ORDER BY` on a column that isn't selected raises an error in MySQL 8.
  - A SELECT alias works in ORDER BY but **not** in WHERE.

## 4. Question Mix (for roughly 250 questions)

| Section | Approx. count |
|---|---|
| SELECT & derived columns | 20–25 |
| WHERE | 15–20 |
| AND / OR / NOT (precedence, De Morgan, XOR logic) | 20–25 |
| IN / NOT IN (incl. NULL traps) | 15–20 |
| BETWEEN (inclusive ends, reversed bounds, strings, times, dates) | 15–20 |
| LIKE (`%`, `_`, escaping, NOT LIKE, case) | 20–25 |
| CONCAT (formatting, padding, NULL) | 12–15 |
| INSTR / LEFT / RIGHT / SUBSTRING (parsing without hard-coded positions) | 25–30 |
| TRIM / LENGTH / REVERSE (last-word, last-occurrence, palindromes, counting chars) | 15–20 |
| ROUND (negative precision, ROUND vs TRUNCATE, nearest 0.05, ceiling without CEIL) | 10–12 |
| DISTINCT (multi-column, derived, NULL, ORDER BY rule) | 12–15 |
| CASE (tiers, WHEN order trap, no-ELSE → NULL, CASE in WHERE / ORDER BY, nested, data checks) | 25–30 |
| Scenario questions (3+ concepts combined) | 12–15 |

Within every section, mix these **question styles**:
1. **Write the query**: a plain business request ("Find the customers whose…").
2. **What will this return?**: show a query or expression and ask for the output (tests understanding, not memory). About 10–15% of the bank.
3. **Spot / fix the bug**: a broken query to correct (`= NULL`, OR/AND precedence, CASE order, reversed BETWEEN).
4. **Compare two versions**: `=` vs `LIKE`, `SUBSTRING` vs `RIGHT`, `ROUND` vs `TRUNCATE`, simple vs searched CASE.
5. **Data check**: use the functions to find inconsistent rows (IDs that don't match SKUs, sizes that break a pattern, descriptions that don't match sizes).
6. **Scenario**: a realistic output such as a receipt line, username, masked name, code like `A-001` or label like `W01-2024`.

## 5. What Makes a Question Hard (while it still looks simple)

- Parse strings **without hard-coded positions** (INSTR-driven, e.g. `'10x10'` vs `'8x8'`).
- Put the trap in the **data type** (VARCHAR numbers, TIME as string, DATE vs string).
- Rely on **NULL logic** (NOT IN with NULL, CONCAT with NULL, CASE without ELSE).
- Rely on **operator precedence** (AND binds tighter than OR, `quantity + 1 * price`).
- Rely on **string ordering** ('Product 10' < 'Product 2', 'Harris' > 'H').
- Use **ranges that wrap** (a night window across midnight cannot use BETWEEN).
- Chain **2–3 functions** (REVERSE + INSTR + LENGTH for the last occurrence, LENGTH − LENGTH(REPLACE) for counting a character).
- Make **CASE order** decide the answer (first matching WHEN wins).
- Use **derived columns inside filters** (an alias can't be used in WHERE, so the expression must be repeated).

## 6. Writing Style Rules

- Number the questions continuously: **Q1 … Q250** (bold), grouped under `## Section N: Topic` headings.
- Name the table in backticks in the question (`customer_purchases`). Name the expected output columns / aliases when it helps grading.
- Use one clear business sentence first, then any constraint ("without using LIKE", "don't hard-code positions").
- Put code for "What will this return?" / "fix this" questions in ```sql fenced blocks.
- Give example outputs from the actual data where a format is expected (`'Johnson, Alice'`, `'A-001'`).
- No difficulty words (see §1). No answers in the question file. Put answers in a separate file only if asked.
- Start the file with a **topic list**, the **dialect**, the **rules** (single table, allowed helpers) and a **schema reference table**.

## 7. Grounding in the Data

Before writing, read every CREATE/INSERT file and note the quirks. Questions should use real values so that results are meaningful (not empty by accident). An intentionally empty result is fine, but only when the question is about reasoning.

### Farmers Market dataset: known quirks to reuse

| Table | Quirk / hook |
|---|---|
| `customer` | `customer_zip` is VARCHAR; '01234' has a leading zero; zips repeat (e.g. '12345' ×2). 3-letter names: Bob, Eve, Ivy, Leo, Tom. Palindromes (case-insensitive): **Bob**, **Eve**. Same-length first/last: Grace Davis, Steve Lewis. Last names ending "son": Johnson, Wilson, Anderson, Jackson, Robinson. Double letters: Miller, Moore, Harris, Lee. |
| `vendor` | `vendor_name` = 'Vendor N' (1–2 digits); `vendor_type` 'Type A'/'Type B' alternate; last name 'White' appears twice (vendors 4 and 16, both Type B); owner 'Eve Jones' (Type A). |
| `booth` | `booth_size` 'WxL' strings of different lengths ('10x10', '8x8', '6x6'); description ↔ size are consistent; price 100 → 195 in steps of 5. |
| `product` | `product_name` 'Product N', `product_sku` 'SKUN' (matches id); sizes cycle Small/Medium/Large by id, **except product 20** (Large instead of Medium), which is good for a data-check question. |
| `product_category` | 'Category N', same id as product. |
| `market_date_info` | Dates 2024-01-01 → 01-20, all Winter; `market_week` and `market_year` are **VARCHAR** (string-compare traps); snow on 01-03, 01-05, 01-10, 01-17, 01-20; no rain days; temp range 13–16. |
| `vendor_inventory` | quantity 10 → 200, price 15 → 34, one row per vendor/date. |
| `customer_purchases` | `transaction_time` goes from 10:00 through to the late-night times 00:00–05:00, which is useful for midnight-wrap questions; product_id = vendor_id = customer_id in every row; row 20 has quantity 1. |
| `market_date table.txt` | A separate SQLite-style demo that **redefines** `market_date_info` with start/end time columns. It conflicts with the main schema, so leave it out unless asked. |

## 8. Final Checklist Before Delivering

- [ ] The count matches the request (e.g. 250), numbered with no gaps or duplicates.
- [ ] Only the requested topics and allowed helpers are used; every question uses one table.
- [ ] No difficulty labels anywhere.
- [ ] Every column and table name matches the schema exactly.
- [ ] Every "What will this return?" question has a definite answer in the stated dialect.
- [ ] Every section mixes the question styles listed in §4.
- [ ] Output saved as Markdown in the course folder, with the schema reference at the top.

## 9. Prompt Template for Next Time

> Using `SQL_Question_Framing_Instructions.md`, write **N** questions on the **<dataset>** covering only **<topics>**. Keep the interview-level depth but the basic tone, add no difficulty labels, use a single table per question, and save the result as `<name>.md`. (Optional: also write an answer key in a separate file.)
