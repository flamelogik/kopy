import os

def list_vtt_files(directory):
    vtt_files = []
    for file in os.listdir(directory):
        if file.endswith('.vtt'):
            vtt_files.append(file)
    print("Found .vtt files:", vtt_files)
    return vtt_files

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

        # Create summary files
        for summary_type in ['A', 'B', 'C']:
            summary_file_path = os.path.join(process_subdirectory, f"{vtt_filename}-summary_{summary_type}.txt")
            with open(summary_file_path, 'w') as summary_file:
                # Write placeholder content for summary files
                summary_file.write(f"This is summary {summary_type} for {vtt_filename}.")

        print(f"Processed '{file_path}' and saved files in '{process_subdirectory}'")

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
