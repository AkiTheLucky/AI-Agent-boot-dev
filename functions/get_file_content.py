import os
from config import CHAR_MAX
from google.genai import types

#schema for the AI to call the function
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="gets content of a file in a valid working directory up to MAX_CHAR characters in length",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path points to the file of which the function should read the contents of",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    
    try:

        #check if file path is legit
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs   
        if valid_target_file == False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_file) == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'

        #read the file and return contents as a string
        with open(target_file, "r") as f:
            contents = f.read(CHAR_MAX)
            if f.read(1):
                contents += f'[...File "{file_path}" truncated at {CHAR_MAX} characters]'
        return contents
    except Exception as e:
        return f"Error: {e}"