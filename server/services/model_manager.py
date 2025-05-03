from openai import OpenAI
from typing import List, Dict, Tuple
from core.participant import Participant
from core.message import Message
from core.transaction import Transaction
from core.settlement import SettlementEngine
from dotenv import load_dotenv
import os, re
import json
from uuid import uuid4

load_dotenv()


class ModelManager:
    def __init__(self):
        self.raw_summary = "Event started. No actions recorded yet."
        self.parsed_log = []
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )

    def extract_transactions(self, message: Message, participants: List[Participant]) -> Tuple[List[Transaction], Message]:
        resolved_sender = self._get_name_by_id(message.sender_id, participants)
        #print(f"extracting for {resolved_sender}")
        system_prompt= f"""
You are a smart financial assistant in a group chat where users describe shared expenses in natural language.

Your job is to understand each message, extract structured transactions from it, and contribute to a running event summary (the "EVENT SUMMARY").

### Context:
- You see messages one at a time.
- Each message is tied to a specific user (the sender).
- The EVENT SUMMARY gives you the full log of what has been said and understood so far.
- If a previous message was ambiguous, your own log should include a line that starts with "NOT UNDERSTOOD: ..." explaining what was missing.
- The user might then reply to clarify — this will be the **next message**.

You must therefore check if the most recent line in the summary is a NOT UNDERSTOOD message. If so, treat the current message as a clarification to that.

---

### Rules:
1. **If you understand the message**, extract one or more transactions and append a new line to the EVENT SUMMARY. Start it with:
   - `UNDERSTOOD: <short summary in third person>`
   This should be a human-readable one-liner.

2. **If you do not understand the message**, do NOT guess. Instead:
   - Append a line to the summary: `NOT UNDERSTOOD: <explain what was unclear>`
   - Prepare a `clarification_question` for the user that will help you understand.

3. **If the message is a clarification**, add:
   - A line starting with `CLARIFICATION: <interpretation>`
   - Then a line starting with `UNDERSTOOD: <actual inferred understanding>`

---

### Output:
Respond **only with a valid JSON object** with the following fields:

```json
{{
  "summary_lines": ["<line1>", "<line2>", "..."],
  "message_text": "<short message to show the user>",

  "status": "understood" | "not_understood" | "clarification",

  "transactions": [
    {{
      "who": "<payer name>",
      "to": ["<payee name>", "..."],
      "total": <amount as float>
    }}
  ],

  "clarification_question": "<only if not_understood>"
}}
```
summary_lines: List of lines to append to the event summary. Each line must be short and follow the formats above.

message_text: A friendly message for the frontend to display — usually identical to the last summary line, but can be different if needed.

status: One of "understood", "not_understood", or "clarification".

transactions: A list of structured transactions if the message was understood.

clarification_question: Only filled if status is not_understood. This is the question the user will see next.

Always return only valid JSON. Do not include Markdown, code blocks, or any prose outside the JSON.
"""
        
        prompt = f"""
The current message is:
"{message.text}"

It was sent by:
"{resolved_sender}"

The current EVENT SUMMARY is:
{self.raw_summary}

What should be appended to the summary now? Return your answer in the required JSON format.
"""
        completion = self.client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
            temperature=0.3
        )
        content = completion.choices[0].message.content.strip()

            
        cleaned = re.sub(r"```(?:json)?\s*([\s\S]*?)\s*```", r"\1", content.strip())
        try:
            result = json.loads(cleaned)
        except json.JSONDecodeError:
            raise ValueError(f"LLM response could not be parsed as JSON: {cleaned}")

        for line in result["summary_lines"]:
            self.raw_summary += f"\n{line}"

        transactions = []
        if result["status"] in ["understood","clarification"]:
            
            for tx in result["transactions"]:
                transaction = Transaction(
                    id=str(uuid4()),
                payer=tx["who"],
                payees=tx["to"],
                amount=float(tx["total"])
                )
                transactions.append(transaction)

        answer = Message("0", result["message_text"])
        return transactions, answer

    def compute_settlement_with_ai(self, transactions: List[Transaction]) -> List[Dict]:
        """
        Uses an LLM to compute the minimum number of payments required to settle the debts.
        Returns a list of dicts: { from, to, amount }
        """
        # Convert Transaction objects to raw dicts
        tx_data = [
            {
                "who": tx.payer,
                "to": tx.payees,
                "total": tx.amount
            } for tx in transactions
        ]

        prompt = f"""
You are a smart financial assistant.
Below is a list of individual expense transactions. Each transaction has:
- who paid,
- for whom,
- and how much.

Your task is to compute the smallest possible number of payments between people to make it fair — so that everyone has contributed equally overall.

Each transaction looks like:
{{ "who": "Alice", "to": ["Bob", "Charlie"], "total": 30 }}

Input transactions:
{json.dumps(tx_data, indent=2)}

Output ONLY a JSON list of settlement payments, like:
[
  {{ "from": "Samu", "to": "Pablo", "amount": 13.33 }},
  ...
]

Don't add explanations. Just a valid JSON list.
"""

        completion = self.client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": "You reduce debt graphs to minimal payment instructions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        content = completion.choices[0].message.content.strip()

        cleaned = re.sub(r"```(?:json)?\s*([\s\S]*?)\s*```", r"\1", content.strip())

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            raise ValueError(f"Could not parse LLM settlement output as JSON:\n{cleaned}")

    def compute_settlement(self, transactions: List[Transaction]) -> List[Dict[str, any]]:
        # You can later swap this with an LLM reasoning pass
        return SettlementEngine.minimize(transactions)

    
    def _get_name_by_id(self, participant_id: str, participants: List[Participant]) -> str:
        for p in participants:
            if p.id == participant_id:
                return p.name
        raise ValueError(f"Participant with ID {participant_id} not found.")
