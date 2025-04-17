# huggingface-to-bigquery-transfer


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

## 🚀 Quickstart

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

### 3️⃣ Cell 3: Run the Loader Script

```bash
python hf-bigquery-loader.py
```

> **What it does:** Executes the general HF → BigQuery loader. Just provide your configuration in the script header, run it, and wait for the data to appear in BigQuery.

---

## 🐛 Troubleshooting

- **503 Service Unavailable**: Add more retries or stage via GCS.
- **Location mismatch**: Ensure your `bq_location` matches the dataset region shown in the Cloud Console.
- **Authentication errors**: Re-run Cell 2 or configure `GOOGLE_APPLICATION_CREDENTIALS` for local usage.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

