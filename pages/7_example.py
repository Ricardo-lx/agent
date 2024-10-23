from openai import OpenAI
import streamlit as st

st.title("ChatGPT-like clone")

openrouter_api_key = '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'

client = OpenAI(api_key=openrouter_api_key, base_url="https://openrouter.ai/api/v1")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "meta-llama/llama-3.1-70b-instruct:free"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": message["role"], "content": message["content"]}
                for message in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

st.button("Clear Chat", on_click=lambda: st.session_state.clear())