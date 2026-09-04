# Raw Data

The original source file is stored here as:

```text
product_sales_dataset_final.csv
```

## Preservation Rule

This file is the immutable source-of-truth dataset for the project and should not be edited in place. Cleaning, header normalization, date parsing, region standardization, and derived fields must be performed in Excel, PostgreSQL, Python, or an exported cleaned-data file.

Validated source characteristics:

- **200,000** transaction/order rows
- **14** raw fields
- **200,000** unique `Order_ID` values
- Date coverage: **2023-01-01 through 2024-12-31**
- Raw region values include `Centre`, which is standardized to `Central` downstream
- The last three raw CSV headers contain surrounding whitespace and require mapping/normalization

See `../data_dictionary.md` for field definitions and validation rules.
