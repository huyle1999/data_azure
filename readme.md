# DataOps Azure Data Platform — Hands-on Project Roadmap

> **Goal:** Dựng một mini Data Platform theo architecture thực tế, nhưng tập trung vào **DataOps**, không đi sâu vào Data Engineering.

---

# 0. Project Goal

## Mục tiêu cuối cùng

Xây được hệ thống:

```text
                    Git
                     │
                     ▼
              Azure DevOps
                     │
                  CI/CD
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
         DEV                   PROD
          │                     │
         ADF                   ADF
          │                     │
         ADLS                 ADLS
          │                     │
     Databricks           Databricks
          │                     │
          └──────────┬──────────┘
                     │
             DataOps Platform
                     │
       ┌─────────────┼─────────────┐
       ▼             ▼             ▼
   Key Vault        RBAC       Monitoring
```

Source data:

```text
PostgreSQL
```

Data flow:

```text
PostgreSQL
    ↓
ADF
    ↓
ADLS Landing
    ↓
ADLS Raw
    ↓
Databricks
    ↓
ADLS Curated / Gold
```

DataOps flow:

```text
Developer
    ↓
Git
    ↓
Pull Request
    ↓
CI
    ↓
Deploy DEV
    ↓
Test
    ↓
Approval
    ↓
Deploy PROD
```

---

# Phase 1 — Project Foundation

## Mục tiêu

Hiểu project structure và chuẩn bị môi trường.

## Cần làm

* Tạo Git repository.
* Tạo cấu trúc project.
* Chuẩn bị Azure subscription.
* Tạo resource group.
* Xác định DEV/PROD architecture.
* Chuẩn bị naming convention.
* Chuẩn bị tagging convention.

## Structure

```text
dataops-platform/
│
├── infra/
│   └── terraform/
│
├── adf/
│
├── databricks/
│
├── tests/
│
├── scripts/
│
├── docs/
│
└── azure-pipelines.yml
```

## Cần hiểu

* Azure Resource Group
* Subscription
* Resource
* Region
* Environment
* Naming convention
* Tags

## Output

```text
Git repository
    +
Azure Resource Group
    +
DEV/PROD design
```

## Không cần học

* Data modeling
* Spark optimization
* ML
* Power BI

---

# Phase 2 — Source Data

## Mục tiêu

Có một source system để mô phỏng hệ thống thật.

Không lấy data từ Kaggle.

Tự generate synthetic data.

## Source

```text
PostgreSQL
```

## Database

```text
restaurant
│
├── customers
├── restaurants
├── orders
└── order_items
```

## Data size

Ban đầu:

```text
customers       10,000
restaurants       100
orders          100,000
order_items     200,000+
```

Sau khi pipeline chạy ổn:

```text
orders          1,000,000+
```

## Data cần có

* Normal records
* NULL
* Duplicate
* Invalid value
* Missing record
* Different dates

Mục đích là sau này dùng chúng để test pipeline và data quality.

## Cần hiểu

* Source system
* Database connection
* Credentials
* Network connectivity
* Incremental data

## Output

```text
PostgreSQL
    │
    └── restaurant database
```

---

# Phase 3 — ADLS Gen2

## Mục tiêu

Dựng Data Lake.

## Architecture

```text
ADLS Gen2
│
└── data/
    │
    ├── landing/
    │
    ├── raw/
    │
    ├── curated/
    │
    └── aggregation/
```

## Landing

Data vừa lấy từ source.

```text
landing/
└── orders/
    └── 2026/
        └── 08/
            └── 18/
```

## Raw

Data được lưu lâu dài để có thể replay/reprocess.

```text
raw/
└── orders/
```

## Curated

Data đã được xử lý bởi Data Engineer.

DataOps chỉ cần biết:

```text
raw → processing → curated
```

không cần tự xây transformation phức tạp.

## Aggregation

Data phục vụ downstream.

```text
aggregation/
└── daily_sales/
```

