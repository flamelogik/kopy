import openai
import os
import re

# Assuming you have set your API key in the environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

def load_replacements(filename):
    replacements = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                if ':' in line:
                    word_to_find, replacement_word = line.strip().split(':', 1)
                    replacements[word_to_find.strip()] = replacement_word.strip()
    except FileNotFoundError:
        print(f"Configuration file not found at {filename}. Please check the path and try again.")
        return None
    return replacements

def replace_words(text, replacements):
    if replacements is None:
        return text
    for word, replacement in replacements.items():
        text = re.sub(r'\b{}\b'.format(re.escape(word)), replacement, text)
    return text

def read_and_process_vtt_file(filepath, replacements):
    print(f"Trying to read VTT file at: {filepath}")
    processed_lines = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for line in lines:
            if '-->' in line or line.strip().isdigit() or not line.strip() or line.strip() == "WEBVTT":
                processed_lines.append(line)
            else:
                processed_lines.append(replace_words(line, replacements))
        return processed_lines
    except FileNotFoundError:
        print("VTT file not found. Please check the path and try again.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the VTT file: {e}")
        return None

def generate_summary(text):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # Adjust model as necessary
            prompt=f"Summarize this video transcript in a detailed paragraph (5-7 sentences): {text}",
            max_tokens=150
        )
        detailed_summary = response.choices[0].text.strip()

        return detailed_summary
    except Exception as e:
        print(f"An error occurred while generating the summary: {e}")
        return None

def main():
    video_transcript_name = input("Enter the name of the Video Transcript: ")
    vtt_file_path = input("Enter the path to the VTT file: ")
    configurations_path = input("Enter the path to the configuration file: ")

    replacements = load_replacements(configurations_path)
    if replacements is None:
        return

    processed_lines = read_and_process_vtt_file(vtt_file_path, replacements)
    if processed_lines is None:
        return

    fixed_vtt_filename = f"{video_transcript_name}_fixed_words.vtt"
    with open(fixed_vtt_filename, 'w', encoding='utf-8') as file:
        file.writelines(processed_lines)
    print(f"Processed transcript saved as {fixed_vtt_filename}")

    full_transcript = ''.join([line for line in processed_lines if not line.startswith(('WEBVTT', '\n'))])
    detailed_summary = generate_summary(full_transcript)
    if detailed_summary is None:
        print("Failed to generate the summary.")
        return

    summary_email_filename = f"{video_transcript_name}_summary.txt"
    with open(summary_email_filename, 'w', encoding='utf-8') as file:
        file.write("Detailed Summary:\n" + detailed_summary + "\n")

    print(f"Summary and email content saved as {summary_email_filename}")

if __name__ == "__main__":
    main()
