import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    #throw everything in a try-except block to not get uncatched errors:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir) == False:
            return f'Error: "{directory}" is not a directory'
        list_of_things = []
        #loop over every item dir or file in the target dir
        for thing in os.listdir(target_dir):
        
            thing_full_path = os.path.join(target_dir, thing)
            thing_size = os.path.getsize(thing_full_path)
            thing_gender = os.path.isdir(thing_full_path)
    
            thing_result = f"- {thing}: file_size={thing_size} bytes, is_dir={thing_gender}"
            list_of_things.append(thing_result)
        result_final = "\n".join(list_of_things)
    
        return result_final
    except Exception as e:
        return f"Error: {e}"
