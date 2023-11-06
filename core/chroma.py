#!/usr/bin/env python
# coding: utf-8

# All imports

import pickle
import pandas as pd
import zipfile
import os
import time
import warnings
import chromadb
import streamlit as st
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
warnings.filterwarnings("ignore")
import shutil
from io import BytesIO
import base64  # Import the base64 module


def st_server_file():
    '''
    Assume each file stored in streamlit server is in embeddings folder, titled embedding0, embedding1 and so on
    Objective: Find largest integer in filename in particular directory, add 1 and form new folder, along with the new file path.
    '''

    # Initialize directory_path variable (containing master folder where all embeddings are saved)
    # and new_directory_name variable containing the new folder for that particular iteration
    directory_path = "embeddings_source/"
    new_directory_name = None

    # Check if the "embeddings" folder (master folder) exists, and if not, create it
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        new_directory_name = "embedding0"

    # List all directories in the "embeddings" directory
    directories = os.listdir(directory_path)

    # Filter  directories that start with "embedding" (8 characters) and are followed by digits
    numeric_directories = [dirname for dirname in directories if dirname.startswith("embedding") and dirname[9:].isdigit()]

    # If there is a list like that
    if numeric_directories:

        # Sort the numeric directory names in descending order
        sorted_directories = sorted(numeric_directories, key=lambda x: int(x[9:]), reverse=True)
        
        # The first element in the sorted list will be the largest directory name
        largest_directory = sorted_directories[0]
        
        # Extract the numeric part of the largest directory name and increment it by 1
        largest_number = int(largest_directory[9:])

        # This is finding the new_number for the new directory name
        new_number = largest_number + 1
        
        # Create the new directory name with the incremented number
        new_directory_name = f"embedding{new_number}"

    # If new_directory_name is set, create the new directory
    if new_directory_name:

        new_directory_path = os.path.join(directory_path, new_directory_name)
        os.makedirs(new_directory_path)

    # Print out the new directory path
    # print(f"Created new directory: {new_directory_path}")


    # Diagnostic till now
    # Print the largest directory name and the new directory name (if created)
    
    # if largest_directory:
    #     print(f"The largest directory name is: {largest_directory}")
    
    # if new_directory_name:
    #     print(f"The new directory name is: {new_directory_name}")

    # Write info of Directory path and Directory name - Diagnostic

    # st.write(f"Master folder where all directories are stored: {directory_path}")
    # st.write(f"Directory path where result will be stored: {new_directory_path}")
    # st.write(f"New Directory (Folder) name: {new_directory_name}")

    return directory_path, new_directory_path, new_directory_name

def check_zipfile_directory():

    # Check if the "zipfiles" folder exists, and if not, create it
    directory_path = "zipfiles/"
    new_directory_name = None
    new_directory_path = None

    # Check if the "embeddings" folder (master folder) exists, and if not, create it
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        new_directory_name = "embedding0"

    # List all directories in the "embeddings" directory
    directories = os.listdir(directory_path)

    # Filter  directories that start with "embedding" (8 characters) and are followed by digits
    numeric_directories = [dirname for dirname in directories if dirname.startswith("embedding") and dirname[9:].isdigit()]

    # If there is a list like that
    if numeric_directories:

        # Sort the numeric directory names in descending order
        sorted_directories = sorted(numeric_directories, key=lambda x: int(x[9:]), reverse=True)
        
        # The first element in the sorted list will be the largest directory name
        largest_directory = sorted_directories[0]
        
        # Extract the numeric part of the largest directory name and increment it by 1
        largest_number = int(largest_directory[9:])

        # This is finding the new_number for the new directory name
        new_number = largest_number + 1
        
        # Create the new directory name with the incremented number
        new_directory_name = f"embedding{new_number}"

    # If new_directory_name is set, create the new directory
    if new_directory_name:

        new_directory_path = os.path.join(directory_path, new_directory_name)
        os.makedirs(new_directory_path)

    # Write info of Directory path and Directory name - Diagnostic

    # st.write(f"Master folder where all directories are stored: {directory_path}")
    # st.write(f"Directory path where result will be stored: {new_directory_path}")
    # st.write(f"New Directory (Folder) name: {new_directory_name}")

    return directory_path, new_directory_path, new_directory_name



