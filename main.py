import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if(api_key is None):
    raise RuntimeError("GEMINI_API_KEY not found")

client = genai.Client(api_key=api_key)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chabot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose",action="store_true",help="Enable verbose output")
    args = parser.parse_args()
    
    messages = [types.Content(role="user",parts=[types.Part(text=args.user_prompt)])]
    
    completed = False
    
    for i in range(20):
        response = client.models.generate_content(model="gemini-2.5-flash",contents=messages,config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt))
        
        if response.usage_metadata is None:
            raise RuntimeError("No usage metadata found in response")
        
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        
        if not response.function_calls:
            print("Final response:")
            print(response.text)
            completed = True
            break
        
        function_results = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=args.verbose)

            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
                or not function_call_result.parts[0].function_response.response
            ):
                raise RuntimeError(f"Empty function response for {function_call.name}")

            function_results.append(function_call_result.parts[0])
        messages.append(types.Content(role="user",parts=function_results))
    
    if not completed:
        print("Maximum iterations (20) reached without a final response")
        sys.exit(1)
        
    if args.verbose:
        print(f"User prompt:{args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            

