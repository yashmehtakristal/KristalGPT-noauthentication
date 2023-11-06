# All imports
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st

# Setting page config & header
st.set_page_config(page_title="Kristal Retriever", page_icon="📖", layout="wide", initial_sidebar_state="expanded")
st.header("📖 Kristal Retriever")

import openai
import os
import tempfile
from tempfile import NamedTemporaryFile
from streamlit_extras.app_logo import add_logo
from st_pages import Page, Section, add_page_title, show_pages, hide_pages
from database_helper_functions import sign_up, fetch_users
import streamlit_authenticator as stauth

## Importing functions

# from ui import (
#     is_query_valid,
#     display_file_read_error,
# )

# from bundle import no_embeddings_process_documents, embeddings_process_documents
# from core.loading import read_documents_from_directory, iterate_files_from_directory, save_uploaded_file, read_documents_from_uploaded_files, get_tables_from_uploaded_file, iterate_files_from_uploaded_files, iterate_excel_files_from_directory, iterate_uploaded_excel_files, print_file_details, show_dataframes, iterate_uploaded_excel_file
# from core.pickle import save_to_pickle, load_from_pickle
# from core.indexing import query_engine_function, build_vector_index
# from core.LLM_preprocessing import conditions_excel, extract_fund_variable, prompts_to_substitute_variable, storing_input_prompt_in_list
# from core.querying import recursive_retriever_old, recursive_retriever
# from core.LLM_prompting import individual_prompt, prompt_loop
# from core.PostLLM_prompting import create_output_result_column, create_output_context_column, intermediate_output_to_excel
# from core.parsing import create_schema_from_excel, parse_value
# from core.Postparsing import create_filtered_excel_file, final_result_orignal_excel_file, reordering_columns
# from core.Last_fixing_fields import find_result_fund_name, find_result_fund_house, find_result_fund_class, find_result_currency, find_result_acc_or_inc, create_new_kristal_alias, update_kristal_alias, update_sponsored_by, update_required_broker, update_transactional_fund, update_disclaimer, update_risk_disclaimer, find_nav_value, update_nav_value 
# from core.output import output_to_excel, download_data_as_excel, download_data_as_csv

# Add the logo to the sidebar
add_logo("https://assets-global.website-files.com/614a9edd8139f5def3897a73/61960dbb839ce5fefe853138_Kristal%20Logotype%20Primary.svg")

show_pages(
    [
        Page("main.py","Login", "🗝️"),
        Page("pages/home.py", "About", "😀"),
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
