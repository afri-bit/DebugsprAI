import os
import json
import google.generativeai as genai

# Configure API Key
API_KEY = ""
genai.configure(api_key=API_KEY)

# Define source folder and output mapping file
SRC_FOLDER = "../ai-coder-helloworld/src"
JSON_MAPPING_FILE = "file_mapping.json"
RESULT_FOLDER = "results"

# Ensure response folder exists
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Create a mapping dictionary
file_mapping = {}

# Step 1: Scan the src folder for Python files
for root, _, files in os.walk(SRC_FOLDER):
    for file in files:
        if file.endswith(".py"):  # Only process Python files
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(
                file_path, SRC_FOLDER
            )  # Store relative path

            # Store mapping
            file_mapping[relative_path] = file_path

# Step 2: Save the mapping to a JSON file
with open(JSON_MAPPING_FILE, "w") as json_file:
    json.dump(file_mapping, json_file, indent=4)

print(f"File mapping saved to {JSON_MAPPING_FILE}")

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

TEXT_PROMPT = """
We need to solve the issue based on following information. Ananlyse the file and check if there is any issue.
If the file is not empty, fix the code based on the following information:
* id: 1
* title: Python Hello World
* description: The add function is not working as expected
* type: bug
* src_folder: src
* test_folder: tests
* log: "2025-02-03 14:32:10 [INFO] The summary of number 4 and 5 is -1"

Requirements for the Output:
- No additional comment
- No markdown code annotations
- The output must contain only the code with the same structures as the input code, but with the necessary fixes. Empty code will be left empty as well.
- Comment the changes for fixed when necessary with AIFIX identification.
- Output must not contain any markdown annotations, so the code can be copied easily.
- If the file is empty, provide empty output as well. Just return empty string.
"""

# Step 3: Upload files to Gemini API and save responses in result folder
for relative_path, file_path in file_mapping.items():
    with open(file_path, "r", encoding="utf-8") as file:
        file_content = file.read()

    if not file_content.strip():
        print(f"Skipping {relative_path} as it is empty.")
        continue

    response = model.generate_content(
        [
            TEXT_PROMPT,
            file_content,
        ]
    )

    # Step 4: Save response in results folder, preserving folder structure
    result_file_path = os.path.join(
        RESULT_FOLDER, relative_path
    )  # Maintain the same structure
    os.makedirs(
        os.path.dirname(result_file_path), exist_ok=True
    )  # Create directories if needed

    with open(result_file_path, "w", encoding="utf-8") as result_file:
        result_file.write(response.text)

    print(f"Processed {relative_path}, response saved to {result_file_path}")

print("\n✅ All files uploaded and responses saved in the `results/` folder.")
