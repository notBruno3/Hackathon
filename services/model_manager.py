from openai import OpenAI
from typing import List, Dict, Tuple
from core.participant import Participant
from core.message import Message
from core.transaction import Transaction
from core.settlement import SettlementEngine
from dotenv import load_dotenv
import os
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

    def extract_transactions(self, message: Message, participants: List[Participant]) -> List[Transaction]:
        resolved_sender = self._get_name_by_id(message.sender_id, participants)

        prompt = f"""
You are an event expense tracker. Your job is to understand short texts describing group payments.

The message was sent by: {resolved_sender}
Known participants: {", ".join([p.name for p in participants])}

CURRENT SUMMARY:
{self.raw_summary}

NEW MESSAGE:
"{message.text}"

Extract transactions. Each transaction must follow this format:
{{
  "who": "<payer>",
  "to": ["<list>", "of", "payees"],
  "total": <amount>
}}

Respond only with a JSON list of such transactions.
"""

        completion = self.client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        content = completion.choices[0].message.content.strip().replace("```json", "").replace("```", "").replace("\\n", "")

        try:
            tx_dicts = json.loads(content)
        except json.JSONDecodeError:
            raise ValueError(f"LLM response could not be parsed as JSON: {content}")

        transactions = []
        for tx in tx_dicts:
            transactions.append(
                Transaction(
                    id=str(uuid4()),
                    payer=tx["who"],
                    payees=tx["to"],
                    amount=float(tx["total"]),
                    source_message_id=message.id,
                )
            )

        # Append natural language summary to event history
        self.raw_summary += f"\n- {resolved_sender}: {message.text}"
        return transactions

    def compute_settlement(self, transactions: List[Transaction]) -> List[Dict[str, any]]:
        # You can later swap this with an LLM reasoning pass
        return SettlementEngine.minimize(transactions)

    def _get_name_by_id(self, participant_id: str, participants: List[Participant]) -> str:
        for p in participants:
            if p.id == participant_id:
                return p.name
        raise ValueError(f"Participant with ID {participant_id} not found.")
