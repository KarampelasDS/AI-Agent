import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_dir, file_path))
        valid_target_dir = os.path.commonpath([abs_dir, target_dir]) == abs_dir
        if valid_target_dir == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_dir.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_dir]
        if args is not None:
            command.extend(args)
        p = subprocess.run(command,cwd=abs_dir,capture_output=True,text=True,timeout=30)
        exitString = ""
        if p.returncode != 0:
            exitString += f"Process exited with code {p.returncode}\n"
        if len(p.stdout) == 0 and len(p.stderr) == 0:
            exitString += "No output produced\n"
        else:
            exitString += f"STDOUT: {p.stdout}\n"
            exitString += f"STDERR: {p.stderr}\n"
        return exitString
        
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file in the working directory with optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to execute, relative to the working directory",
            ),
        },
    ),
)