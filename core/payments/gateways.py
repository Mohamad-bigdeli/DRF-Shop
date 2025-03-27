import json
import requests
from typing import Dict, Any, Union
from django.conf import settings
from payments.exceptions import PaymentError


class ZibalClient:
    def __init__(
        self,
        merchant_id: str = None,
        timeout: Union[int, float] = 10,
        sandbox: bool = False,
        enable_logging: bool = True,
    ):

        self.merchant_id = merchant_id or settings.ZIBAL_MERCHANT_ID
        self.sandbox = sandbox
        self.timeout = timeout
        self.enable_logging = enable_logging
        self.base_url = (
            "https://gateway.zibal.ir/v1/"
            if not sandbox
            else "https://sandbox.zibal.ir/v1/"
        )

        self._log(
            f"ZibalClient initialized with merchant_id: {self.merchant_id}, sandbox: {self.sandbox}"
        )

    def payment_request(
        self,
        amount: int,
        callback_url: str,
        description: str = "Payment for order",
        mobile: str = None,
        order_id: str = None,
    ) -> Dict[str, Any]:

        url = self.base_url + "request"
        payload = {
            "merchant": self.merchant_id,
            "amount": amount,
            "callbackUrl": callback_url,
            "description": description,
        }

        if mobile:
            payload["mobile"] = mobile
        if order_id:
            payload["orderId"] = order_id

        headers = {"Content-Type": "application/json"}

        self._log(f"Sending payment request to {url} with payload: {payload}")

        try:
            response = requests.post(
                url, headers=headers, data=json.dumps(payload), timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()

            self._log(f"Received response from Zibal: {data}")

            if data.get("result") != 100:
                error_msg = data.get("message", "Payment request failed")
                self._log(f"Payment request failed: {error_msg}", error=True)
                raise PaymentError(error_msg)

            return data

        except requests.Timeout:
            self._log("Request timed out during payment request", error=True)
            raise PaymentError("Request timed out")

        except requests.RequestException as e:
            self._log(f"Network error occurred: {str(e)}", error=True)
            raise PaymentError("Network error occurred")

    def payment_verify(self, track_id: str) -> Dict[str, Any]:

        url = self.base_url + "verify"
        payload = {"merchant": self.merchant_id, "trackId": track_id}
        headers = {"Content-Type": "application/json"}

        self._log(f"Sending verification request to {url} with trackId: {track_id}")

        try:
            response = requests.post(
                url, headers=headers, data=json.dumps(payload), timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()

            self._log(f"Received verification response: {data}")

            if data.get("result") != 100:
                error_msg = data.get("message", "Payment verification failed")
                self._log(f"Verification failed: {error_msg}", error=True)
                raise PaymentError(error_msg)

            return data

        except requests.RequestException as e:
            self._log(f"Verification error: {str(e)}", error=True)
            raise PaymentError("Verification failed")

    def generate_payment_url(self, track_id: str) -> str:

        payment_url = f"{self.base_url.replace('/v1/', '')}start/{track_id}"
        self._log(f"Generated payment URL: {payment_url}")
        return payment_url

    def _log(self, message: str, error: bool = False) -> None:

        if self.enable_logging:
            log_msg = f"[ZibalClient] {message}"
            if error:
                print(f"ERROR: {log_msg}")
            else:
                print(log_msg)
