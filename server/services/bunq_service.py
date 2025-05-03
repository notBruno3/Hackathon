# services/bunq_service.py

from bunq.sdk.context.api_context import ApiContext
from bunq.sdk.context.bunq_context import BunqContext
from bunq.sdk.model.generated.endpoint import MonetaryAccountBankApiObject, RequestInquiryApiObject
from bunq.sdk.model.generated.object_ import AmountObject, PointerObject
from bunq import ApiEnvironmentType

from typing import List, Dict
import os


class BunqService:
    def __init__(self):
        # Load or create bunq API context (sandbox or production)
        self._init_api_context()

    def _init_api_context(self):

        if os.path.exists("bunq.conf"):
            api_context = ApiContext.restore("bunq.conf")
        else:
            api_key = "sandbox_64460b0910e62edae2a6ae297ea346c589302710289841210214078d"
            api_context = ApiContext.create(
                ApiEnvironmentType.SANDBOX, # SANDBOX for testing
                api_key,
                "My Device Description"
            )
            api_context.save("bunq.conf")

        api_context.ensure_session_active()
        BunqContext.load_api_context(api_context)

    def send_requests(self, transactions: List[Dict], email_lookup: Dict[str, str]) -> List[Dict]:
        """Send payment requests based on settlement transactions.
        Each transaction is a dict with 'from', 'to', 'amount' keys.
        email_lookup maps user names to bunq-verified emails.
        """
        responses = []
        user_id = BunqContext.user_context().user_id
        account_id = MonetaryAccountBankApiObject.list(user_id).value[0].id_

        for tx in transactions:
            from_user = tx["from"]
            to_user = tx["to"]
            amount = float(tx["amount"])
            to_email = email_lookup.get(to_user)

            if not to_email:
                responses.append({
                    "status": "error",
                    "reason": f"No email found for user '{to_user}'",
                    "transaction": tx
                })
                continue

            try:
                request = RequestInquiryApiObject.create(
                    amount=AmountObject(str(amount), "EUR"),
                    counterparty_alias=PointerObject("EMAIL", to_email),
                    description=f"FairShare: You owe {amount:.2f}€ to {to_user}",
                    monetary_account_id=account_id,
                    user_id=user_id
                )

                responses.append({
                    "status": "success",
                    "request_id": request.value.id_,
                    "to": to_user,
                    "amount": amount
                })
            except Exception as e:
                responses.append({
                    "status": "error",
                    "reason": str(e),
                    "transaction": tx
                })

        return responses
