import streamlit as st
import openai
import os
import json
from prompts import journal_prompt
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("JournAI: Reflective Journal Assistant")

def get_sentiment_label(entry):
    sentiment_prompt = f"""
Classify the sentiment of this journal entry as 'positive', 'neutral', or 'negative'.

Entry:
\"\"\"{entry}\"\"\"

Label:
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": sentiment_prompt}
        ]
    )
    label = response['choices'][0]['message']['content'].strip().lower()
    return label

def save_entry(entry_text, response_text):
    log = {
        "timestamp": datetime.now().isoformat(),
        "entry": entry_text,
        "response": response_text
    }
    with open("journal_log.jsonl", "a") as f:
        f.write(json.dumps(log) + "\n")


entry = st.text_area("What's on your mind today?", height=200)



if st.button("Reflect"):
    if entry.strip():
        with st.spinner("Thinking..."):
            response = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = [
                    {"role": "user", "content": journal_prompt(entry)}
                ]
            )
            reply = response['choices'][0]['message']['content'].strip()
            sentiment = get_sentiment_label(entry)
            st.success("Here's your reflection:")
            st.write(reply)
            st.markdown(f"**Sentiment Analysis:** {sentiment}")
            save_entry(entry, reply)
    else:
        st.warning("Please enter a journal entry before reflecting.")