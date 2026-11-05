"""Default container test: fixture ingestion, dbt build and exact expected answers."""
import subprocess
import sys

for command in [
    ['scripts/make_fixture.py'],
    ['scripts/run_local.py', '--input', 'data/fixture'],
    ['scripts/assert_fixture.py'],
]:
    subprocess.run([sys.executable, *command], check=True)
print('PASS: container smoke workflow completed.')
