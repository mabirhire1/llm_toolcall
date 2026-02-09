import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "openai/gpt-4o-mini")

# Initialize OpenAI client with OpenRouter
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    
)

# ------------------
# Tools (Business Logic)
# ------------------
def get_flight_schedule(origin: str, destination: str):
    return {
        "origin": origin,
        "destination": destination,
        "flight_time_hours": 5.5,
        "price_usd": 920
    }

def get_hotel_schedule(city: str):
    return {
        "city": city,
        "hotels": [
            {"name": "Nairobi Serena", "price_usd": 250},
            {"name": "Radisson Blu", "price_usd": 200}
        ]
    }

def convert_currency(amount: float, from_currency: str, to_currency: str):
    exchange_rates = {
        ("USD", "NGN"): 1400
    }
    rate = exchange_rates[(from_currency, to_currency)]
    return {
        "amount_converted": amount * rate,
        "currency": to_currency
    }

# #------------------
# # Tool Schemas
# # ------------------
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_flight_schedule",
            "description": "Returns flight duration and price in USD",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {"type": "string"},
                    "destination": {"type": "string"}
                },
                "required": ["origin", "destination"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_hotel_schedule",
            "description": "Get hotel options for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "convert_currency",
            "description": "Convert between currencies",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number"},
                    "from_currency": {"type": "string"},
                    "to_currency": {"type": "string"}
                },
                "required": ["amount", "from_currency", "to_currency"]
            }
        }
    }
]

# --------------------
# Main Execution Logic
# --------------------

prompt = (
    "I'm taking a flight from Lagos to Nairobi for a conference. "
    "I would like to know the total flight time back and forth, "
    "and the total cost of logistics for this conference if I'm staying for three days."
)

messages = [{"role": "user", "content": prompt}]

# Tool calls
def execute_function(function_name, args):
        if function_name == "get_flight_schedule":
            return get_flight_schedule(**args)
        elif function_name == "get_hotel_schedule":
            return get_hotel_schedule(**args)
        elif function_name == "convert_currency":
            return convert_currency(**args)
        else:
            return {"error": f"Unknown function: {function_name}"}

# ------------------
#  Conversation Loop
# ------------------
def run_conversation_loop():
    global messages

while True:
    response = client.chat.completions.create(
        model=LLM_MODEL_NAME,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    if message.tool_calls:
        messages.append(message)

        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            result = execute_function(function_name, function_args)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": json.dumps(result)
            })

        continue

    print("\nFinal LLM Response:\n")
    print(message.content)
    break

run_conversation_loop()
