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

Verification status: **verified on a GitHub-hosted runner** in [run #1](https://github.com/Abir-Ahmad/commerceflow-ecommerce-warehouse/actions/runs/42029595045), commit `0826c8902f90e901e4d26d6ee9b1cf8856f3bffa`. The `Build and test local workflow container` step succeeded: the image was exported as `commerceflow:test`, the container built 17 dbt models, passed 48 tests and seven reconciliations, passed exact fixture assertions and exited successfully. Docker remains unavailable in the authoring environment. Full original-data execution inside Docker has not been tested; the verified container test uses the synthetic fixture.
