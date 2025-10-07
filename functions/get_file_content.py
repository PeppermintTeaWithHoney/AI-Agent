import os
from .configfile import string_hard_limit
from google.genai import types


def get_file_content(working_directory, file_path):
    working_path = os.path.abspath(working_directory)

    full_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    ok = os.path.commonpath([working_path, full_file_path]) == working_path
    if not ok:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(full_file_path, "r") as file:
            data = file.read()
            if len(data) >= string_hard_limit:
                data = data[:string_hard_limit]
                return (
                    f'{data} + [...File "{file_path}" truncated at 10000 characters]"'
                )
            return data
    except Exception as e:
        return f"Error: reading files. {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads a file in and returns the first 10000 characters or less if it doesn't have 10000`.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="It's the file_path the function needs to get provided.",
            ),
        },
    ),
)
