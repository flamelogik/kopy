# --------------------------------------------------------------------------- #

# filename:    'logik-kopy_pro.py'
# version:      4.0.0

# --------------------------------------------------------------------------- #

import os
import re
import openai

# --------------------------------------------------------------------------- #

# Assuming you have set your API key in the environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

# --------------------------------------------------------------------------- #

def list_vtt_files(directory):
    vtt_files = []
    for file in os.listdir(directory):
        if file.endswith('.vtt'):
            vtt_files.append(file)
    print("Found .vtt files:", vtt_files)
    return vtt_files

# --------------------------------------------------------------------------- #

def process_vtt_file(file_path, process_directory):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        subtitle_entries = []
        timestamp = None
        subtitle_text = ""

        for line in lines:
            line = line.strip()
            if '-->' in line:  # Check if line contains timestamp
                if timestamp:  # If there was a previous timestamp, save the subtitle entry
                    subtitle_entries.append((timestamp, subtitle_text))
                    subtitle_text = ""  # Reset subtitle text
                timestamp = line
            elif line:  # Check if line is not empty
                subtitle_text += line + " "  # Append to subtitle text
        
        # Append the last subtitle entry
        subtitle_entries.append((timestamp, subtitle_text))

        # Create directory for processed files
        vtt_filename = os.path.splitext(os.path.basename(file_path))[0]
        process_subdirectory = os.path.join(process_directory, vtt_filename)
        os.makedirs(process_subdirectory, exist_ok=True)

        # Write subtitle contents to file
        subtitle_file_path = os.path.join(process_subdirectory, f"{vtt_filename}-subtitle_contents.txt")
        with open(subtitle_file_path, 'w') as subtitle_file:
            for _, subtitle_text in subtitle_entries:
                subtitle_file.write(subtitle_text.strip() + '\n')

        # Generate and write summaries
        full_transcript = ''.join(subtitle_text for _, subtitle_text in subtitle_entries)
        generate_and_write_summaries(vtt_filename, full_transcript, process_subdirectory)

        print(f"Processed '{file_path}' and saved files in '{process_subdirectory}'")

# --------------------------------------------------------------------------- #

def generate_and_write_summaries(vtt_filename, subtitle_contents, process_subdirectory):
    try:
        # Summary A (5-7 sentences)
        summary_a = generate_summary(subtitle_contents, max_tokens=150)
        if summary_a is None:
            print("Failed to generate Summary A.")
        else:
            with open(os.path.join(process_subdirectory, f"{vtt_filename}-summary_A.txt"), 'w', encoding='utf-8') as file:
                file.write("Summary A:\n" + summary_a + "\n")

        # Summary B (170 words)
        summary_b = generate_summary(subtitle_contents, max_tokens=170)
        if summary_b is None:
            print("Failed to generate Summary B.")
        else:
            with open(os.path.join(process_subdirectory, f"{vtt_filename}-summary_B.txt"), 'w', encoding='utf-8') as file:
                file.write("Summary B:\n" + summary_b + "\n")

        # Summary C (140 words)
        summary_c = generate_summary(subtitle_contents, max_tokens=140)
        if summary_c is None:
            print("Failed to generate Summary C.")
        else:
            with open(os.path.join(process_subdirectory, f"{vtt_filename}-summary_C.txt"), 'w', encoding='utf-8') as file:
                file.write("Summary C:\n" + summary_c + "\n")

        print(f"Summaries generated successfully for '{vtt_filename}'")
    except Exception as e:
        print(f"An error occurred while generating summaries: {e}")

# --------------------------------------------------------------------------- #

def generate_summary(text, max_tokens):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # Adjust model as necessary
            prompt=f"Summarize the text in a detailed paragraph (5-7 sentences):\n{text}",
            max_tokens=max_tokens
        )
        detailed_summary = response.choices[0].text.strip()
        return detailed_summary
    except Exception as e:
        print(f"An error occurred while generating the summary: {e}")
        return None

# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    script_path = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(script_path)
    build_directory = os.path.join(parent_directory, 'build')
    config_directory = os.path.join(parent_directory, 'config')
    doc_directory = os.path.join(parent_directory, 'doc')
    process_directory = os.path.join(parent_directory, 'process')
    script_directory = os.path.join(parent_directory, 'script')
    vtt_directory = os.path.join(parent_directory, 'example')
    # vtt_directory = os.path.join(parent_directory, 'vtt_files')

    # Ensure the process directory exists
    os.makedirs(process_directory, exist_ok=True)

    # List all .vtt files in the vtt_directory
    vtt_files = list_vtt_files(vtt_directory)
    print("List of .vtt files in the directory:")
    for file in vtt_files:
        file_path = os.path.join(vtt_directory, file)
        process_vtt_file(file_path, process_directory)

# --------------------------------------------------------------------------- #
