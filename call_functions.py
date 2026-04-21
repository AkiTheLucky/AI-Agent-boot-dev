#imports here as well?
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_files import schema_write_file, write_file
#functions available to the AI


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ],
)

#lets actually allow the AI to touch functions
def call_function(function_call, verbose=False):
    #name?
    #args?
    #handle verbose paramenter
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    
    #determine which function to call
    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
        # etc.
}
    #define function name stop
    function_name = function_call.name or ""

    #check if function name in function map and crash
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
    )

    #overwrite an argument to make sure the working directory is fine
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"
    functions_result = function_map[function_name](**args)

    #success path, known function is the response
    return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": functions_result},
                )
            ],
)

 
        
        
    
    

        