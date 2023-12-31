import streamlit as st
import streamlit.components.v1 as components
from langchain import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryMemory

from dataclasses import dataclass
from typing import Literal


from langchain import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryMemory

from langchain.agents import create_csv_agent
agent = create_csv_agent = "https://github.com/Joggyjagz7/test-proactive-chatbot/blob/main/data/jobscomplaint.csv"


@dataclass
class Message:
    """Class for keeping track of a chat message."""
    origin: Literal["customer", "pr pal"]
    message: str

def load_css():
    with open("style/style.css", "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []
    if "token_count" not in st.session_state:
        st.session_state.token_count = 0
    if "conversation" not in st.session_state:
        llm = OpenAI(
            temperature=0,
            openai_api_key=st.secrets["openai_api_key"],
            openai_api_key="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",
            model_name="text-davinci-003"
        )
        st.session_state.conversation = ConversationChain(
            llm=llm,
            memory=ConversationSummaryMemory(llm=llm),
        )

def on_click_callback():
    with get_openai_callback() as cb:
        human_prompt = st.session_state.human_prompt
        llm_response = st.session_state.conversation.run(
            human_prompt
        )
        st.session_state.history.append(
            Message("customer", human_prompt)
        )
        st.session_state.history.append(
            Message("pr pal", llm_response)
        )
        st.session_state.token_count += cb.total_tokens

load_css()
initialize_session_state()

st.title("Proactive Repair Pal 👷‍♀️🛠️")
st.subheader(" ",divider='rainbow')
st.markdown("Welcome to the Proactive Repair Pal Bot. I am a proactive repair chatbot that tracks user tasks/complaints with reference IDs, providing real-time updates for enhanced user experience and efficiency")

chat_placeholder = st.container()
prompt_placeholder = st.form("chat-form")
#credit_card_placeholder = st.empty()

with chat_placeholder:
    for chat in st.session_state.history:
        div = f"""
<div class="chat-row 
    {'' if chat.origin == 'ai' else 'row-reverse'}">
    <img class="chat-icon" src="app/style/{
        'worker.png' if chat.origin == 'pr pal' 
                      else 'user.png'}"
         width=32 height=32>
    <div class="chat-bubble
    {'ai-bubble' if chat.origin == 'ai' else 'human-bubble'}">
        &#8203;{chat.message}
    </div>
</div>
        """
        st.markdown(div, unsafe_allow_html=True)
    
    for _ in range(3):
        st.markdown("")

with prompt_placeholder:
    st.markdown("**Ask me**")
    cols = st.columns((6, 1))
    cols[0].text_input(
        "How can I help you today?",
        value=" ",
        label_visibility="collapsed",
        key="human_prompt",
    )
    cols[1].form_submit_button(
        "Submit", 
        type="primary", 
        on_click=on_click_callback, 
    )

#credit_card_placeholder.caption(f"""
#Used {st.session_state.token_count} tokens \n
#Debug Langchain conversation: 
#{st.session_state.conversation.memory.buffer}
#""")

components.html("""
<script>
const streamlitDoc = window.parent.document;

const buttons = Array.from(
    streamlitDoc.querySelectorAll('.stButton > button')
);
const submitButton = buttons.find(
    el => el.innerText === 'Submit'
);

streamlitDoc.addEventListener('keydown', function(e) {
    switch (e.key) {
        case 'Enter':
            submitButton.click();
            break;
    }
});
</script>
""", 
    height=0,
    width=0,
)
