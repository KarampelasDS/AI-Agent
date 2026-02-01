import os
from google.genai import types
from dotenv import load_dotenv
from functions.get_files_info import schema_get_files_info,get_files_info
from functions.write_file import schema_write_file,write_file
from functions.get_file_content import schema_get_file_content,get_file_content
from functions.run_python_file import schema_run_python_file,run_python_file

load_dotenv()
working_directory = os.environ.get("WORKING_DIRECTORY",'./calculator')

available_functions = types.Tool(function_declarations=[schema_get_files_info,schema_write_file,schema_get_file_content,schema_run_python_file],)

def call_function(function_call,verbose=False):
    function_name = function_call.name or ""
    
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    
    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }
    
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ]
        )
    
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = working_directory
    
    function_result = function_map[function_name](**args)
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ]
    )
    
    