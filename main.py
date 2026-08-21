import os
import warnings
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

# Suppress deprecation warnings for a clean user interface
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Load environment variables from .env file
load_dotenv()

@tool
def calculator(a: float, b: float) -> str:
    """Useful for performing basic arithmeric calculations with numbers"""
    return f"The sum of {a} and {b} is {a + b}"

@tool
def say_hello(name: str) -> str:
    """Useful for greeting a user"""
    return f"Hello {name}, I hope you are well today"

# Page configuration
st.set_page_config(
    page_title="Grok Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Grok Theme CSS
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
    /* Global Styles */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #09090b !important; /* Zinc-950 dark */
        color: #f4f4f5 !important; /* Zinc-100 */
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* App Title Header */
    .grok-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 2.8rem;
        background: linear-gradient(135deg, #f4f4f5 30%, #a1a1aa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 0.2rem;
        letter-spacing: -0.05em;
    }
    
    .grok-subtitle {
        text-align: center;
        color: #71717a; /* Zinc-500 */
        font-size: 0.95rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #030712 !important; /* Gray-950 dark */
        border-right: 1px solid #1f2937;
    }
    [data-testid="stSidebar"] .stMarkdown {
        color: #e5e7eb;
    }
    
    /* Chat Input Container Custom styling */
    [data-testid="stChatInput"] {
        background-color: #0f172a !important; /* Slate-900 */
        border: 1px solid #334155 !important; /* Slate-700 */
        color: #f1f5f9 !important;
        border-radius: 24px !important;
    }
    
    /* Chat Message Bubbles */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border-bottom: 1px solid #18181b; /* Zinc-900 border separating messages */
        padding: 1.5rem 1rem !important;
    }
    
    [data-testid="stChatMessage"][data-test-user-role="user"] {
        background-color: rgba(24, 24, 27, 0.3) !important;
    }
    
    /* Status indicators */
    .stStatusWidget {
        background-color: #18181b !important;
        border: 1px solid #27272a !important;
        border-radius: 12px !important;
    }
    
    /* Sidebar Selectbox & Slider borders */
    div[data-baseweb="select"] > div {
        background-color: #18181b !important;
        border-color: #27272a !important;
        color: #f4f4f5 !important;
    }
    
    /* Custom button styling */
    .stButton>button {
        background-color: #1e1b4b !important; /* Indigo dark button */
        color: #ffffff !important;
        border: 1px solid #3730a3 !important;
        border-radius: 8px !important;
        width: 100%;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        background-color: #312e81 !important;
        border-color: #4f46e5 !important;
        box-shadow: 0 0 12px rgba(99, 102, 241, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar layout
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/57/X_logo_2023.svg", width=50) # Cool X/Grok aesthetic icon
    st.title("Grok Panel")
    st.markdown("---")
    
    # Model Selection
    env_model = os.getenv("GROQ_MODEL", "qwen/qwen3.6-27b")
    model_options = [
        "qwen/qwen3.6-27b",
        "llama-3.3-70b-versatile",
        "llama3-70b-8192",
        "mixtral-8x7b-32768"
    ]
    default_index = model_options.index(env_model) if env_model in model_options else 0
    model_name = st.selectbox(
        "Choose LLM Model",
        options=model_options,
        index=default_index,
        help="Select the Groq-powered AI model for your assistant."
    )
    
    # System mode selector
    mode = st.radio(
        "System Mode",
        options=["Regular Mode", "Fun/Witty Mode"],
        index=0,
        help="Regular Mode provides standard helpful answers. Fun Mode gives Grok-style witty and rebellious responses."
    )
    
    # Temperature Slider
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7 if mode == "Fun/Witty Mode" else 0.2,
        step=0.05,
        help="Higher values make output more random, lower values more deterministic."
    )
    
    st.markdown("---")
    
    # System instructions (defaults change based on mode selection, but are editable)
    default_prompt = (
        "You are Grok, a witty, rebellious chatbot inspired by the Hitchhiker's Guide to the Galaxy. "
        "You answer questions with a bit of humor, sarcasm, and a sharp mind. Use a fun and slightly cheeky tone."
        if mode == "Fun/Witty Mode"
        else "You are a helpful, precise, and polite AI assistant."
    )
    
    system_prompt = st.text_area(
        "System Instructions",
        value=default_prompt,
        height=120,
        help="These instructions shape the persona of the chatbot."
    )
    
    st.markdown("---")
    
    # Clear chat button
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Title headers
st.markdown('<div class="grok-title">Grok Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="grok-subtitle">Groq-Powered LangGraph Agent with Tools</div>', unsafe_allow_html=True)

# Initialize messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display message history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "tools" in msg and msg["tools"]:
            for tool_call in msg["tools"]:
                with st.expander(f"⚙️ Tool Invoked: {tool_call['name']}", expanded=False):
                    st.code(f"Input: {tool_call['args']}\nOutput: {tool_call['output']}")

# Chat input and execution
if user_input := st.chat_input("Ask Grok anything..."):
    # Render user query immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
        
    # Get response container
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        # Build langchain chat history for context
        chat_history = []
        for msg in st.session_state.messages[:-1]:
            if msg["role"] == "user":
                chat_history.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                # Ensure we represent previous assistant messages correctly
                chat_history.append(AIMessage(content=msg["content"]))
        
        chat_history.append(HumanMessage(content=user_input))
        
        # Initialize LangGraph React agent with current settings
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key:
            st.error("Error: `GROQ_API_KEY` is not set. Please configure it in your `.env` file.")
            st.stop()
            
        try:
            model = ChatGroq(model=model_name, temperature=temperature, groq_api_key=groq_key)
            agent_executor = create_react_agent(
                model,
                tools=[calculator, say_hello],
                prompt=system_prompt
            )
            
            assistant_response = ""
            tool_calls_executed = []
            
            # Use Streamlit's st.status container to show thinking steps and tools in progress
            with st.status("Grok is processing...", expanded=True) as status_widget:
                for chunk in agent_executor.stream({"messages": chat_history}):
                    # Agent output node
                    if "agent" in chunk:
                        agent_data = chunk["agent"]
                        if "messages" in agent_data:
                            for msg in agent_data["messages"]:
                                if isinstance(msg, AIMessage):
                                    if msg.content:
                                        assistant_response += msg.content
                                        # Render current streamed text
                                        response_placeholder.markdown(assistant_response)
                                    if msg.tool_calls:
                                        for tc in msg.tool_calls:
                                            st.write(f"🔍 Calling tool `{tc['name']}` with arguments: `{tc['args']}`")
                                            tool_calls_executed.append({
                                                "name": tc["name"],
                                                "args": tc["args"],
                                                "output": "" # will fill this on tool node chunk
                                            })
                                            
                    # Tool output node
                    elif "tools" in chunk:
                        tools_data = chunk["tools"]
                        if "messages" in tools_data:
                            for msg in tools_data["messages"]:
                                st.write(f"✅ Tool `{msg.name}` returned output.")
                                # Find corresponding tool call and update its output
                                if tool_calls_executed:
                                    for t_call in tool_calls_executed:
                                        if t_call["name"] == msg.name and not t_call["output"]:
                                            t_call["output"] = str(msg.content)
                                            break
                
                status_widget.update(label="Response Complete!", state="complete", expanded=False)
                
            # If assistant response is empty, but we had tool runs, let's display some text
            if not assistant_response:
                assistant_response = "I have run the requested tools but returned no additional text."
                response_placeholder.markdown(assistant_response)
                
            # Add to state history
            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_response,
                "tools": tool_calls_executed
            })
            
        except Exception as e:
            st.error(f"Failed to execute request: {str(e)}")