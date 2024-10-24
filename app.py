import os
import streamlit as st
from pathlib import Path
import zipfile
import pyperclip  # Library to copy text to the clipboard

# Function to generate the tree structure with filters and file truncation for LLM input
def generate_tree_structure(root_dir, exclude_files=None, exclude_dirs=None, level=0, file_limit=2):
    exclude_files = exclude_files or []
    exclude_dirs = exclude_dirs or []
    
    tree_structure = ""
    prefix = "    " * level + "|-- "
    
    try:
        dir_content = os.listdir(root_dir)
        
        # Sort to ensure a consistent order for display
        dir_content.sort()

        # Separate directories and files
        dirs = [item for item in dir_content if os.path.isdir(os.path.join(root_dir, item))]
        files = [item for item in dir_content if os.path.isfile(os.path.join(root_dir, item))]
        
        # Display directories
        for directory in dirs:
            if directory in exclude_dirs:
                continue
            tree_structure += prefix + directory + "/" + "\n"
            tree_structure += generate_tree_structure(os.path.join(root_dir, directory), exclude_files, exclude_dirs, level + 1, file_limit)
        
        # Display files, limiting long lists of similar file types
        if len(files) > file_limit * 2:  # If more files than twice the file limit (e.g., 4)
            for item in files[:file_limit]:  # Print first `file_limit` files
                if not any(item.endswith(ex) for ex in exclude_files):
                    tree_structure += prefix + item + "\n"
            tree_structure += prefix + f"... ({len(files) - file_limit * 2} more files skipped)" + "\n"
            for item in files[-file_limit:]:  # Print last `file_limit` files
                if not any(item.endswith(ex) for ex in exclude_files):
                    tree_structure += prefix + item + "\n"
        else:
            for item in files:
                if not any(item.endswith(ex) for ex in exclude_files):
                    tree_structure += prefix + item + "\n"
                
    except PermissionError:
        pass  # Handle directories you don't have access to

    return tree_structure

# Function to collect all files of a specific type
def collect_files_by_type(root_dir, file_extension, relative_to):
    collected_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(file_extension):
                relative_path = os.path.relpath(os.path.join(dirpath, filename), relative_to)
                collected_files.append(relative_path)
    return collected_files

# Function to read the contents of collected files
def read_file_contents(root_dir, file_paths):
    file_contents = {}
    for file_path in file_paths:
        full_path = os.path.join(root_dir, file_path)
        try:
            with open(full_path, "r", encoding="utf-8") as file:
                file_contents[file_path] = file.read()
        except Exception as e:
            file_contents[file_path] = f"Error reading file: {e}"
    return file_contents

# Function to handle uploaded zip files and extract them
def handle_zip_file(uploaded_zip):
    with zipfile.ZipFile(uploaded_zip, "r") as zip_ref:
        extract_dir = Path("extracted_repo")
        zip_ref.extractall(extract_dir)
        return extract_dir

# Streamlit App
st.title("Directory to Text: LLM Prompting")

# File uploader for directory or file
uploaded_file = st.file_uploader("Upload a file or a zipped directory", type=["zip", "py", "jl", "txt"])

# Components for exclusions and settings in the main body
st.header("Filter Options")

exclude_files = st.multiselect(
    "Exclude Files (by extension)", 
    options=[".DS_Store", ".png", ".jpg", ".git", ".ipynb", ".mp4", ".md"],
    default=[".DS_Store", ".git"]
)

exclude_dirs = st.multiselect(
    "Exclude Directories", 
    options=["__MACOSX", ".git", "output", "assets", ".idea", "__pycache__"],
    default=["__MACOSX", ".git"]
)

# Set the limit for number of files shown per folder
file_limit = st.slider("Number of files to show at the start and end of large folders", 1, 10, 2)

# File type to collect
file_extension = st.text_input("File extension to collect (e.g., .jl)", value=".jl")

# Prompt for LLM
st.header("LLM Prompt")
llm_prompt = st.text_area(
    "Enter the prompt you would like to include for the LLM (e.g., 'Please provide code insights on the following repository structure and files...')",
    value="Please provide code insights on the following repository structure and files:"
)

if uploaded_file is not None:
    # Check if the uploaded file is a ZIP file (which would be a directory)
    if uploaded_file.name.endswith('.zip'):
        st.success(f"Zipped directory uploaded: {uploaded_file.name}")
        extract_dir = handle_zip_file(uploaded_file)

        # Generate and display the filtered tree structure with file truncation
        st.subheader("Filtered Tree Structure:")
        tree_structure = generate_tree_structure(extract_dir, exclude_files, exclude_dirs, file_limit=file_limit)
        st.text(tree_structure)

        # Collect and display files of the specified type
        st.subheader(f"Files with extension {file_extension}:")
        collected_files = collect_files_by_type(extract_dir, file_extension, extract_dir)
        if collected_files:
            st.text("\n".join(collected_files))
        else:
            st.text(f"No files with extension {file_extension} found.")

        # Read the contents of the collected files
        st.subheader(f"Contents of {file_extension} files:")
        file_contents = read_file_contents(extract_dir, collected_files)
        for file_path, content in file_contents.items():
            st.text(f"\n{file_path}:\n")
            st.code(content)

        # Combine all output, including the LLM prompt
        full_output = llm_prompt + "\n\n" + "------------\n"
        full_output += tree_structure + "\n------------\n" + f"Files with extension {file_extension}:\n" + "\n".join(collected_files)
        full_output += "\n------------\n" + "Contents of files:\n"
        for file_path, content in file_contents.items():
            full_output += f"\n{file_path}:\n{content}\n"
        full_output += "\n------------\nThis input is designed for providing code insights with an LLM.\n"

        # Option to download the filtered tree structure, file list, and file contents as a text file
        if st.button("Download LLM Context"):
            tree_file = f"llm_context_{uploaded_file.name}.txt"
            with open(tree_file, "w") as f:
                f.write(full_output)
            with open(tree_file, "rb") as f:
                st.download_button(
                    label="Download LLM Context",
                    data=f,
                    file_name=tree_file,
                    mime="text/plain"
                )
        
        # Button to copy the entire output to clipboard
        if st.button("Copy to Clipboard"):
            pyperclip.copy(full_output)
            st.success("The content has been copied to your clipboard!")

    else:
        st.success(f"File uploaded: {uploaded_file.name}")
        file_content = StringIO(uploaded_file.getvalue().decode("utf-8"))
        st.text(file_content.read())