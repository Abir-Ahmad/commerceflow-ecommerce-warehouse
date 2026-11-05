"""One reproducible, fail-fast command for local ingestion, dbt build and evidence."""
import argparse
import os
from pathlib import Path
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[1]
def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True, type=Path)
    p.add_argument('--evidence', type=Path, default=Path('target/evidence.json'))
    args = p.parse_args()
    source = args.input.resolve()
    os.chdir(ROOT)
    subprocess.run([sys.executable, 'scripts/load_raw.py', '--input', str(source)], check=True)
    dbt = Path(sys.executable).parent / ('dbt.exe' if os.name == 'nt' else 'dbt')
    subprocess.run([str(dbt), 'build', '--profiles-dir', 'profiles', '--target', 'local'], check=True)
    subprocess.run([sys.executable, 'scripts/verify_actual.py', '--input', str(source), '--output', str(args.evidence)], check=True)
if __name__ == '__main__':
    main()
