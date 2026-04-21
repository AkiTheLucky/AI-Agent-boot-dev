import os
from google.genai import types

#schema for the AI to call the function
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="writes or overrides the contents of a file within the allowed working directoy, which is fed to the AI from the outside",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path points to the file of which the contents should be written or overridden",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="content is a string that should be written to the target file",
                
            )
        },
    ),
)

#new file writing function for my baby boo agent
def write_file(working_directory, file_path, content):
    #everything in a try-except block
    try:

    
    #check if file path is legit
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        # Will be True or False
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs   
        if valid_target_file == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        #not sure if i need this if statement yet
        #if os.path.isfile(target_file) == False:
        #    return f'Error: File not found or is not a regular file: "{file_path}"'

        #check if all parent directories exist
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        #open the file in write mode
        with open(target_file, "w") as f:
            f.write(content)
            
        

        #in the end, submit this string
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {e}"