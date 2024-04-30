import os
import sys

def read_configurations(config_file):
    configurations = {}
    with open(config_file, 'r') as file:
        for line in file:
            key, value = line.strip().split(':')
            configurations[key.strip()] = value.strip()
    return configurations

def replace_words(text, configurations):
    for word_to_find, replacement_word in configurations.items():
        text = text.replace(word_to_find, replacement_word)
    return text

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = input_file + ".modified"
    config_file = os.path.expanduser("~/Desktop/configurations.txt")

    if not os.path.exists(config_file):
        print("Configurations file not found on the desktop.")
        sys.exit(1)

    configurations = read_configurations(config_file)

    try:
        with open(input_file, 'r') as file:
            text = file.read()
    except FileNotFoundError:
        print("Input file not found.")
        sys.exit(1)

    modified_text = replace_words(text, configurations)

    try:
        with open(output_file, 'w') as file:
            file.write(modified_text)
        print(f"Text replaced and saved to {output_file}")
    except IOError:
        print("Error writing to output file.")

if __name__ == "__main__":
    main()

