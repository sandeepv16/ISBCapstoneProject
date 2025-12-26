import streamlit as st
import google.generativeai as genai
import configparser
import llm
import time
# Page configuration
# st.set_page_config(page_title="Gemini Chatbot", page_icon="💬")
# import logging 
config = configparser.ConfigParser()


config.read('config.ini')

context = config["GENERAL"]["request_prompt"]

host = config["POSTGRES"]["host"]
port = config["POSTGRES"]["port"]
user = config["POSTGRES"]["user"]
password = config["POSTGRES"]["password"]

# st.set_page_config(page_title="Ask Me Anything", layout="wide")
st.markdown("<h4 style='color: black;'>💬 Ask your queries below</h4>", unsafe_allow_html=True)

# st.title("")

response_prompt = config["GENERAL"]["response_prompt"]

# Set up Gemini API key
genai.configure(api_key= config["GENERAL"]["gemini_api_key"])

st.markdown(
    """
    <style>
    .chat-container {
        background-color: #f7f7f7;
        border-radius: 10px;
        padding: 20px;
        max-height: 500px;
        overflow-y: auto;
    }
    .user-message {
        background-color: #d1e7ff;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: right;
    }
    .bot-message {
        background-color: #e9ecef;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: left;
    }
    .input-box {
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("Chatbot Settings")

model = genai.GenerativeModel('gemini-1.5-flash-8b')
# chat = model.start_chat()
# chat.send_message(context)



# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


faqs = [
        "What is the purpose of this chatbot?",
        "List details of all the images updated in the last 1 week",
        "What are the key features?",
        "whats the total available number of pipes?"
    ]


with st.sidebar:
    st.header("Chatbot Settings")
    model_choice = st.selectbox("Select Model", [
        "gemini-1.5-flash"
    ])
    # temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    # max_tokens = st.slider("Max Tokens", 100, 8192, 2000)

st.sidebar.subheader("Frequently Asked Questions")
temperature = 0.7
max_tokens= 3000
for faq in faqs:
    if st.sidebar.button(faq):
        # When an FAQ is clicked, set it as the user input
        st.session_state.user_input = faq


# Function to generate AI response
def get_gemini_response(messages, model_name, temperature, max_tokens):
    try:
        # Initialize the model
        # model = genai.GenerativeModel(model_name)
        
        # Prepare the chat history
        chat_history = [
            {"role": msg["role"], "parts": [msg["content"]]} 
            for msg in messages
        ]
        
        # Start a chat session
        chat = model.start_chat(history=chat_history)
        
        # Generate response with specified parameters
        response = chat.send_message(
            messages[-1]["content"],
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens
            )
        )
        
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"
    
# # Display chat messages
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])
def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

# Function to generate AI response
def get_gemini_response(messages, model_name, temperature, max_tokens):
    try:
        # Initialize the model
        # model = genai.GenerativeModel(model_name)
        
        # Prepare the chat history
        chat_history = [
            {"role": msg["role"], "parts": [msg["content"]]} 
            for msg in messages
        ]
        
        # Start a chat session
        chat = model.start_chat(history=chat_history)
        
        # Generate response with specified parameters
        response = chat.send_message(
            messages[-1]["content"],
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens
            )
        )
        
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

# # Display chat messages
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# Chat input


if st.session_state.get('user_input'):
    prompt = st.session_state.user_input
    st.session_state.messages.append({"role": "user", "content": context})
    st.session_state.messages.append({"role": "user", "content": prompt})
    print(prompt)
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Get AI response
        full_response = get_gemini_response(
            st.session_state.messages, 
            model_choice, 
            temperature, 
            max_tokens
        )
        print(full_response)
        
        try:
            results = llm.getDataFromSQL(host = host,user=user , password=password,port=port, query=full_response.replace("`","").replace("sql",""))
        

            rp = response_prompt.format(prompt, full_response, results)

            st.session_state.messages.append({"role": "user", "content": rp})

            full_response = get_gemini_response(
                st.session_state.messages, 
                model_choice, 
                temperature, 
                max_tokens
            )
            print(full_response)
            
            # Display and store the response
            message_placeholder.markdown((full_response))
            st.session_state.messages.append({
                "role": "assistant", 
                "content": full_response
            })

        except:
            message_placeholder.markdown((full_response))
    st.session_state.user_input = None # Reset the FAQ-triggered input

# prompt 
    

if prompt:= st.chat_input("Enter your message"):
    # Add user 
    # message to chat history

    st.session_state.messages.append({"role": "user", "content": context})
    st.session_state.messages.append({"role": "user", "content": prompt})
    print(prompt)
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Get AI response
        full_response = get_gemini_response(
            st.session_state.messages, 
            model_choice, 
            temperature, 
            max_tokens
        )
        print(full_response)
        
        try:
            results = llm.getDataFromSQL(host = host,user=user , password=password,port=port, query=full_response.replace("`","").replace("sql",""))
        
            print(results)
            rp = response_prompt.format(prompt, full_response, results)

            st.session_state.messages.append({"role": "user", "content": rp})

            full_response = get_gemini_response(
                st.session_state.messages, 
                model_choice, 
                temperature, 
                max_tokens
            )
            print(full_response)
            
            # Display and store the response
            message_placeholder.markdown((full_response))
            st.session_state.messages.append({
                "role": "assistant", 
                "content": full_response
            })

        except Exception as e:
            print(str(e))
            message_placeholder.markdown((full_response))


# # Display chat messages
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):

#         st.markdown(message["content"])


if st.button("Back to Home"):
        st.switch_page("streamlit.py")

# Clear chat history button
if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
