# ✈️ Serverless Flight Data ETL Pipeline on AWS

This project implements a fully automated, **serverless ETL pipeline** on AWS to ingest, transform, and load **daily flight data** into Amazon Redshift Serverless using AWS Glue, S3, Step Functions, and other AWS services.

---

## 🚀 Overview

The pipeline ingests **daily partitioned CSV files** from S3, joins them with static airport dimension data, and loads the processed data into Redshift Serverless for downstream analytics. It is **event-driven** and requires **zero manual intervention** once deployed.

---

## 🧰 Tech Stack

- **Storage/Data Lake**: Amazon S3 (Hive-style partitioned folders)  
- **Data Warehouse**: Amazon Redshift Serverless  
- **ETL & Cataloging**: AWS Glue (Crawlers, Jobs, Data Catalog)  
- **Orchestration**: AWS Step Functions, Amazon EventBridge  
- **Notification**: Amazon SNS  
- **Security & Networking**:
  - AWS IAM (roles and policies)
  - VPC Endpoints: S3, Redshift, STS, Secrets Manager, KMS
  - Security Groups (TCP port for Redshift)

---

## 🗂️ Data Structure

### S3 Structure
s3://<bucket-name>/daily_flights/ # Hive-style partitioned fact data
└── date=2024-07-08/flights.csv

s3://<bucket-name>/dim/
└── airports.csv # Dimension data

---

## 🛠️ Setup Instructions

### 1. Prepare S3 Buckets
- Upload `airports.csv` to `/dim/`
- Upload daily `flights.csv` files to `/daily_flights/` using Hive-style partitioning

### 2. Create Redshift Serverless
- Create a Redshift Serverless cluster and database
- Create schemas and tables for:
  - Airport dimension
  - Daily flights fact table

### 3. Configure Security
- Create IAM roles with required permissions for:
  - Glue, S3, Redshift, SNS, Step Functions
- Create VPC Endpoints:
  - S3, Redshift, STS, Secrets Manager, KMS
- Modify Redshift security group to allow TCP connections

### 4. Set Up Glue
- Create 3 Glue Crawlers:
  1. Redshift – Airport table
  2. Redshift – Flight table
  3. S3 – Incremental partitioned flight data
- Create a Glue ETL Job:
  - Joins fact and dimension data
  - Applies filters and transformations
  - Loads final output into Redshift

### 5. Orchestrate with Step Functions + EventBridge
- Step Function:
  - Triggers S3 Crawler
  - Runs Glue ETL Job
  - Publishes status via SNS
- EventBridge:
  - Listens for new object creation in S3
  - Triggers Step Function execution

---

## 🔄 How It Works

1. A new `flights.csv` is uploaded to the partitioned S3 location.
2. EventBridge detects the event and triggers the Step Function.
3. Step Function:
   - Runs the S3 Glue Crawler to detect schema
   - Executes the Glue ETL Job to process the data
   - Sends a status update via SNS
4. Final enriched data is loaded into Redshift Serverless.

---

## 📈 Outcome

- End-to-end **automated ingestion and processing** pipeline  
- **Serverless and scalable** architecture  
- **Event-driven orchestration** with no manual triggers  

---

## 📬 Notifications

SNS sends a success or failure message after each pipeline execution to subscribed endpoints (e.g., email, Lambda, HTTP).

---

## 🧪 Future Enhancements

- Add Glue triggers to support real-time streaming ingestion  
- Integrate with Amazon QuickSight for dashboards and analytics  
- Add support for schema evolution and data validation  

---

## 📎 License

This project is for educational and demonstration purposes.




