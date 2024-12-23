# Financial Budget Assistant

This is a chatbot that helps users organize their budget and gives savings tips based on their income and expenses.

## Requirements

1- Python 3.11

2- Create a new environment using the following command:

```bash
$ python -m venv chatbot_venv
```

3- Activate the environment:

```bash
$ .\chatbot_venv\Scripts\activate
```

## Installation

### Install the required packages

```bash
$ pip install -r requirements.txt
```

Set your Gemini_API_KEY value in the main.py file.

## Run the FastAPI server

```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Run the streamlit app in another terminal

```bash
$ streamlit run streamlit_app.py
```


## Budget Calculation and Savings Tips Generation

This chatbot leverages prompt engineering techniques with Google's Gemini AI model to provide financial advice. Rather than implementing hard-coded calculations, the system uses a carefully crafted instruction prompt that:

1. **Defines the Chatbot's Persona**
   - Establishes the bot as a financial expert
   - Sets the tone for professional financial advice
   - Creates a consistent interaction pattern

2. **Implements the 50/30/20 Rule Through Context**
   The system instruction provides the AI model with:
   - Clear categorization of expenses (needs: 50%, wants: 30%, savings: 20%)
   - Guidelines for adjusting these percentages based on user data
   - Framework for analyzing user's financial situation

3. **Guides Response Generation**
   The instruction includes:
   - A specific format for budget breakdown
   - Direction to provide actionable savings tips
   - An example interaction that demonstrates the desired output format
