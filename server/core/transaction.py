from typing import List

class Transaction:
    def __init__(self, id: str, payer: str, payees: List[str], amount: float, source_message_id: str):
        self.id = id
        self.payer = payer
        self.payees = payees
        self.amount = amount
        self.source_message_id = source_message_id
