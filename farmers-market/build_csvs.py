"""Rebuilds vendor_inventory.csv and vendor_booth_assignments.csv from the
values shown in the InterviewBit output (market days are every Wed + Sat)."""
import csv
from datetime import date, timedelta
from pathlib import Path

OUT = Path(__file__).parent / "csv"


def market_days(start, end):
    d, days = start, []
    while d <= end:
        if d.weekday() in (2, 5):  # Wednesday, Saturday
            days.append(d.isoformat())
        d += timedelta(days=1)
    return days


def nums(s):
    return [x for x in s.replace("|", " ").split()]


# ---------- vendor_inventory ----------
summer = market_days(date(2019, 7, 3), date(2019, 9, 28)) + market_days(date(2020, 7, 1), date(2020, 9, 30))
full = market_days(date(2019, 4, 3), date(2019, 12, 28)) + market_days(date(2020, 3, 4), date(2020, 10, 10))

p1 = nums("""7.38 10.96 13.08 10.22 10.59 9.04 10.66 6.76 11.23 10.72 6.98 10.73 10.63 7.88 7.84 10.58 9.34 7.4 10.13 11.44 8.84 10.32 12.73 8.63 6.29 9.54 |
11.92 10.08 11.85 10.08 10.01 8.15 8.52 10.29 8.52 8.66 15.49 9.19 10.51 12.7 10.28 10.86 12.34 9.38 14.23 9.38 10.75 10.84 10.11 10.04 10.19 9.88 13.76""")
p2 = nums("""33.63 24.56 28.83 29.17 29.89 28.31 30.48 26.65 29.87 32.23 29.28 27.18 33.35 25.58 32.02 17.29 26.2 27.87 35.86 31.11 24.44 24.16 29.34 28.4 33.72 28.91 |
24.17 31.82 28.19 28.49 29.75 36.98 31.27 32.9 34.13 24.15 36.52 34.16 26.15 28.51 26.48 32.86 30.95 28.01 32.06 30.06 28.66 29.9 31.59 29 22.03 30.16 28.95""")
p3 = nums("""70 70 60 80 60 70 70 70 80 50 70 70 80 50 50 60 80 80 80 50 60 60 50 80 80 70 |
60 60 50 60 80 80 60 60 70 70 70 60 70 60 70 60 60 80 50 50 60 80 60 70 50 70 60""")
p4 = nums("""40 40 30 30 40 40 40 30 | 40 30 40 40 30 30 40 30 40 | 30 40 30 30 40 40 40 40 30 |
40 30 30 40 40 40 40 30 30 | 40 40 40 30 40 40 40 30 40 | 40 40 40 30 40 40 40 30 |
30 40 40 40 30 30 40 40 40 | 40 40 40 30 40 40 40 30 40 | 30 40 40 40 40 30 30 40 |
30 40 40 30 40 40 40 40 | 40 40 30 40 40 40 40 40 40 | 30 40 30 30 30 40 40 40 40 |
40 40 40 40 40 30 40 40 | 40 40 30 40 40 30 40 40 40 | 30 40 40 40 40 40 40 30 40 |
40 40 40 30 30 40 30 40 30 | 40 30 30""")
p5 = nums("""16 23 23 25 22 24 18 18 | 25 21 24 17 16 18 25 16 18 | 17 16 22 17 19 16 21 18 25 |
24 19 16 17 23 18 25 21 20 | 18 20 21 18 20 17 19 24 20 | 21 25 25 21 16 18 23 21 |
21 19 25 17 23 25 19 24 18 | 18 15 21 16 21 25 22 17 15 | 20 22 16 21 19 19 18 17 |
15 17 16 22 20 15 25 22 | 22 16 24 19 23 25 22 22 24 | 18 22 25 15 17 16 20 18 24 |
15 24 21 22 21 15 22 23 | 16 24 19 21 16 22 23 15 18 | 21 23 16 21 21 17 19 25 20 |
21 15 18 24 17 25 21 15 25 | 22 20 20""")

inv = []
for pid, vid, price, dates, qty in [
    (1, 7, "6.99", summer, p1),
    (2, 7, "3.49", summer, p2),
    (3, 7, "0.5", summer, p3),
    (4, 7, "4", full, p4),
    (5, 8, "6.5", full, p5),
]:
    assert len(dates) == len(qty), (pid, len(dates), len(qty))
    inv += [(d, q, vid, pid, price) for d, q in zip(dates, qty)]
inv += [(d, q, 8, 7, "18") for d, q in
        [("2019-04-03", 8), ("2019-04-06", 8), ("2019-04-10", 6), ("2019-04-13", 6)]]

with open(OUT / "vendor_inventory.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["market_date", "quantity", "vendor_id", "product_id", "original_price"])
    w.writerows(inv)

# ---------- vendor_booth_assignments ----------
vba_dates = market_days(date(2019, 4, 3), date(2019, 12, 28)) + market_days(date(2020, 3, 4), date(2020, 5, 27))
rows = []
for d in vba_dates:
    summer19 = "2019-06-01" <= d <= "2019-09-28"
    peak19 = "2019-07-03" <= d <= "2019-09-28"
    a = [(1, 2), (3, 1), (4, 7)]
    if d == "2019-04-10":
        a = [(1, 7), (3, 1), (4, 2)]
    if summer19:
        a.append((4, 11))
    a += [(7, 11), (8, 10 if peak19 else 6), (9, 8)]
    rows += [(v, b, d) for v, b in a]

with open(OUT / "vendor_booth_assignments.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["vendor_id", "booth_number", "market_date"])
    w.writerows(rows)

print("vendor_inventory rows:", len(inv), "| vendor_booth_assignments rows:", len(rows))
