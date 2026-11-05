"""Read-only preflight: ADC + existing project + SELECT 1. Never enables billing."""
import os
import sys
import google.auth
from google.auth.exceptions import DefaultCredentialsError
from google.cloud import bigquery
try:
    credentials, default_project = google.auth.default(scopes=['https://www.googleapis.com/auth/bigquery'])
except DefaultCredentialsError:
    print('BLOCKED: no Google Application Default Credentials; BigQuery NOT verified.')
    sys.exit(2)
project = os.environ.get('GCP_PROJECT') or default_project
if not project:
    print('BLOCKED: set GCP_PROJECT to an existing sandbox project.')
    sys.exit(2)
client = bigquery.Client(project=project, credentials=credentials)
config = bigquery.QueryJobConfig(maximum_bytes_billed=10000000)
print(list(client.query('select 1 as connection_ok', job_config=config).result()))
print('Authentication/query OK. Confirm sandbox/no billing in Google Cloud before loading.')
