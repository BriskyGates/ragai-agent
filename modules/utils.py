#!/usr/bin/env python

# Ragai - (c) Eric Dodémont, 2024.

"""
Miscellaneous functions, including function to chunk and embed files.
"""

# Only to be able to run on Github Codespace
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import shutil
from langchain_community.document_loaders import JSONLoader, PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import chromadb
from chromadb.config import Settings
import os

from config.config import *


def load_files_and_embed(json_file_paths: list, pdf_file_paths: list, embed: bool) -> None:
    """
    Loads and chunks files into a list of documents then embed
    """

    try:

        embedding_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)

        chroma_server_password = os.getenv("CHROMA_SERVER_AUTHN_CREDENTIALS", "YYYY")
        chroma_client = chromadb.HttpClient(host=CHROMA_SERVER_HOST, port=CHROMA_SERVER_PORT, settings=Settings(chroma_client_auth_provider="chromadb.auth.token_authn.TokenAuthClientProvider", chroma_client_auth_credentials=chroma_server_password))

        nbr_files = len(json_file_paths)
        st.write(f"Number of JSON files: {nbr_files}")
        j = 0  # Number of JSON files
        i = 0  # Number of JSON items / Web pages
        for json_file_path in json_file_paths:
            j = j + 1
            loader = JSONLoader(file_path=json_file_path, jq_schema=".[]", text_content=False)
            docs = loader.load()
            i = i + len(docs)
            if embed:
                st.write(f"Duration: {(j/60):.2f}/{int(nbr_files/60)} minutes -- JSON files: {j}/{nbr_files} -- Web pages: {i}")  # If 1 second per embedding
                if len(docs) != 0:  # Or else there is an error
                    Chroma.from_documents(docs, embedding=embedding_model, collection_name=CHROMA_COLLECTION_NAME, client=chroma_client)
        st.write(f"Number of Web pages: {i}")

        nbr_files = len(pdf_file_paths)
        st.write(f"Number of PDF files: {nbr_files}")
        j2 = 0
        i2 = 0
        if pdf_file_paths:  # if equals to "", then skip
            for pdf_file_path in pdf_file_paths:
                j2 = j2 + 1
                loader = PyPDFLoader(pdf_file_path)
                pages = loader.load_and_split()  # 1 pdf page per chunk
                i2 = i2 + len(pages)
                if embed:
                    st.write(f"Duration: {(j2/60):.2f}/{int(nbr_files/60)} minutes -- PDF files: {j2}/{nbr_files} -- PDF pages: {i2}")  # If 1 second per embedding
                    Chroma.from_documents(pages, embedding=embedding_model, collection_name=CHROMA_COLLECTION_NAME, client=chroma_client)
        st.write(f"Number of PDF pages: {i2}")
        st.write(f"Number of Web pages and PDF pages: {i + i2}")

    except Exception as e:
        st.write("Error: The Chroma vector DB is not available locally. Is it running on a remote server?")
        st.write(f"Error: {e}")


def delete_directory(dir_path):
    try:
        shutil.rmtree(dir_path)
        print(f"Directory '{dir_path}' and all its contents have been deleted successfully")
    except FileNotFoundError:
        print(f"Error: Directory '{dir_path}' does not exist")
    except PermissionError:
        print(f"Error: Permission denied to delete '{dir_path}'")
    except Exception as e:
        print(f"Error: {e}")