## Cần hiểu

* ADLS Gen2
* Storage Account
* Container
* Blob
* Hierarchical namespace
* Folder convention
* Partition
* Access control

## Output

```text
Working ADLS Gen2
```

---

# Phase 4 — Azure Data Factory

## Mục tiêu

Dựng ingestion/orchestration layer.

Architecture:

```text
PostgreSQL
     │
     ▼
    ADF
     │
     ▼
ADLS Landing
```

## ADF cần học

```text
ADF
├── Pipeline
├── Activity
├── Dataset
├── Linked Service
├── Integration Runtime
├── Parameter
├── Variable
└── Trigger
```

## Pipeline đầu tiên

```text
Copy Activity
     │
     ▼
PostgreSQL
     │
     ▼
ADLS Landing
```

## Sau đó

Thêm:

```text
Validation
    ↓
Copy
    ↓
Success / Failure
```

## Cần hiểu

### Linked Service

ADF kết nối tới resource nào?

```text
ADF → PostgreSQL
ADF → ADLS
```

### Dataset

Data nằm ở đâu và format gì?

### Pipeline

Workflow chạy như thế nào?

### Integration Runtime

ADF dùng compute/network nào để kết nối source?

---

# Phase 5 — Integration Runtime

## Mục tiêu

Hiểu cách Azure service kết nối tới hệ thống bên ngoài Azure.

Mô phỏng:

```text
PostgreSQL
  │
  │
  ▼
Self-hosted Integration Runtime
  │
  ▼
Azure Data Factory
  │
  ▼
ADLS
```

## Cần làm

* Cài Self-hosted IR.
* Connect IR với ADF.
* Test connectivity.
* Cho ADF đọc PostgreSQL.
* Copy data sang ADLS.

## Cần hiểu

* Azure IR
* Self-hosted IR
* Network path
* Firewall
* Port
* Authentication
* Connectivity troubleshooting

## Output

ADF có thể lấy data từ PostgreSQL.

---

# Phase 6 — Databricks

## Mục tiêu

Hiểu Databricks ở góc nhìn DataOps.

Không học PySpark sâu.

## Cần biết

```text
Databricks
├── Workspace
├── Notebook
├── Cluster / Compute
├── Job
├── Job Run
├── Secret
└── Permissions
```

## Pipeline

```text
ADLS Raw
    ↓
Databricks Job
    ↓
Notebook
    ↓
ADLS Curated
```

Notebook chỉ cần transformation rất đơn giản.

Ví dụ:

```text
raw orders
    ↓
remove duplicate
    ↓
validate amount
    ↓
write curated
```

## DataOps focus

Mày cần quan tâm:

```text
Job chạy được không?
       ↓
Có fail không?
       ↓
Log ở đâu?
       ↓
Retry thế nào?
       ↓
Deploy job thế nào?
       ↓
Configuration nằm đâu?
```

## Không cần tập trung

```text
❌ Spark internals
❌ Shuffle optimization
❌ Advanced PySpark
❌ ML
```

---

# Phase 7 — Unity Catalog

## Mục tiêu

Hiểu governance layer của Databricks.

Architecture:

```text
Unity Catalog
│
├── Catalog
│
├── Schema
│
└── Tables
```

Ví dụ:

```text
restaurant
└── analytics
    ├── orders
    ├── customers
    └── daily_sales
```

## Cần làm

* Tạo catalog.
* Tạo schema.
* Tạo table.
* Grant permission.
* Test access.
* Kiểm tra lineage cơ bản.

## Cần hiểu

* Catalog
* Schema
* Table
* External location
* Storage credential
* RBAC / permissions
* Data lineage

## Output

Data Engineer có thể dùng platform mà không cần quyền admin.

---

# Phase 8 — Infrastructure as Code

## Mục tiêu

Không tạo Azure infrastructure bằng Portal nữa.

Dùng:

```text
Terraform
```

## Terraform phải dựng được

