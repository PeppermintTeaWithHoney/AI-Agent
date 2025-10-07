import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from system_prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

import sys

# load_dotenv()
# api_key = os.environ.get("GEMINI_API_KEY")
# client = genai.Client(api_key = api_key)

# response = client.models.generate_content(
# model='gemini-2.0-flash-001', contents ="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
#        )
# print(response.text)
# print(response.usage_metadata.prompt_token_count)
# print (f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
# print (f"Response tokens: {response.usage_metadata.candidates_token_count}")
# messages = [
#   types.Content(role="user", parts=[types.Part(text=user_prompt)]),
# ]


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    args = []

    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
    user_prompt = " ".join(args)

    verbose = "--verbose" in sys.argv

    if len(sys.argv) < 2:
        print("Usage: python main.py 'your prompt here'")
        sys.exit(1)
    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    for i in range(20):
        try:
            response = generate_content(client, messages, verbose)
            if response.text and len(response.function_calls or []) == 0:
                print(response.text)
                break

        except Exception as e:
            return f"Error: can't generate content {e}."


def generate_content(client, messages, verbose):
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    for candidate in response.candidates:
        messages.append(candidate.content)

    functions_called = response.function_calls

    if functions_called:
        for fc in functions_called:
            tool_content = call_function(fc, verbose=verbose)
            messages.append(tool_content)
            if not tool_content.parts or not tool_content.parts[0].function_response:
                raise RuntimeError("Missing function_response from call_function")

            if verbose:
                print(f"-> {tool_content.parts[0].function_response.response}")

    return response


if __name__ == "__main__":
    main()
