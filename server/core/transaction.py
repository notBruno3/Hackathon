from typing import List

class Transaction:
    def __init__(self, id: str, payer: str, payees: List[str], amount: float):
        self.id = id
        self.payer = payer
        self.payees = payees
        self.amount = amount
