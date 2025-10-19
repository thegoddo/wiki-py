# Wiki-Py: Your Terminal's Gateway to Wikipedia

**Video Demo**: https://youtu.be/HbBJ_ZEXRXk

## Project Overview

Wiki-Py is a powerful and intuitive command-line interface (CLI) tool that brings the vast knowledge of Wikipedia directly to your terminal. Built with Python, this application allows users to quickly search, summarize, and view full articles on any topic, all without leaving the comfort of their command line. The tool is designed to be fast, efficient, and user-friendly, providing a rich experience with colorful, easy-to-read output.

## Key Features

    Quick Summaries: Get a concise summary of a topic with a single command. This is perfect for quick fact-checking or getting a general understanding of a subject.

    Full Article Content: For in-depth research, the tool allows you to retrieve the complete text of any Wikipedia article, providing a thorough and comprehensive view of the topic.

    Topic Search: Unsure of the exact article name? Use the search functionality to find a list of the most relevant topics based on your query. This feature is particularly useful for discovering related subjects.

    Multilingual Support: Wiki-Py supports any language available on Wikipedia. Simply specify the language code, and the tool will fetch content in your chosen language, making it a truly global information source.

    Intelligent Disambiguation: The tool is smart enough to handle cases where a topic name is ambiguous (e.g., "Python," which could be a programming language or a snake). Instead of crashing, it gracefully handles these errors by suggesting a list of possible topics, guiding you to the correct article. This directly addresses the need for better support for topics with the same name.

    Colorful, Read-out-Loud Output: The use of the colorama library adds vibrant color to the output, making the information easier to parse and more visually appealing. Titles, summaries, and search results are distinctly styled to enhance readability.

## How to Use

### 1. Setup

First, ensure you have Python installed. Then, install the required libraries: wikipedia and colorama.

`pip install wikipedia colorama`

### 2. Usage Examples

Wiki-Py uses argparse for robust command-line argument handling. Here are some examples of how to use its main functionalities:

`# Get a Summary of a Topic:`
`This is the default behavior when using the -n or --name flag.`

# Get a summary of the 'Python' programming language

`python project.py -n "Python"`

# Get a summary in French

`python project.py -n "Paris" -l "fr"`

`Get the Full Content of an Article:`
`Combine the -n flag with the -f or --full flag to retrieve the complete article text.`

# Get the full article for 'C++'

`python project.py -n "C++" --full`

# Get the full article for 'Albert Einstein' in German

`python project.py -n "Albert Einstein" -l "de" --full`

Search for a Topic:

` Use the -s or --search flag to find a list of topics related to your query.`

# Search for topics related to 'science'

`python project.py -s "science"`

# Search in Spanish for topics on 'art'

` python project.py -s "arte" -l "es"`

Technical Implementation

The project is built on three core libraries:

    wikipedia: The heart of the application, used to programmatically access Wikipedia's content, search for pages, and retrieve summaries.

    argparse: This standard Python library is used to parse command-line arguments, ensuring the application is easy to use with clear flag names and helpful usage messages. The arguments are carefully configured so that -n and -s are mutually exclusive, while the -f flag acts as a modifier for -n.

    colorama: This library provides a simple way to add colors to the terminal output, improving the user's experience by visually separating different types of information.

The code is structured with separate functions for each main action (get_summary, get_full_content, get_results), making the logic clean and easy to maintain. The main function orchestrates the entire process, handling user input, setting the language, and calling the appropriate function based on the provided arguments.
Conclusion

Wiki-Py is a robust and valuable tool for anyone who frequently uses the terminal for work or study. It demonstrates a strong understanding of Python, external libraries, and the creation of user-friendly command-line interfaces. The addition of language support and graceful error handling for disambiguation topics makes it a reliable and production-ready tool.
