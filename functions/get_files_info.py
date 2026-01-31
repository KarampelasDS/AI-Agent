import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        abs_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_dir, directory))
        valid_target_dir = os.path.commonpath([abs_dir, target_dir]) == abs_dir
        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        lines = []
        for name in os.listdir(target_dir):
            full_name = os.path.join(target_dir,name)
            is_dir = os.path.isdir(full_name)
            file_size = os.path.getsize(full_name)
            final_string = f"- {name}: file_size={file_size} bytes, is_dir={is_dir}"
            lines.append(final_string)
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"
    
    
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
    
        