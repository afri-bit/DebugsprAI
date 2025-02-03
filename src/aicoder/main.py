import google.generativeai as genai

import os

if __name__ == "__main__":
    # Set the API key
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    if GEMINI_API_KEY is None:
        raise ValueError("Please set the 'GEMINI_API_KEY' environment variable")

    GEMINI_MODEL_NAME = os.environ.get("GEMINI_MODEL_NAME")
    if GEMINI_MODEL_NAME is None:
        raise ValueError("Please set the 'GEMINI_MODEL_NAME' environment variable")

    genai.configure(api_key=GEMINI_API_KEY)

    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(history=[])

    response = chat_session.send_message(
        "Give me python hello world. Only code, without any markdown annotations, so i can copy the code easily"
    )

    print(response.text)