```text
Resource Group
Storage Account
ADLS
ADF
Key Vault
Log Analytics
Monitoring resources
Databricks
```

## Structure

```text
infra/
└── terraform/
    │
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    ├── providers.tf
    │
    └── environments/
        ├── dev.tfvars
        └── prod.tfvars
```

## Cần thực hành

```bash
terraform init
terraform validate
terraform plan
terraform apply
terraform destroy
```

## Cần hiểu

* Resource
* Variable
* Output
* Module
* State
* Remote state
* Plan
* Apply
* Drift

## Output

Có thể dựng lại environment bằng code.

---

# Phase 9 — Security & Secrets

## Mục tiêu

Không hardcode credential.

Architecture:

```text
ADF / Databricks
       │
       ▼
   Key Vault
       │
       ├── DB secret
       ├── API secret
       └── connection secret
```

## Cần làm

* Tạo Key Vault.
* Tạo secrets.
* Managed Identity.
* RBAC.
* Cho ADF access Key Vault.
* Cho Databricks access secret theo design phù hợp.

## Cần hiểu

```text
Managed Identity
Service Principal
RBAC
Key Vault
Secret
Access Policy
```

## Test

User A:

```text
Can read secret
```

User B:

```text
Cannot read secret
```

---

# Phase 10 — CI Pipeline

## Mục tiêu

Mỗi Pull Request phải được validate tự động.

Flow:

```text
Developer
    ↓
Git branch
    ↓
Pull Request
    ↓
CI
```

## CI cần làm

```text
Terraform
├── format
├── validate
└── plan

ADF
├── validate
└── artifact check

Databricks
└── basic validation

Tests
└── data quality / config tests
```

## Pipeline

```text
PR
 │
 ▼
Checkout
 │
 ▼
Validate
 │
 ├── Terraform
 ├── ADF
 ├── Databricks
 └── Tests
 │
 ▼
PASS / FAIL
```

## Output

Code lỗi thì **không được merge**.

---

# Phase 11 — CD: DEV Deployment

## Mục tiêu

Merge code → tự động deploy DEV.

Flow:

```text
Merge
  ↓
Build
  ↓
Deploy DEV
```

## Deploy

```text
Terraform
    ↓
Azure infrastructure

ADF artifact
    ↓
ADF DEV

Databricks artifact
    ↓
Databricks DEV
```

## Cần hiểu

* Build artifact
* Deployment stage
* Service connection
* Environment
* Variable
* Secret
* Approval

---

# Phase 12 — DEV → PROD Promotion

## Mục tiêu

Hiểu environment promotion.

Architecture:

```text
             Git
              │
              ▼
             CI
              │
              ▼
             DEV
              │
          Integration Test
              │
              ▼
          Manual Approval
              │
              ▼
             PROD
```

## Quan trọng

Không build lại code khác nhau cho PROD.

```text
Same artifact
      ↓
DEV
      ↓
PROD
```

Chỉ thay đổi:

```text
Environment configuration
```

Ví dụ:

```text
DEV_STORAGE_ACCOUNT
PROD_STORAGE_ACCOUNT
```

## Output

Một commit có thể đi:

```text
Git → DEV → PROD
```

với approval.

---

# Phase 13 — Data Quality & Quality Gate

## Mục tiêu

Pipeline không chỉ kiểm tra:

```text
"Job chạy thành công"
```

mà còn:

```text
"Data có hợp lệ không?"
```

## Test cơ bản

```text
row_count > 0

id IS NOT NULL

duplicate_id = 0

amount >= 0

required column exists
```

## Pipeline

```text
Databricks Job
      ↓
Data Quality Test
      │
      ├── PASS → Continue
      │
      └── FAIL → Stop
```

## DataOps concept cần hiểu

* Data quality
* Quality gate
* Validation
* Schema validation
* Data contract cơ bản
* Failure handling

---

# Phase 14 — Monitoring & Observability

## Mục tiêu

