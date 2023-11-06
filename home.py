# All imports
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# All imports

import streamlit as st
from streamlit_extras.app_logo import add_logo
from st_pages import Page, Section, add_page_title, show_pages, hide_pages


show_pages(
    [
        Page("home.py","About", "😀"),
        # Section(name = "Bulk Upload", icon="📚"),
        Page("pages/bulk_upload_basic.py", "Bulk Upload - Basic", "📚"),
        Page("pages/bulk_upload_advanced.py", "Bulk Upload - Advanced", "📚"),
        # Section(name = "QA Basic", icon="❓"),
        Page("pages/qa_basic.py", "Q&A - Basic", "❓"),
        Page("pages/qa_advanced.py", "Q&A - Advanced", "❓"),
        # Section(name = "Chatbot", icon="💬"),
        # Page("pages/chatbot_without_memory.py", "Chatbot - Basic", "💬"),
        # Page("pages/chatbot_with_memory.py", "Chatbot - Advanced", "💬")
    ]
)

# Setting page config & header
st.set_page_config(page_title = "Kristal Retriever", page_icon = "📖", layout = "wide", initial_sidebar_state = "expanded")
st.header("📖 Kristal Retriever")

# Add the logo to the sidebar
add_logo("https://assets-global.website-files.com/614a9edd8139f5def3897a73/61960dbb839ce5fefe853138_Kristal%20Logotype%20Primary.svg")


import openai
import os
import tempfile
from tempfile import NamedTemporaryFile
from database_helper_functions import sign_up, fetch_users
import streamlit_authenticator as stauth


# Display Markdown of the main page
st.markdown(
'''
This section will give more information about Kristal GPT. 

This application has 2 main features (Bulk Upload and Q&A). Moreover, it has two high-level categorization (Basic, Advanced) 

Here is the simple categorization of the aforementioned:

- Basic
    - Bulk Upload - Basic
    - Q&A - Basic
- Advanced
    - Bulk Upload - Advanced
    - Q&A - Advanced

### Features explanation

***Bulk Upload:***

This feature allows the user to upload an excel file (or select a template) containing the list of prompts, along with other relevant fields.

***Q&A:***

This feature allows the user to input prompts individually, as if they are "chatting" with the uploaded documents.

### Categorization

***Basic:***

The Basic version of the application has the minimum features required to successfully run the application. These are:

1. Option to save embeddings for current iteration/load saved embeddings
2. Specifying the folder for the embeddings
3. Uploading the pdf files, as well as the excel files.
4. Displaying the results as a dataframe
5. Providing option to download displayed dataframe as a CSV file or Excel file

***Advanced:***

The Advanced version of the application has the same features as the basic, with the addition of the following:

1. Select which LLM model to use
2. Select the number of nodes to retrieve from LLM (during vector search)
3. Select the temperature parameter of LLM
4. Select the request timeout (in seconds) of LLM
5. Select the maximum retries of LLM
6. Select the amount of time for LLM to wait before executing next prompt (in loop)
7. Select whether to display all chunks retrieved from vector search (If no, i.e. default value, will display the chunk that has highest score)
8. Select to show the parsed contents of the document
9. Select to show all tables parsed from the pdf document
'''
)
