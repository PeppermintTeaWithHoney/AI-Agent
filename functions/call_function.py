from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from google.genai import types


def call_function(function_call_part, verbose=False):
    FUNCTIONS = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")

    else:
        print(f" - Calling function: {function_call_part.name}")

    kwargs = dict(function_call_part.args or {})
    kwargs["working_directory"] = "./calculator"
    name = function_call_part.name
    func = FUNCTIONS.get(name)

    if func is None:
        return types.Content(
            role="user",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"error": f"Unknown function: {name}"},
                )
            ],
        )

    if name not in FUNCTIONS:
        return types.Content(
            role="user",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"error": f"Unknown function: {name}"},
                )
            ],
        )

    call = func(**kwargs)

    return types.Content(
        role="user",
        parts=[
            types.Part.from_function_response(
                name=name,
                response={"result": call},
            )
        ],
    )
