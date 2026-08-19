# DataOps Azure Data Platform — Demo Project

> **Mục tiêu:** Xây dựng mini Data Platform theo kiến trúc thực tế, tập trung tối đa vào **DataOps** (IaC, CI/CD, Security, Monitoring), không đi sâu vào chi tiết Data Engineering.

## 🏗 Kiến trúc tổng quan

```text
PostgreSQL (Source) 
    ↓ (Self-hosted IR)
Azure Data Factory (Ingestion & Orchestration) 
    ↓
ADLS Gen2 (Landing → Raw → Curated → Aggregation) 
    ↓
Databricks (Processing & Unity Catalog Governance)
    ↑
Azure DevOps (CI/CD: Git → PR → DEV → Approval → PROD)
    ↑
Terraform (IaC) + Key Vault (Security) + Azure Monitor (Observability)