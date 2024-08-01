#!/usr/bin/env python

# RagAiAgent - (c) Eric Dodémont, 2024.

"""
This function runs the frontend web interface.
"""

import streamlit as st
from langchain_core.messages.human import HumanMessage
import uuid
import asyncio

from modules.assistant_backend import instanciate_ai_assistant_graph_agent
from config.config import *


# Function defined in two files: should be moved in a module
def reset_conversation():
    """
    Reset the conversation: new thread id + clear the screen
    """

    st.session_state.messages = []
    st.session_state.threadId = {"configurable": {"thread_id": uuid.uuid4()}}


def assistant_frontend():
    """
    Everything related to Streamlit for the main page (about & chat windows) and connection with the Langchain backend.
    """

    st.set_page_config(page_title=ASSISTANT_NAME, page_icon=ASSISTANT_ICON)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.threadId = {"configurable": {"thread_id": uuid.uuid4()}}

    if "model" not in st.session_state:
        st.session_state.model = DEFAULT_MODEL

    if "temperature" not in st.session_state:
        st.session_state.temperature = DEFAULT_TEMPERATURE

    if "password_ok" not in st.session_state:
        st.session_state.password_ok = False

    if "input_password" not in st.session_state:
        st.session_state.input_password = ""

    # Retrieve and generate

    ai_assistant_graph_agent = instanciate_ai_assistant_graph_agent(st.session_state.model, st.session_state.temperature)

    # Write the mermaid graph in the graph.txt file (to be displayed in https://mermaid.live/)
    with open("graph.txt", "w") as f:
        f.write(ai_assistant_graph_agent.get_graph().draw_mermaid())    
    f.close()

    # # # # # # # #
    # Main window #
    # # # # # # # #

    st.image(LOGO_PATH, use_column_width=True)

    st.markdown(f"## {ASSISTANT_NAME}")
    st.caption("💬 A chatbot powered by Langchain, Langgraph and Streamlit")

    # # # # # # # # # # # # # #
    # Side bar window (About) #
    # # # # # # # # # # # # # #

    with st.sidebar:

        st.write(f"Model: {st.session_state.model} ({st.session_state.temperature})")
        st.write(ABOUT_TEXT)
        st.write(SIDEBAR_FOOTER)

    # # # # # # # # # # # #
    # Chat message window #
    # # # # # # # # # # # #

    with st.chat_message("assistant"):
        st.write(HELLO_MESSAGE)

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # React to user input
    if question := st.chat_input(USER_PROMPT):
        # Display user message in chat message container
        st.chat_message("user").markdown(question)
        # Add question to Streamlit chat history (messages) 
        st.session_state.messages.append({"role": "user", "content": question})

        #try:

        # Call the agent

        if st.session_state.model in (VERTEXAI_MENU):

            # Display last AIMessage (final answers) / No tokens streaming

            response = ai_assistant_graph_agent.invoke({"messages": [HumanMessage(content=question)]}, config=st.session_state.threadId)
            answer = response["messages"][-1].content                
            st.chat_message("assistant").markdown(answer)

        elif st.session_state.model in (ANTHROPIC_MENU):

            # Display all AIMessage (intermediary and final answers) + tool calls / No tokens streaming
            
            for message in ai_assistant_graph_agent.stream({"messages": [HumanMessage(content=question)]}, config=st.session_state.threadId, stream_mode="values"):
                message_type1 = type(message["messages"][-1]).__name__  # HumanMessage, AIMessage, ToolMessage
                message_type2 = type(message["messages"][-1].content).__name__  # str only for last AIMessage, else dict
                if message_type1 == "AIMessage" and message_type2 == "str":
                    answer = message["messages"][-1].content  # Last AIMessage = Final answer
                    st.chat_message("assistant").markdown(answer)
                elif message_type1 == "AIMessage":
                    data = message["messages"][-1].content
                    answer = data[0]["text"]
                    st.chat_message("assistant").markdown(answer)
                    for item in data[1:]:
                        if "name" in item:
                            answer = item["name"]
                            st.chat_message("tool").markdown(f"Tool call: {answer}")
                    
        elif st.session_state.model in (OPENAI_MENU):

            # Display last AIMessage (final answer) / Tokens streaming

            # Not streaming (sync): invoke
            # Streaming (sync): stream (messages or tokens)
            # Streaming (async): astream_events

            # NOK with Anthropic async/event: if tokens streaming, the answer is a list of dictionaries (NOK),
            # in place of a string (OK). Also a problem with Google VertexAI.
            
            async def agent_answer(question):
                answer = ""
                answer_container = st.empty()
                async for event in ai_assistant_graph_agent.astream_events({"messages": [HumanMessage(content=question)]}, config=st.session_state.threadId, version="v2"):
                    kind = event["event"]
                    if kind == "on_chat_model_stream":
                        answer_token = event["data"]["chunk"].content
                        if answer_token:
                            answer = answer + answer_token
                            answer_container.write(answer)
                return(answer)
            
            answer = asyncio.run(agent_answer(question))

        else: 
            st.session_state.model in (GOOGLE_MENU, OLLAMA_MENU)
            answer_container = st.empty()
            answer_container.write("Error: model not supported")

        # Add answer to Streamlit chat history (messages)
        st.session_state.messages.append({"role": "assistant", "content": answer})

        # Clear the conversation
        st.button(NEW_CHAT_MESSAGE, on_click=reset_conversation)

        #except Exception as e:
        #    st.write("Error: Cannot invoke/stream the agent!")
        #    st.write(f"Error: {e}")
