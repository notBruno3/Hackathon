from openai import OpenAI
from typing import List, Dict, Tuple
from dotenv import load_dotenv
import os

load_dotenv()


class ModelManager:
    def __init__(self):
        self.raw_summary = "Event started. No actions recorded yet."
        self.parsed_log = []  # list of {person, action, amount, item}
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )
    
    def call_understanding_model(self, message: str) -> Tuple[str, bool]:
        """Send a message and receive a response and understanding flag."""
        prompt = f"""
You are an event expense tracker. Your job is to understand short texts describing group payments. You are having a conversation with a person, so whenever it refers to itself (I did this, I did that), assume its the person you are talking to.

CURRENT SUMMARY:
{self.raw_summary}

NEW MESSAGE:
"{message}"

Think about the new message in the entirety of the context. Make sure you know who the people being talked about are. Ask about names if not sure, ask about quantities if not mentioned, ask about anything. Write the summary to be clear with this. Include any extra meta information you need, like a declaration of how many people there are, etc etc.
Respond with either:
1. "UNDERSTOOD: <your short summary of who paid what>"
2. "NOT UNDERSTOOD: <a clarifying question>"
"""
        completion = self.client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        response = completion.choices[0].message.content.strip()
        understood = response.startswith("UNDERSTOOD")
        return response, understood

    def update_summary(self, new_fact: str):
        self.raw_summary += f"\n- {new_fact}"
        # You could also extract structured data using another LLM pass

    def needs_clarification(self, message, clarification):
        prompt  = f"""
You are an event expense tracker. Your job is to understand short texts describing group payments.

You got this message:
{message}

Under this summary of the event transactions: 
{self.raw_summary}

You didn't quite understand something about the message, and got this clarification:
{clarification}
Do you understand what it means?
Respond with either:
1. "UNDERSTOOD: <your short summary of who paid what>"
2. "NOT UNDERSTOOD: <a clarifying question>"""
        completion = self.client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[{"role": "user", "content": prompt}],
        )
        response = completion.choices[0].message.content.strip()
        understood = response.startswith("UNDERSTOOD")
        return response, understood



    def generate_settlement(self) -> Dict:
        """At end of event, call model to create payments"""
        reasoning_prompt = f"""
You are a finance AI. Below is a summary of an event, where people spent money.
Your job is to compute the **minimum number of payments** needed to make it fair.

SUMMARY:
{self.raw_summary}

Output ONLY a JSON like:
[
  {{ "from": "Samu", "to": "Pablo", "amount": 5.25 }},
  ...
]
"""
        
        
        response = self.client.chat.completions.create(
            model="openai/o4-mini",
            messages=[{"role": "user", "content": reasoning_prompt}],
        )

        return response.choices[0].message.content


# --- Example usage ---
if __name__ == "__main__":
    mm = ModelManager()
    messages = ["Pablo paid 20 for pizza for everyone, and Samu brought a game that was 10",
                "Pelayo bought me tickets to the cinema for 20€ each",
                "I payed for Pelayo's ice cream that was 3€",
                "I payed Samuel's popcorn for 5€"]
    for message in messages:
        resp, understood = mm.call_understanding_model(message)
        print("Agent:", resp)
        if understood:
            mm.update_summary(resp.replace("UNDERSTOOD: ", ""))
        else:
            clarification = input("I need more clarification: ")
            response, understood = mm.needs_clarification(message, clarification)
            if understood: mm.update_summary(response.replace("UNDERSTOOD: ", ""))

    final_json = mm.generate_settlement()
    print("Payments to make it fair:\n", final_json)