import os
import subprocess
from google.genai import types

#schema for the AI to call the function
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs a .py file if its within the allowed working directoy, which is fed to the AI from the outside",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path points to the python file of which the function should execute",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="optional arguments that are appended to the command of the python execution instrucitons",
                items=types.Schema(type=types.Type.STRING),
            )
        },
    ),
)


def run_python_file(working_directory, file_path, args=None):
    #everything in a try-except block
    try:

    
    #check if file path is legit
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        # Will be True or False
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs   
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        

        #start subprocess and build the command:
        command = ["python", target_file]

        if args is not None:
            command.extend(args)
        
        command_output = subprocess.run(command, cwd=working_directory, text=True, capture_output=True, timeout=30)
        
        parts = []
        if command_output.returncode != 0:
            parts.append(f"Process exited with code {command_output.returncode}")
            # ... more conditions ...
        if command_output.stdout == "" and command_output.stderr == "":
            parts.append("No output produced")
        if command_output.stdout != "":
            parts.append(f"STDOUT: {command_output.stdout}")
        parts.append(f"STDERR: {command_output.stderr}")
        return "\n".join(parts)
        


    except Exception as e:
        return f"Error: executing Python file: {e}"

