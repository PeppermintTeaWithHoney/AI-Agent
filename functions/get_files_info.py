import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    working_path = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, directory))
    if not target_path.startswith(working_path):
        return f"Error: Cannot list {directory} its outside of the working directory"
    if not os.path.isdir(target_path):
        return f"Error: {directory} is not a directory"
    try:
        all_files = []
        for filename in os.listdir(target_path):
            size = 0
            filepath = os.path.join(target_path, filename)
            is_dir = os.path.isdir(filepath)
            all_files.append(f"- {filename}: file size = {size} bytes, is_dir={is_dir}")
        return "\n".join(all_files)
    except Exception as e:
        return f"Error: listing files: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
