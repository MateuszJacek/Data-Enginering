from pathlib import Path # Import Path from pathlib module

current_dir = Path.cwd() # Get the current working directory
current_file = Path(__file__).name # Get the name of the current script file
 
print(f"Files in {current_dir}:") # Print the current directory path

for filepath in current_dir.iterdir(): # Iterate over each item in the current directory
    if filepath.name == current_file: # Skip the current script file
        continue # Skip the current script file

    print(f"  - {filepath.name}") # Print the name of the file or directory

    if filepath.is_file(): # Check if the item is a file
        content = filepath.read_text(encoding='utf-8') # Read the content of the file
        print(f"    Content: {content}") # Print the content of the file