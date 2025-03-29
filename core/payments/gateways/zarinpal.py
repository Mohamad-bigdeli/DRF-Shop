import json
import requests
from typing import Dict, Any, Optional
from django.conf import settings
from payments.exceptions import PaymentError


class ZarinPalClient:

    def __init__(
        self,
        merchant_id: str = None,
        sandbox: bool = True,
        timeout: float = 10.0,
        enable_logging: bool = True,
    ):

        self.merchant_id = merchant_id or settings.ZARINPAL_MERCHANT_ID
        self.sandbox = sandbox or settings.ZARINPAL_SANDBOX
        self.timeout = timeout
        self.enable_logging = enable_logging
        
        # Base URLs (Sandbox vs. Real)
        self.base_api_url = (
            "https://payment.zarinpal.com/pg/v4/payment/"  # Production
            if not sandbox
            else "https://sandbox.zarinpal.com/pg/v4/payment/"  # Sandbox
        )
        
        # Payment Gateway URL (For redirecting users)
        self.payment_gateway_url = (
            "https://payment.zarinpal.com/pg/StartPay/"  # Production
            if not sandbox
            else "https://sandbox.zarinpal.com/pg/StartPay/"  # Sandbox
        )

        self._log(f"Initialized ZarinPalClient (Sandbox: {sandbox}, MerchantID: {self.merchant_id})")

    def request_payment(
        self,
        amount: int,
        callback_url: str,
        description: str = "Payment for order",
        mobile: Optional[str] = None,
        email: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> Dict[str, Any]:

        url = self.base_api_url + "request.json"
        payload = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "callback_url": callback_url,
            "description": description,
        }
        
        # Optional fields
        if mobile:
            payload["mobile"] = mobile
        if email:
            payload["email"] = email
        if metadata:
            payload["metadata"] = metadata

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        self._log(f"Payment Request -> {url} | Payload: {payload}")

        try:
            response = requests.post(
                url,
                data=json.dumps(payload),
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()

            self._log(f"Payment Response <- {data}")

            if data.get("data", {}).get("code") != 100:
                error_msg = data.get("errors", {}).get("message", "Payment request failed")
                raise PaymentError(f"ZarinPal Error: {error_msg} (Code: {data.get('data', {}).get('code')})")

            authority = data["data"]["authority"]
            payment_url = f"{self.payment_gateway_url}{authority}"

            return {
                "authority": authority,
                "payment_url": payment_url,
                "raw_response": data,
            }

        except requests.Timeout:
            raise PaymentError("Payment request timed out")
        except requests.RequestException as e:
            raise PaymentError(f"Network error: {str(e)}")

    def verify_payment(self, authority: str, amount: int, ) -> Dict[str, Any]:

        url = self.base_api_url + "verify.json"
        payload = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "authority": authority,
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        self._log(f"Verify Request -> {url} | Payload: {payload}")

        try:
            response = requests.post(
                url,
                data=json.dumps(payload),
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()

            self._log(f"Verify Response <- {data}")

            if data.get("data").get("code") != 100:
                error_msg = data.get("errors")
                raise PaymentError(f"ZarinPal Error: {error_msg} (Code: {data.get('data').get('code')})")

            return {
                "ref_id": data["data"]["ref_id"],
                "raw_response": data,
            }

        except requests.Timeout:
            raise PaymentError("Verification request timed out")
        except requests.RequestException as e:
            raise PaymentError(f"Network error: {str(e)}")

    def _log(self, message: str, error: bool = False) -> None:
        """Internal logging method."""
        if self.enable_logging:
            log_msg = f"[ZarinPalClient] {message}"
            print("ERROR: " + log_msg if error else log_msg)