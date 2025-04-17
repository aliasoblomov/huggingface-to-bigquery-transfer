# huggingface-to-bigquery-transfer
A simple Python tool to transfer and clone Hugging Face datasets into Google BigQuery.

# hf2bq

A lightweight Python tool to **clone** and **transfer** any Hugging Face dataset into Google BigQuery with just a few lines of code. Whether you need a one‑off load or an automated sync, **hf2bq** handles download, schema inference, retries, and regional configuration—so you can focus on analysis, not infrastructure.

---

## 🔑 Features

- **Clone & Transfer**: Pull data directly from Hugging Face and push it into BigQuery.
- **Autodetect Schema**: Let BigQuery infer column types automatically.
- **Retries & Backoff**: Built‑in exponential backoff to handle transient failures (e.g., 503 errors).
- **Region‑Aware**: Specify your BigQuery dataset’s location (US, EU, etc.).

---

## 🛠️ Prerequisites & Permissions

Before you begin, make sure you have:

- A **Google Cloud Project** with the **BigQuery API** enabled.
- A **BigQuery dataset** already created in your project (e.g. `my_dataset`).
- **Roles** granted on the target dataset:
  - `BigQuery Data Editor` (`roles/bigquery.dataEditor`)
  - `BigQuery Job User` (`roles/bigquery.jobUser`)

> _Optional (GCS stashing):_ If you plan to stage large datasets via Cloud Storage, you'll also need:
> - `Storage Object Viewer` and `Storage Object Creator` on your GCS bucket.

---

## 🚀 Quickstart in Colab or Jupyter

This template consists of **three** cells. Run them **in order**:

### 1️⃣ Cell 1: Install Dependencies

```bash
!pip install datasets pandas google-cloud-bigquery pyarrow db-dtypes -q
```

> **What it does:** Installs Python packages for loading Hugging Face datasets (`datasets`), working with DataFrames (`pandas`), and interacting with BigQuery (`google-cloud-bigquery`, `pyarrow`, `db-dtypes`).

### 2️⃣ Cell 2: Authenticate to Google Cloud

```python
from google.colab import auth  # or use `google.auth` in a local environment
auth.authenticate_user()
print("✅ Authenticated with GCP")
```

> **What it does:** Opens a browser prompt (in Colab) or uses existing credentials to authorize your session to call GCP APIs.

### 3️⃣ Cell 3: Main HF → BigQuery Loader

Below is the general loader script. **Replace** the configuration placeholders before running.

```python
# === CONFIGURATION ===
# ▸ gcp_project_id: your GCP project ID
# ▸ bq_dataset_id : your existing BigQuery dataset
# ▸ bq_table_id   : name for the new table to create/overwrite
# ▸ hf_dataset    : Hugging Face dataset identifier (e.g. "username/dataset_name")
# ▸ hf_split      : which split to load ("train", "test", etc.)
# ▸ bq_location   : dataset region (e.g. "US", "EU")
# ======================
gcp_project_id = "YOUR_PROJECT_ID"
bq_dataset_id  = "YOUR_DATASET"
bq_table_id    = "YOUR_TABLE_NAME"
hf_dataset     = "username/dataset_name"
hf_split       = "train"
bq_location    = "US"

import time
import pandas as pd
from datasets import load_dataset
from google.cloud import bigquery

# Build the fully-qualified table reference
table_ref = f"{gcp_project_id}.{bq_dataset_id}.{bq_table_id}"

# 1) Download & convert dataset
df = load_dataset(hf_dataset, split=hf_split).to_pandas()
print(f"Loaded {{len(df)}} rows × {{len(df.columns)}} columns from Hugging Face")

# 2) Initialize BigQuery client
client = bigquery.Client(project=gcp_project_id, location=bq_location)
job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE", autodetect=True)

# 3) Upload with retries
max_retries = 5
for attempt in range(1, max_retries + 1):
    try:
        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()
        print(f"✅ Loaded {{job.output_rows}} rows into {{table_ref}}")
        break
    except Exception as e:
        print(f"Attempt {{attempt}} failed: {{e}}")
        if attempt == max_retries:
            raise
        time.sleep(2 ** attempt)
```

---

## 🙋‍♂️ Usage

1. **Clone** this repository:
   ```bash
git clone https://github.com/<your-org>/hf2bq.git
cd hf2bq
   ```
2. Open the notebook in Colab or Jupyter.
3. Follow the **Quickstart** steps above.

---

## 🐛 Troubleshooting

- **503 Service Unavailable**: Add more retries or stage via GCS.
- **Location mismatch**: Ensure your `bq_location` matches the dataset region shown in the Cloud Console.
- **Authentication errors**: Re-run Cell 2 or configure `GOOGLE_APPLICATION_CREDENTIALS` for local usage.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

