import os
import argparse
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if(api_key is None):
    raise RuntimeError("GEMINI_API_KEY not found")

client = genai.Client(api_key=api_key)

def main():
    parser = argparse.ArgumentParser(description="Chabot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    response = client.models.generate_content(model="gemini-2.5-flash",contents=args.user_prompt)
    if response.usage_metadata is not None:
        print("Prompt tokens: ",response.usage_metadata.prompt_token_count)
        print("Response tokens: ",response.usage_metadata.candidates_token_count)
        print(response.text)
    else:
        raise RuntimeError("No usage metadata found in response")
    


if __name__ == "__main__":
    main()
