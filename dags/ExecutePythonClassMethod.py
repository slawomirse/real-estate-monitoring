from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class ExecutePythonClassMethod(BaseOperator):
    @apply_defaults
    def __init__(self, python_class, method_name, *args, **kwargs):
        super(ExecutePythonClassMethod, self).__init__(*args, **kwargs)
        self.python_class = python_class
        self.method_name = method_name

    def execute(self, context):
        method = getattr(self.python_class, self.method_name)
        method()