Biết platform đang hoạt động hay chết ở đâu.

## Monitor

### ADF

```text
Pipeline success
Pipeline failure
Pipeline duration
Activity failure
```

### Databricks

```text
Job success
Job failure
Job duration
Cluster status
```

### Azure

```text
Resource health
Storage
Network
Authentication
```

### CI/CD

```text
Build failure
Deployment failure
Approval
Rollback
```

## Architecture

```text
ADF
 │
Databricks
 │
Azure Resources
 │
 ▼
Azure Monitor
 │
 ▼
Log Analytics
 │
 ▼
Alert
```

## Cần thực hành

Cố tình làm pipeline fail.

Sau đó tìm:

```text
Where did it fail?
Why did it fail?
Which resource failed?
Which log contains the error?
How to retry?
```

---

# Phase 15 — Failure & Recovery

## Mục tiêu

Đây là phần rất quan trọng với DataOps.

Cố tình tạo:

```text
Database unavailable
ADLS permission denied
Wrong secret
Invalid schema
Databricks job failure
ADF pipeline failure
Terraform drift
```

Sau đó xử lý.

## Cần hiểu

```text
Retry
Timeout
Failure handling
Alert
Rollback
Rerun
Idempotency
Recovery
```

Ví dụ:

```text
ADF failed
   ↓
Investigate log
   ↓
Fix configuration
   ↓
Rerun
   ↓
Validate data
```

---

# Phase 16 — End-to-End DataOps Pipeline

## Mục tiêu

Ghép tất cả lại.

Final architecture:

```text
                         Git
                          │
                          ▼
                   Azure DevOps
                          │
                    ┌─────┴─────┐
                    │    CI     │
                    └─────┬─────┘
                          │
                    Deploy DEV
                          │
                          ▼
                  ┌──────────────┐
                  │     ADF      │
                  └──────┬───────┘
                         │
                  PostgreSQL
                         │
                         ▼
                       ADLS
                         │
                         ▼
                    Databricks
                         │
                         ▼
                      Curated
                         │
                         ▼
                    Quality Test
                         │
                    ┌────┴────┐
                    │  PASS   │
                    └────┬────┘
                         │
                   Integration Test
                         │
                         ▼
                     Approval
                         │
                         ▼
                    Deploy PROD
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
          Key Vault             Monitoring
              │                     │
              └──────────┬──────────┘
                         ▼
                     Production
```

---

# Phase 17 — Production Simulation

## Mục tiêu

Đưa project từ "lab" thành "gần production".

## Thêm

```text
DEV
TEST
PROD
```

## Thêm

* Remote Terraform state
* Separate service connections
* Separate Key Vault
* RBAC
* Managed Identity
* Approval gate
* Monitoring
* Alert
* Data quality
* Rollback
* Documentation

## Test scenario

### Scenario 1

```text
Developer sửa ADF
```

Expected:

```text
PR
 ↓
CI
 ↓
DEV
 ↓
Test
 ↓
Approval
 ↓
PROD
```

### Scenario 2

```text
Terraform change sai
```

Expected:

```text
terraform plan
 ↓
Detect change
 ↓
Reject PR
```

### Scenario 3

```text
Databricks Job fail
```

Expected:

```text
Job fail
 ↓
Log
 ↓
Alert
 ↓
Investigate
 ↓
Fix
 ↓
Rerun
```

### Scenario 4

```text
Secret expired / invalid
```

Expected:

```text
Pipeline fail
 ↓
Monitor
 ↓
Key Vault
 ↓
Fix secret
 ↓
Rerun
```

---

# Phase 18 — Architecture Mapping

Sau khi hoàn thành project, map nó với architecture thật.

