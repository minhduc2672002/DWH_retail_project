# 🛍️ Retail Data Warehouse Project

A retail data warehouse project built to process and analyze historical sales data using a dimensional model and data pipeline. The dataset contains over 500,000 records of transactions made by customers for a UK-based online retail store. This project includes data modeling, ETL pipeline design, and reporting on key business metrics.

---

## 📑 Table of Contents

- [📊 Dataset](#-dataset)
- [🏗️ Data Modeling](#️-data-modeling)
- [🔄 Data Pipeline](#-data-pipeline)
- [📈 Results](#-results)
- [🔗 References](#-references)

---

## 📊 Dataset

Source: [Online Retail Dataset - Kaggle](https://www.kaggle.com/datasets/tunguz/online-retail)

This dataset includes transactions for a UK-based online retailer over a period from 2010 to 2011.

| Column Name     | Description                                                                                                                                  |
|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| `InvoiceNo`     | Invoice number. 6-digit unique ID for each transaction. If prefixed with 'C', it indicates a **cancellation**.                              |
| `StockCode`     | Unique product/item code.                                                                                                                    |
| `Description`   | Product name or description.                                                                                                                 |
| `Quantity`      | Quantity of the product per transaction.                                                                                                     |
| `InvoiceDate`   | Date and time of the transaction.                                                                                                            |
| `UnitPrice`     | Price per unit of the product (in GBP).                                                                                                      |
| `CustomerID`    | Unique ID assigned to each customer.                                                                                                         |

---

## 🏗️ Data Modeling

The data is modeled using the **star schema** approach with one fact table and several dimension tables for efficient querying and reporting.

![Data Modeling Diagram](https://github.com/minhduc2672002/DWH_retail_project/assets/133132824/bcf15c69-6d20-424e-84db-99fbbc6222c2)

- **Fact Table**: Contains transactional data such as product, quantity, unit price, total value, and time.
- **Dimension Tables**: Include dimensions like `Product`, `Customer`, `Date`, and possibly `Country`.

---

## 🔄 Data Pipeline

The ETL pipeline is implemented to:
- Load raw data
- Clean and transform data
- Create dimension and fact tables
- Load data into a data warehouse

Pipeline flow:

![Pipeline Diagram](https://github.com/minhduc2672002/DWH_retail_project/assets/133132824/9ca70534-1df9-48c5-b43b-d7b124f79bd6)

The pipeline may be implemented using **Airflow**, **Spark**, or a custom Python-based solution depending on requirements.

---

## 📈 Results

The pipeline generates analytical views and dashboards for:
- Revenue trends over time
- Best-selling products
- Customer behavior
- Geographic insights

Sample output:

![Results](https://github.com/minhduc2672002/DWH_retail_project/assets/133132824/19d576fd-529c-4a39-a35d-95993bd5e425)

---

## 🔗 References

- [Kaggle Dataset - Online Retail](https://www.kaggle.com/datasets/tunguz/online-retail)
- [Dimensional Modeling Techniques - Kimball Group](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/dimensional-modeling-techniques/)
- [Airflow Documentation](https://airflow.apache.org/docs/)
- [Spark SQL & DataFrames Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
