from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from typing import List, Dict

Gemini_API_KEY = "xxxxxxxxxx"

# Configure Gemini API
genai.configure(api_key=Gemini_API_KEY)

# Define system instruction for the chatbot
system_instruction = """
You are a financial expert chatbot designed to help users organize their budget and provide personalized savings tips. 
Your tasks include:
- Collecting financial information from the user: monthly income, fixed expenses (e.g., rent, bills), discretionary expenses (e.g., dining, hobbies), and optional savings goals.
- Calculating a recommended budget using the 50/30/20 rule:
  - 50% for needs (fixed expenses).
  - 30% for wants (discretionary expenses).
  - 20% for savings (or adjusted percentages based on the user's data).
- Providing actionable savings tips, such as reducing specific expenses or setting up an emergency fund.

User Interaction Example:
    User: "I earn $3000 monthly, spend $1200 on rent, $300 on utilities, and $600 on hobbies."
    Bot:
        "Here’s your recommended budget:
        Needs (50%): $1500
        Wants (30%): $900
        Savings (20%): $600
        To save more, try reducing your hobbies spending by $100."
"""

# Create the generative model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", system_instruction=system_instruction
)

# Initialize FastAPI app
app = FastAPI()

# Create a dictionary to store chat sessions
chat_sessions: Dict[str, Dict] = {}


class ChatMessage(BaseModel):
    message: str
    session_id: str


class ChatHistory(BaseModel):
    role: str
    content: str


@app.post("/chat/")
async def chat_with_bot(chat_message: ChatMessage):
    try:
        session_id = chat_message.session_id

        # Create a new chat session if it doesn't exist
        if session_id not in chat_sessions:
            chat_sessions[session_id] = {
                "chat": model.start_chat(history=[]),
                "history": [],
                "user_data": {
                    "monthly_income": None,
                    "fixed_expenses": None,
                    "discretionary_expenses": None,
                    "savings_goals": None,
                },
            }

        session = chat_sessions[session_id]

        # Add user message to history
        session["history"].append({"role": "user", "content": chat_message.message})

        # Create context from history
        context = "Previous conversation context:\n"
        for msg in session["history"]:
            context += f"{msg['role']}: {msg['content']}\n"

        # Send message with context
        response = session["chat"].send_message(
            f"{context}\nUser's latest message: {chat_message.message}"
        )

        # Add bot response to history
        session["history"].append({"role": "bot", "content": response.text})

        # Extract and store financial information (you can expand this)
        if "monthly" in chat_message.message.lower() and "$" in chat_message.message:
            try:
                amount = float(chat_message.message.split("$")[1].split()[0])
                session["user_data"]["monthly_income"] = amount
            except:
                pass

        return {
            "bot_response": response.text,
            "session_id": session_id,
            "user_data": session["user_data"],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Add endpoint to get chat history
@app.get("/chat/{session_id}/history")
async def get_chat_history(session_id: str):
    if session_id not in chat_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"history": chat_sessions[session_id]["history"]}


# Add endpoint to clear chat history
@app.delete("/chat/{session_id}")
async def clear_chat_history(session_id: str):
    if session_id in chat_sessions:
        del chat_sessions[session_id]
    return {"message": "Chat history cleared"}