| Mini Project   | Project thật                     |
| -------------- | -------------------------------- |
| PostgreSQL     | SAP / DB / API / external source |
| ADF            | Data Factory                     |
| Self-hosted IR | On-prem integration              |
| ADLS           | Data Lake                        |
| Landing        | Landing Zone                     |
| Raw            | Raw Zone                         |
| Databricks     | Data Processing                  |
| Curated        | Curated Zone                     |
| Aggregation    | Aggregation Zone                 |
| Unity Catalog  | Data Governance                  |
| Key Vault      | Security                         |
| Azure Monitor  | Monitoring                       |
| Azure DevOps   | CI/CD                            |
| Terraform      | IaC                              |
| Databricks Job | Production workload              |

---

# Final Skill Target

Sau project này, mày phải trả lời được các câu hỏi:

## Infrastructure

* Resource này được tạo bằng gì?
* Terraform state nằm đâu?
* DEV/PROD khác nhau thế nào?
* Làm sao recreate environment?

## CI/CD

* ADF deploy thế nào?
* Databricks deploy thế nào?
* PR validate cái gì?
* DEV → PROD promotion thế nào?
* Rollback thế nào?

## Security

* Secret nằm đâu?
* Managed Identity là gì?
* Service Principal là gì?
* Ai được access ADLS?
* Ai được access Key Vault?

## Data Platform

* ADF làm gì?
* Databricks làm gì?
* ADLS làm gì?
* Integration Runtime làm gì?
* Raw/Curated/Aggregation khác nhau thế nào?

## Operations

* Pipeline fail thì xem log ở đâu?
* Databricks Job fail thì debug thế nào?
* Permission denied thì kiểm tra gì?
* Schema change thì xử lý thế nào?
* Data quality fail thì pipeline có tiếp tục không?

## Architecture

Cuối cùng nhìn architecture thật và có thể nói:

> "Đây là ingestion layer."

> "Đây là processing layer."

> "Đây là governance/security layer."

> "Đây là CI/CD layer."

> "Đây là monitoring layer."

> "Đây là phần DataOps mà tôi chịu trách nhiệm."

---

# Definition of Done

Project được coi là **xong** khi:

* [ ] PostgreSQL source chạy được
* [ ] Synthetic data được generate
* [ ] ADLS Gen2 hoạt động
* [ ] ADF copy được PostgreSQL → ADLS
* [ ] Integration Runtime hoạt động
* [ ] Databricks Job chạy được
* [ ] Raw → Curated flow chạy được
* [ ] Unity Catalog được cấu hình
* [ ] Terraform dựng được infrastructure
* [ ] Key Vault lưu secrets
* [ ] Managed Identity/RBAC hoạt động
* [ ] CI validate được code
* [ ] CD deploy được DEV
* [ ] DEV → PROD có approval
* [ ] Data quality gate hoạt động
* [ ] Azure Monitor thu được logs
* [ ] Alert khi pipeline fail
* [ ] Có thể cố tình tạo failure và recovery
* [ ] Có thể destroy/recreate infrastructure bằng IaC
* [ ] Hiểu được toàn bộ flow từ source → production

---

# Thứ tự học quan trọng nhất

Không cần học tất cả cùng lúc.

```text
1. Azure basics
       ↓
2. ADLS
       ↓
3. ADF
       ↓
4. Integration Runtime
       ↓
5. Databricks basics
       ↓
6. Terraform
       ↓
7. Key Vault + IAM
       ↓
8. Azure DevOps CI/CD
       ↓
9. Data Quality
       ↓
10. Monitoring
       ↓
11. Failure / Recovery
       ↓
12. Production Simulation
```

**Trọng tâm DataOps:**

```text
        ┌──────────────────────────┐
        │        DATAOPS           │
        │                          │
        │  IaC                     │
        │  CI/CD       ⭐⭐⭐⭐⭐      │
        │  Security                │
        │  Environment             │
        │  Monitoring              │
        │  Reliability             │
        │  Data Quality            │
        │  Automation              │
        └──────────────────────────┘
```

Data Engineering chỉ cần **đủ hiểu workload để vận hành nó**. Không cần biến project này thành khóa học PySpark/Data Engineering.

