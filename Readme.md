# RFX Document Retrieval and Chatbot
The script provides a commandline interface that allows users to interact with a set of RFX (Request for Proposals, Quotes, etc.) documents. The script is powered by GPT-4o-mini integrated with Langchain for document retrieval and Langsmith for monitoring the retrieval trace.

## Features:
- Loads and processes PDF RFX documents.
- Embeds the documents using OpenAI embeddings.
- Retrieves document content using Chroma vector store for context-aware question answering.
- Interacts with users to answer questions based on retrieved document content.
- Maintains chat history for improved conversation flow.

## Contents:
1. [Environment Variables](#environment-variables)
2. [How to Run](#how-to-run)

## Environment Variables
Ensure first that Python 3.9+ is installed. The script was made using Python 3.9.6. Then install the required libraries using:
    pip install -r requirements.txt

Next, head over to the ".env" file and set the environment variables. 
 1. Ensure to add the correct OpenAI and LangSmith Secret API Keys.
 2. Set Tracing to true and add a project name.

## How to Run
The file structure should look like this:

- **RFX_DOCS/**: Contains the RFX documents in PDF format.
- **app.py**: Main script to load documents, embed them, and run the application.
- **requirements.txt**: Lists all necessary dependencies to install.
- **.env**: Stores environment variables, including OpenAI and Langsmith API keys.
- **Readme.md**: Provides information about the project, installation instructions, and usage guidelines.

To run the script simply run the app.py file as:
    python app.py


