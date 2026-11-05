"""Execute real operators via dag.test(); this does not test a live scheduler."""
import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('commerceflow_dag',ROOT/'dags/commerceflow.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
run=module.dag.test()
states={t.task_id:str(t.state) for t in run.get_task_instances()}
assert str(run.state)=='success' and len(states)==3 and all(v=='success' for v in states.values()), states
result={'mode':'Airflow 2.10.5 dag.test(); local serial execution; no scheduler deployed', 'state':str(run.state),'tasks':states}
out=ROOT/'target/airflow-test.json'
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,indent=2)+'\n')
print(result)
