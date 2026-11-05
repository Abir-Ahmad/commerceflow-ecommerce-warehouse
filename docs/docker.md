# Minimal Docker workflow

`Dockerfile` packages only the existing local Python/dbt workflow. It uses Python 3.12 slim and the same locked dependencies as local CI. It does not include Airflow, BigQuery credentials, raw data or a database service.

```bash
docker build -t commerceflow:test .
docker run --rm commerceflow:test
```

The default command runs `scripts/container_smoke.py`: generate the synthetic edge-case fixture, load it, build 17 models and run 48 dbt tests, reconcile seven metrics against CSVs, and check exact expected answers. A non-zero exit fails CI.

To process your original data instead (Linux/macOS/WSL):

```bash
docker run --rm \
  --mount type=bind,src="$PWD/data/olist",dst=/input,readonly \
  commerceflow:test python scripts/run_local.py --input /input
```

The database and generated results live inside the temporary container and are discarded with `--rm`. For inspection, omit `--rm` and give the container a name. No cloud authentication is needed for either command.

Verification status: Docker is absent in the authoring environment (no executable or daemon socket). A real build and execution are included in the existing `dbt-duckdb` GitHub Actions job; hosted outcome is pending. Merely adding this Dockerfile is not evidence that the image builds or runs.