def upload_zip_files():

    # Create a temporary directory, called zipfiles, for storing uploaded ZIP files
    # temp_dir = "zipfiles"
    # os.makedirs(temp_dir, exist_ok=True)

    # Upload ZIP files
    uploaded_zip_file = st.file_uploader('Upload a ZIP file', type="zip")

    return uploaded_zip_file


def write_zip_files_to_directory(uploaded_zip_file, chroma_file_path):

    # If files are uploaded
    if uploaded_zip_file is not None:

        # Determine the full path to save the ZIP file
        zip_file_path = os.path.join(chroma_file_path, uploaded_zip_file.name)


        # Save the uploaded ZIP file to the temporary directory
        with open(zip_file_path, "wb") as f:
            f.write(uploaded_zip_file.read())

        # chroma_file_path = os.path.abspath(unique_filename)

        st.success(f"ZIP file '{uploaded_zip_file.name}' uploaded and saved to: {chroma_file_path}", icon="✅")

        # Unzip the uploaded ZIP file
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:

            # Extract ZIP file to same directory
            zip_ref.extractall(chroma_file_path)

        # st.success(f"ZIP file '{uploaded_zip_file.name}' successfully extracted in: {chroma_file_path}")



def print_files_in_particular_directory(directory):

    # List all files in the directory
    files = os.listdir(directory)

    st.write(f"Checking files: {files}")
    st.write(f"Printing files in this directory: {directory}")

    # Print the list of filenames
    for filename in files:
        st.write(filename)

def print_files_in_directory(directory):
    st.write(f"Printing files in this directory and its subdirectories: {directory}")

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            st.write(file_path)

def download_embedding_zip(directory, zip_filename):
    # st.write(f"Creating a zip file of all files in this directory and its subdirectories: {directory}")

    zip_buffer = BytesIO()

    # shutil.make_archive(zip_buffer, 'zip', directory)

    # Create a zip archive in memory
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:

        # foldername: Path to current folder being processed
        # subfolders: List of subdirectory names within current folder
        # filenames: List of file names within current folder

        for foldername, subfolders, filenames in os.walk(directory):

            for filename in filenames:

                # Create the full file path
                file_path = os.path.join(foldername, filename)

                # How would you refer to the file from within the directory (without including the full path)
                # Maintains structure 
                arcname = os.path.relpath(file_path, directory)

                # Arcname specifies name to be used for file within ZIP archive
                zipf.write(file_path, arcname)

    # st.write("Zip file created successfully")

    # Seek back to the beginning of the BytesIO object
    zip_buffer.seek(0)

    # Generate the data URI for the ZIP file
    data_uri = f"data:application/zip;base64,{base64.b64encode(zip_buffer.read()).decode()}"

    # Create download link
    download_link = f"<a href='{data_uri}' download='{zip_filename}.zip'>Download embeddings zip file</a>"
    st.markdown(download_link, unsafe_allow_html=True) # Display the custom download link


    # Download zip file via button
    # For zip file, use MIME type = “application/zip”
    # For rar and 7z file, use MIME type = “application/octet-stream”
    # zip_file_download = st.download_button(
    #         label = "Download zip file",
    #         data = zip_buffer.read(),
    #         file_name = f"{zip_filename}.zip",
    #         mime = "application/zip"
    #     )


