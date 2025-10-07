import os
from google.genai import types


def write_file(working_directory, file_path, content):
    working_dir = os.path.abspath(working_directory)
    if os.path.isabs(file_path):
        full_file_path = os.path.abspath(file_path)
    else:
        full_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if os.path.commonpath([working_dir, full_file_path]) != working_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        parent = os.path.dirname(full_file_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
    except Exception as e:
        return f"Error: creating file_path: {e}"

    try:
        with open(full_file_path, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: writing to file. {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a file in directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING, description="The given content to write."
            ),
        },
    ),
)
