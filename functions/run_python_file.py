import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    working_dir = os.path.abspath(working_directory)
    full_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not full_file_path.startswith(working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_file_path):
        return f'Error: File "{file_path}" not found.'
    if full_file_path[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file.'

    argument = ["python3", full_file_path]
    if len(args) > 0:
        for x in args:
            argument.append(x)

    try:
        result = subprocess.run(
            argument,
            timeout=30,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if len(result.stdout) == 0 and len(result.stderr) == 0:
            return "No output produced."
        if result.returncode != 0:
            return f"Return Code: {result.returncode}\n STDOUT:{result.stdout}\n STDERR: {result.stderr}/n Process exited with code {result.returncode}"
        return f"Return Code: {result.returncode}\n STDOUT:{result.stdout}\n STDERR: {result.stderr}"

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional CLI arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to execute, path should be relative to the calculator directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional List of strings we pass to our program as arguments.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)
