# Directory to Text: LLM Prompting

**Directory to Text: LLM Prompting** is a Streamlit app designed to assist with generating a textual representation of a directory structure for use as input to Large Language Models (LLMs). This app allows you to upload a zipped directory of code files, filter out unnecessary files or directories, and generate a structured text output designed to provide context to an LLM for code insights and analysis.

## Features

- **Directory Structure Visualization**: Upload a zipped directory, and the app will generate a tree structure showing the hierarchy of the files and folders.
- **File Type Filtering**: Easily exclude files or directories that are irrelevant for LLM insights (e.g., `.DS_Store`, `.git`).
- **Display of Code Files**: Collect files of a specific extension (e.g., `.jl`, `.py`, etc.), and view their contents directly in the app.
- **LLM-Friendly Prompt Generation**: Include your custom prompt for the LLM to provide guidance on the type of insights you're seeking, and the prompt will be incorporated into the generated output.
- **Download and Clipboard**: Download the full structured output as a `.txt` file or copy it directly to your clipboard.

## How It Works

1. **Upload a Zipped Directory**: Upload a `.zip` file containing your code repository.
2. **Filter Options**:
   - Exclude specific file types or directories that are not relevant.
   - Specify the number of files to display in large directories.
   - Specify a file extension to extract and display specific code files.
3. **Enter an LLM Prompt**: Provide a prompt to instruct the LLM on how to interpret the directory and code structure.
4. **Generate Output**:
   - The app will generate a text file that includes your LLM prompt, a tree structure of the directory, and the contents of relevant code files.
5. **Download or Copy**: Download the generated text file or copy it to your clipboard for easy sharing with LLMs.

## Usage

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/directory-to-text-llm-prompting.git
   cd directory-to-text-llm-prompting
   ```
Using the App on Streamlit

You can also use the app directly on Streamlit without installation. Visit the live app at:

Streamlit App

Functionality Walkthrough

	1.	File Upload: Drag and drop a .zip file containing your project or select a file from your file explorer.
	2.	Filter Options:
	•	Exclude Files/Directories: Choose from a list of common files or directories (e.g., .git, .DS_Store, __MACOSX, etc.) to exclude from the tree structure and file content output.
	•	Limit Displayed Files: For directories with many files (e.g., 100+ images), you can limit how many files are shown from the start and end of the directory.
	•	Collect Specific File Types: Enter a file extension to collect and display specific files (e.g., .py, .jl, .txt).
	3.	LLM Prompt: Add your custom prompt at the top of the text output to give the LLM specific instructions (e.g., “Analyze the repository structure for dependencies between modules”).
	4.	Generate and Download: Once you’ve uploaded the directory and added the LLM prompt, click the button to download the full .txt file or copy it to your clipboard.
