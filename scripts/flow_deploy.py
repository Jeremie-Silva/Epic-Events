import inspect
import os
import importlib.util

from prefect import Flow
import os
import importlib.util
from pathlib import Path

from prefect.deployments.deployments import Deployment


if __name__ == '__main__':
    for file in Path('app/workflows/').resolve().iterdir():
        if file.is_file() and file.suffix == '.py':
            spec = importlib.util.spec_from_file_location(file.stem, str(file.resolve()))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for name, obj in inspect.getmembers(module):
                if isinstance(obj, Flow):
                    obj.serve(name=name).deploy()
                    # obj.deploy(name=name,work_pool_name="local-pool")