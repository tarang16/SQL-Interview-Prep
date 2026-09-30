"""Creates farmers_market_setup.sql (CREATE TABLE + INSERT) from the CSVs.
The literal text NULL in a CSV becomes SQL NULL."""
import csv
from pathlib import Path

HERE = Path(__file__).parent
TABLES = {
    "market_date_info": """market_date DATE NOT NULL PRIMARY KEY,
  market_day VARCHAR(45), market_week VARCHAR(45), market_year VARCHAR(45),
  market_start_time VARCHAR(45), market_end_time VARCHAR(45), special_notes BLOB,
  market_season VARCHAR(45), market_min_temp VARCHAR(200), market_max_temp VARCHAR(45),
  market_rain_flag INT, market_snow_flag INT""",
    "booth": """booth_number INT NOT NULL PRIMARY KEY, booth_price_level VARCHAR(45),
  booth_description VARCHAR(255), booth_type VARCHAR(45)""",
    "vendor": """vendor_id INT NOT NULL PRIMARY KEY, vendor_name VARCHAR(45), vendor_type VARCHAR(45),
  vendor_owner_first_name VARCHAR(45), vendor_owner_last_name VARCHAR(45)""",
    "customer": """customer_id INT NOT NULL PRIMARY KEY, customer_first_name VARCHAR(45),
  customer_last_name VARCHAR(45), customer_zip VARCHAR(45)""",
    "product_category": """product_category_id INT NOT NULL PRIMARY KEY, product_category_name VARCHAR(45)""",
    "product": """product_id INT NOT NULL PRIMARY KEY, product_name VARCHAR(45), product_size VARCHAR(45),
  product_category_id INT, product_qty_type VARCHAR(45)""",
    "vendor_booth_assignments": """vendor_id INT NOT NULL, booth_number INT NOT NULL, market_date DATE NOT NULL,
  PRIMARY KEY (vendor_id, booth_number, market_date)""",
    "vendor_inventory": """market_date DATE NOT NULL, quantity DECIMAL(16,2), vendor_id INT NOT NULL,
  product_id INT NOT NULL, original_price DECIMAL(16,2),
  PRIMARY KEY (market_date, vendor_id, product_id)""",
    "customer_purchases": """product_id INT NOT NULL, vendor_id INT NOT NULL, market_date DATE NOT NULL,
  customer_id INT NOT NULL, quantity DECIMAL(16,2), cost_to_customer_per_qty DECIMAL(16,2),
  transaction_time TIME NOT NULL""",
}

NUMERIC = {"INT", "DECIMAL"}


def lit(v):
    if v == "NULL":
        return "NULL"
    return "'" + v.replace("\\", "\\\\").replace("'", "''") + "'"


out = ["-- Farmers Market database (MySQL 8 / Workbench). Run the whole script once.",
       "CREATE DATABASE IF NOT EXISTS farmers_market;", "USE farmers_market;", "SET NAMES utf8mb4;", ""]
for t in reversed(list(TABLES)):
    out.append(f"DROP TABLE IF EXISTS {t};")
out.append("")
for t, cols in TABLES.items():
    out.append(f"CREATE TABLE {t} (\n  {cols}\n) DEFAULT CHARSET = utf8mb4;")
    with open(HERE / "csv" / f"{t}.csv", encoding="utf-8") as f:
        r = list(csv.reader(f))
    header, data = r[0], r[1:]
    values = ",\n".join("(" + ", ".join(lit(v) for v in row) + ")" for row in data)
    out.append(f"INSERT INTO {t} ({', '.join(header)}) VALUES\n{values};\n")

(HERE / "farmers_market_setup.sql").write_text("\n".join(out), encoding="utf-8")
print("written")
