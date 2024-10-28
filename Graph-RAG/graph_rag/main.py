import streamlit as st
from graph_rag.agent import agent_with_chat_history,config
import time
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.header("SARA: Your Political Analyst and Assistant")

# Function to add a message to the chat history and display it
def add_and_display_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})
    with st.chat_message(role):
        st.write_stream(stream_data(content))
        

# Display initial message if chat is empty
if not st.session_state.messages:
    response = agent_with_chat_history.invoke({"input": "Greet the user and suggest some sample topics"}, config)['output']
    add_and_display_message("👩‍💻", response)
else:
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# React to user input
user_message = st.chat_input()
sentiment_mapping = [":material/thumb_down:", ":material/thumb_up:"]

if user_message:
    # Display user message
    add_and_display_message("user", user_message)

    # Get and display assistant response
    with st_lottie_spinner("https://lottie.host/0cb9f979-55c9-470b-a2a7-394c52bfb395/MJXZu1gkRD.json",width=100):
        response = agent_with_chat_history.invoke({"input": user_message}, config)['output']
    add_and_display_message("👩‍💻", response)
    selected = st.feedback("thumbs")
    if selected is not None:
        # st.markdown(f"Your response is saved: {sentiment_mapping[selected]}")
        st.success('Recored your response!👩‍💻', icon="✅")
            








# def stream_data(text):
#     for word in text.split(" "):
#         yield word + " "
#         time.sleep(0.02)

# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []


# st.header("SARA: Your Political Analyst and Assistant")
# # with st.sidebar:
# #     if st.button("New Chat"):
# #         st.session_state.messages=[]
#     # input_images=st.file_uploader('Upload screenshots or images files',type=['txt','jpg'],accept_multiple_files=True)
#     # if st.button("Upload"):
#     #     ingest_images(input_images)


# if st.session_state.messages == []:
#     with st.chat_message("👩‍💻"):
#         response=agent_with_chat_history.invoke({"input":"Greet the user and suggest some sample topics"},config)['output']
#         st.write_stream(stream_data(response))


# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # React to user input
# user_message=st.chat_input()
# if user_message is not None:
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(user_message)
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": user_message})


#     response=agent_with_chat_history.invoke({"input":user_message},config)['output']
        
#     # Display assistant response in chat message container
#     with st.chat_message("👩‍💻"):
#         st.write_stream(stream_data(response))
#     # Add assistant response to chat history
#     st.session_state.messages.append({"role": "👩‍💻", "content": response})






# user_message=st.chat_input()

# if user_message is not None:
#     with st.chat_message("user"):
#         st.markdown(user_message)
#     with st.chat_message("👩‍💻"):
#         # with st.spinner():
#         response=agent_with_chat_history.invoke({"input":user_message},config)['output']
#         st.write_stream(stream_data(response))
#         # st.markdown(response)