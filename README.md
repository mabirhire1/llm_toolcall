# FastAPI LLM Tools Implementation (OpenRouter)

This project demonstrates how to enhance the capabilities of Large Language Models (LLMs) by integrating **custom tools (function calls)** using **FastAPI** and the **OpenAI SDK via OpenRouter**.

The system allows an LLM to:

* Retrieve a **flight booking schedule** with pricing in USD
* Retrieve a **hotel booking schedule** with pricing in USD
* Perform **currency conversion**

The LLM is prompted with a real-world travel query and automatically calls the appropriate tools to compute the final answer, which is printed to standard output.

---

## Features

* Uses **OpenRouter** to access OpenAI-compatible models
* Supports **tool/function calling**
* No API endpoints — output is printed directly to the console
* Environment-based configuration using `.env`

---

## Project Structure

```bash
.
├── .gitignore
├── .env
├── main.py
├── README.md
└── requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root directory with the following values:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
GEMINI_API_KEY=optional_or_placeholder
LLM_MODEL_NAME=openai/gpt-4o-mini
```

> Only `OPENROUTER_API_KEY` is required for this implementation. The others are optional placeholders to satisfy interface requirements.

---

## Installation

1. Clone the repository or copy the project files.
2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Run the application using:

```bash
uvicorn main:app
```

This will execute the tool-calling workflow and print the final LLM response directly to the terminal.

---

## Example Prompt

The system automatically sends the following prompt to the LLM:

> *"I'm taking a flight from Lagos to Nairobi for a conference. I would like to know the total flight time back and forth, and the total cost of logistics for this conference if I'm staying for three days."*

---

## Example Output

```text
Your flight from Lagos to Nairobi takes approximately **5.5 hours**. 

The estimated round-trip flight cost is **$920**.

For your stay in Nairobi, here are some hotel options for three nights:

1. **Nairobi Serena**: $250 per night
   - Total for 3 nights: $750
2. **Radisson Blu**: $200 per night
   - Total for 3 nights: $600

### Total Cost of Logistics:
- **Flight**: $920
- **Hotel (Nairobi Serena)**: $750
- **Total**: $1,670
- **Hotel (Radisson Blu)**: $600
- **Total**: $1,520

Your total logistics cost will be **$1,670** if you choose Nairobi Serena or **$1,520** if you opt for Radisson Blu.
```

---

## Tools Implemented

### 1. Flight Booking Tool

Returns flight duration and pricing for outbound and return trips.

### 2. Hotel Booking Tool

Returns nightly rate and total cost for a stay.

### 3. Currency Conversion Tool

Converts in USD, NGN

---

## Technology Stack

* **Python 3.10+**
* **FastAPI**
* **OpenAI SDK** (via OpenRouter)
* **python-dotenv**

---

## License

This project is provided for educational and demonstration purposes. You are free to modify and extend it for your own use.

---

## Author

Built by an AI Developer focused on building intelligent systems using LLMs and tool orchestration.