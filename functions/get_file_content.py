import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        abs_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_dir, file_path))
        valid_target_dir = os.path.commonpath([abs_dir, target_dir]) == abs_dir
        if valid_target_dir == False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_dir,"r") as f:
            content = (f.read(MAX_CHARS))
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Prints the content of a specified file relative to the working directory, limited to a maximum number of characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read from, relative to the working directory",
            ),
        },
    ),
)