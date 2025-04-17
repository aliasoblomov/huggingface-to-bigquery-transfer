# ─── CELL 3: General HF → BigQuery Loader ────────────────────────────────────

# === CONFIGURATION (REPLACE THESE!) ===
gcp_project_id = "YOUR_PROJECT_ID"        # ← e.g. "my‑gcp‑project"
bq_dataset_id  = "YOUR_BQ_DATASET"        # ← must already exist
bq_table_id    = "YOUR_TABLE_NAME"        # ← name for the new table
hf_dataset     = "username/dataset_name"  # ← any HF dataset ID
hf_split       = "train"                  # ← split to load (e.g. "train", "test")
bq_location    = "US"                     # ← match your dataset’s region
# =======================================

import time
import pandas as pd
from datasets import load_dataset
from google.cloud import bigquery

# Fully‑qualified table ref
table_ref = f"{gcp_project_id}.{bq_dataset_id}.{bq_table_id}"

print(f"• HF dataset: {hf_dataset} [{hf_split}]")
print(f"• BQ table:   {table_ref} (location={bq_location})\n")

# 1) Download & convert HF dataset → DataFrame
print("1️⃣ Downloading dataset from Hugging Face…")
hf_ds = load_dataset(hf_dataset, split=hf_split)
df    = hf_ds.to_pandas()
print(f"   → Loaded DataFrame: {df.shape[0]} rows × {df.shape[1]} columns\n")

# 2) Init BigQuery client & job config
client = bigquery.Client(project=gcp_project_id, location=bq_location)
job_config = bigquery.LoadJobConfig(
    write_disposition="WRITE_TRUNCATE",  # overwrite existing table
    autodetect=True,                     # infer schema
)

# 3) Upload with exponential‑backoff retries
max_retries = 5
for attempt in range(1, max_retries + 1):
    try:
        print(f"🔄 Attempt {attempt}: uploading…")
        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()  # wait for completion (raises on error)
        print(f"✅ Success: {job.output_rows} rows loaded into {table_ref}")
        break
    except Exception as err:
        print(f"⚠️  Attempt {attempt} failed: {err}")
        if attempt == max_retries:
            raise RuntimeError("All retries failed — aborting.") from err
        backoff = 2 ** attempt
        print(f"   ↳ retrying in {backoff}s…\n")
        time.sleep(backoff)

print("\n🎉 Done!")
