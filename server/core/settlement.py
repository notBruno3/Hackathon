from __future__ import annotations

from .transaction import Transaction
from typing import List, Dict, Any
from collections import defaultdict


class SettlementEngine:
    @staticmethod
    def minimize(transactions: List[Transaction]) -> List[Dict[str, Any]]:
        # Step 1: Compute net balances
        balances = defaultdict(float)

        for tx in transactions:
            amount_per_person = tx.amount / len(tx.payees)
            for payee in tx.payees:
                balances[payee] -= amount_per_person
            balances[tx.payer] += tx.amount

        # Round to avoid floating point issues
        balances = {person: round(balance, 2) for person, balance in balances.items()}

        # Step 2: Split into debtors and creditors
        creditors = []
        debtors = []

        for person, balance in balances.items():
            if balance > 0:
                creditors.append([person, balance])
            elif balance < 0:
                debtors.append([person, -balance])

        # Step 3: Greedy settlement
        settlements = []

        i, j = 0, 0
        while i < len(debtors) and j < len(creditors):
            debtor, debt_amt = debtors[i]
            creditor, credit_amt = creditors[j]
            amount = min(debt_amt, credit_amt)

            settlements.append({
                "from": debtor,
                "to": creditor,
                "amount": round(amount, 2)
            })

            debtors[i][1] -= amount
            creditors[j][1] -= amount

            if debtors[i][1] == 0:
                i += 1
            if creditors[j][1] == 0:
                j += 1

        return settlements
