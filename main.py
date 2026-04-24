#imports
import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_functions import available_functions, call_function
from stt import transcribe_file
from tts import speak_text

#setup
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("API key not found, you dunce")
client = genai.Client(api_key=api_key)


#compute the command line input of the user
parser = argparse.ArgumentParser(description="baby's first chatbot")
parser.add_argument("user_prompt",nargs="?",default=None, type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

#lets try voice mode
if args.user_prompt is not None:
    user_text = args.user_prompt
else:
    user_text = transcribe_file("input.wav")


messages = [types.Content(role="user", parts=[types.Part(text=user_text)])]
#collect messages outside the loop to not reset it
#work on chat history, create new list of users prompt(s)
#messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

#wrap everything in a loop
for _ in range(200):
    # call the model, handle responses, etc.
    
    #get responmse from API, check if API key is valid, store tokens in and tokens out to variables
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            #temperature=0,
            tools=[available_functions]
            )
    )
    if response.usage_metadata == None:
        raise RuntimeError("API key not found, you dunce")

    #check all messages and candiates, early in the loop, before function calling
    if response.candidates is not None:
        for candidate in response.candidates:
            messages.append(candidate.content)


    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count


    # print results:  response of LLM
    # if --verbose is true add user prompt, tokens in, tokens out,
    if args.verbose == True:
        print(f"User prompt: {user_text}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    function_results_list = []
    # check function calls first print response response of LLM
    if response.function_calls != None:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=args.verbose)
            if function_call_result.parts == []:
                raise Exception(f"parts list is empty")
            if function_call_result.parts[0].function_response == None:
                raise Exception(f"part is None")
            if function_call_result.parts[0].function_response.response == None:
                raise Exception(f"function is None")
            function_results_list.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

        messages.append(types.Content(role="user", parts=function_results_list))

    else:
        print(response.text)
        speak_text(response.text)
        exit(0)
    

print(f"maximum iterations reached without response")
exit(1)