def download_embedding_old(chroma_file_path):

    # Check if the file "chroma.sqlite3" exists in the directory
    exact_chroma_file_path = os.path.join(chroma_file_path, 'chroma.sqlite3')

    if os.path.exists(exact_chroma_file_path):
        # st.markdown("### Download the SQLite Database")
        # st.write("Click the button below to download the 'chroma.sqlite3' file:")

        # Create a download button
        # st.download_button(label="Download embedding", data = exact_chroma_file_path, key='download_embedding', mime = "application/vnd.sqlite3", help = "Download embeddings")
        # Create a custom download link using HTML

        # MIME type: application/vnd.sqlite3 (did not work)
        # MIME type: application/x-sqlite3 (did not work)
        # MIME type: application/sqlite3 (did not work)

        with open(exact_chroma_file_path, "rb") as fp:
            btn = st.download_button(
                label = "Download db file",
                data = fp,
                file_name = "chroma.sqlite3",
                mime = "application/vnd.sqlite3"
            )

        
        # download_link = f'<a href="{exact_chroma_file_path}" download="chroma.sqlite3" target="_blank" type="application/sqlite3">Download chroma.sqlite3</a>'
        # st.markdown(download_link, unsafe_allow_html=True) # Display the custom download link



# Create/Get ChromaDB collection
@st.cache_resource(show_spinner = False)
def create_or_get_chroma_db(chroma_file_path):

    # Writing chroma_file_path - Diagnostic
    # st.write(chroma_file_path)

    # Chroma will store its database files on disk, and load them on start
    db = chromadb.PersistentClient(path = chroma_file_path)

    # Create a client
    chroma_client = chromadb.EphemeralClient()

    # Get a collection object from an existing collection, by the name "quickstart". If it doesn't exist, create it.
    chroma_collection = db.get_or_create_collection("embeddings")

    # set up ChromaVectorStore and load in the collection object
    vector_store = ChromaVectorStore(chroma_collection = chroma_collection)

    # Set vector_store as a StorageContext attribute
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    return vector_store, storage_context


# Create ChromaDB collection
@st.cache_resource(show_spinner = False)
def create_chroma_db(chroma_file_path):

    try:

        # Chroma will store its database files on disk, and load them on start
        db = chromadb.PersistentClient(path = chroma_file_path)

        # Create a client
        chroma_client = chromadb.EphemeralClient()

        # Get a collection object from an existing collection, by the name "embeddings". If it doesn't exist, create it.
        chroma_collection = db.create_collection("embeddings")

        # set up ChromaVectorStore and load in the collection object
        vector_store = ChromaVectorStore(chroma_collection = chroma_collection)

        # Set vector_store as a StorageContext attribute
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        return vector_store, storage_context
    
    except Exception as e:

        st.warning(f'''An error occurred while creating embeddings: {str(e)}''')
        st.stop()

# Get ChromaDB collection
@st.cache_resource(show_spinner = False)
def get_chroma_db(chroma_file_path):

    try:

        # Chroma will store its database files on disk, and load them on start
        db = chromadb.PersistentClient(path = chroma_file_path)

        # Create a client
        chroma_client = chromadb.EphemeralClient()

        # Get a collection object from an existing collection, by the name "embeddings". If it doesn't exist, create it.
        chroma_collection = db.get_collection("embeddings")

        # set up ChromaVectorStore and load in the collection object
        vector_store = ChromaVectorStore(chroma_collection = chroma_collection)

        # Set vector_store as a StorageContext attribute
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        return vector_store, storage_context
    
    except Exception as e:

        st.warning(f'''An error occurred while retrieving embeddings: {str(e)}
        Please make sure you loaded the correct embeddings for the relevant pdf files. The program will create new embeddings for this iteration''')

        # Chroma will store its database files on disk, and load them on start
        db = chromadb.PersistentClient(path = chroma_file_path)

        # Create a client
        chroma_client = chromadb.EphemeralClient()

        # Get a collection object from an existing collection, by the name "quickstart". If it doesn't exist, create it.
        chroma_collection = db.get_or_create_collection("embeddings")

        # set up ChromaVectorStore and load in the collection object
        vector_store = ChromaVectorStore(chroma_collection = chroma_collection)

        # Set vector_store as a StorageContext attribute
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        return vector_store, storage_context
