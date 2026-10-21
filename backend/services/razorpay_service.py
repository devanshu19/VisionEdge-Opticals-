"""
VisionEdge — Razorpay Payment Gateway Service
=============================================
Provides production-ready helpers for:
  - Client initialization and readiness validation
  - Razorpay order creation (converting INR rupees to paise)
  - Payment and webhook HMAC-SHA256 signature verification
  - Fetching live payment and order statuses
  - Admin-initiated refunds (full and partial)
  - Safe error reporting without credential leakage
"""

import hmac
import hashlib
import logging
from typing import Optional, Tuple, Dict, Any

import razorpay
from razorpay.errors import SignatureVerificationError, BadRequestError, GatewayError

from config import Config

logger = logging.getLogger("visionedge.razorpay")


class RazorpayService:
    @staticmethod
    def is_configured() -> bool:
        """Check if Razorpay API keys are configured."""
        return Config.is_razorpay_configured()

    @classmethod
    def get_client(cls) -> razorpay.Client:
        """
        Instantiate and return an official Razorpay Client.
        Raises ValueError if credentials are not configured.
        """
        if not cls.is_configured():
            logger.error("Attempted to access Razorpay client, but credentials are missing.")
            raise ValueError(
                "Razorpay payment gateway is not properly configured. "
                "Please set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET."
            )
        return razorpay.Client(auth=(Config.RAZORPAY_KEY_ID, Config.RAZORPAY_KEY_SECRET))

    @staticmethod
    def rupees_to_paise(amount_in_rupees: float) -> int:
        """Convert float/decimal rupees into integer paise."""
        return int(round(float(amount_in_rupees) * 100))

    @staticmethod
    def paise_to_rupees(amount_in_paise: int) -> float:
        """Convert integer paise back to float rupees."""
        return round(float(amount_in_paise) / 100.0, 2)

    @classmethod
    def create_order(
        cls,
        amount_in_rupees: float,
        receipt: str,
        notes: Optional[Dict[str, Any]] = None,
        currency: str = "INR"
    ) -> Dict[str, Any]:
        """
        Create a new Razorpay order.

        :param amount_in_rupees: Amount in INR (e.g. 1499.00)
        :param receipt: Unique internal reference / order number
        :param notes: Metadata dictionary (order_id, customer_id, store, etc.)
        :param currency: Currency code, default 'INR'
        :return: Dict containing Razorpay order payload
        """
        client = cls.get_client()
        amount_paise = cls.rupees_to_paise(amount_in_rupees)

        if amount_paise < 100:  # Razorpay minimum is 100 paise (₹1.00)
            raise ValueError("Minimum order amount for Razorpay is ₹1.00")

        order_data = {
            "amount": amount_paise,
            "currency": currency or Config.RAZORPAY_CURRENCY or "INR",
            "receipt": str(receipt),
            "payment_capture": 1,  # Auto capture payment
            "notes": notes or {}
        }

        try:
            logger.info("Creating Razorpay order: amount_paise=%d, receipt=%s", amount_paise, receipt)
            rzp_order = client.order.create(data=order_data)
            logger.info("Created Razorpay order successfully: rzp_order_id=%s", rzp_order.get("id"))
            return rzp_order
        except BadRequestError as e:
            logger.error("Razorpay BadRequestError creating order: %s", str(e))
            raise ValueError(f"Razorpay order creation failed: {str(e)}")
        except GatewayError as e:
            logger.error("Razorpay GatewayError creating order: %s", str(e))
            raise RuntimeError("Payment gateway error occurred while creating order. Please try again.")
        except Exception as e:
            logger.error("Unexpected error creating Razorpay order: %s", str(e))
            raise RuntimeError("Unable to initiate online payment session.")

    @classmethod
    def verify_payment_signature(
        cls,
        razorpay_order_id: str,
        razorpay_payment_id: str,
        razorpay_signature: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Verify the authenticity of a Razorpay payment signature.

        Uses HMAC SHA-256 over '{razorpay_order_id}|{razorpay_payment_id}' with RAZORPAY_KEY_SECRET.
        :return: (is_valid: bool, error_reason: Optional[str])
        """
        if not razorpay_order_id or not razorpay_payment_id or not razorpay_signature:
            return False, "Missing order ID, payment ID, or signature."

        secret = Config.RAZORPAY_KEY_SECRET
        if not secret:
            return False, "Server Razorpay secret is not configured."

        try:
            client = cls.get_client()
            client.utility.verify_payment_signature({
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature
            })
            return True, None
        except SignatureVerificationError:
            logger.warning(
                "Payment signature verification failed for order %s, payment %s",
                razorpay_order_id, razorpay_payment_id
            )
            return False, "Payment signature verification failed."
        except Exception as e:
            # Fallback direct HMAC computation
            try:
                payload = f"{razorpay_order_id}|{razorpay_payment_id}".encode("utf-8")
                expected_sig = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
                if hmac.compare_digest(expected_sig, razorpay_signature):
                    return True, None
                return False, "Payment signature mismatch."
            except Exception as fallback_err:
                logger.error("Error during manual signature fallback: %s", str(fallback_err))
                return False, "Signature verification error."

    @classmethod
    def verify_webhook_signature(
        cls,
        raw_body: bytes,
        webhook_signature: str,
        secret: Optional[str] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Verify incoming Razorpay webhook signature.

        :param raw_body: Exact raw request body bytes
        :param webhook_signature: Value from 'X-Razorpay-Signature' header
        :param secret: Optional custom secret; defaults to Config.RAZORPAY_WEBHOOK_SECRET
        :return: (is_valid: bool, error_reason: Optional[str])
        """
        webhook_secret = secret or Config.RAZORPAY_WEBHOOK_SECRET
        if not webhook_secret:
            logger.error("Webhook verification attempted but RAZORPAY_WEBHOOK_SECRET is not configured.")
            return False, "Webhook secret not configured on server."

        if not webhook_signature:
            return False, "Missing X-Razorpay-Signature header."

        try:
            client = cls.get_client()
            # client.utility.verify_webhook_signature expects body (str or bytes)
            client.utility.verify_webhook_signature(
                raw_body.decode("utf-8") if isinstance(raw_body, bytes) else raw_body,
                webhook_signature,
                webhook_secret
            )
            return True, None
        except SignatureVerificationError:
            logger.warning("Webhook signature verification failed.")
            return False, "Webhook signature verification failed."
        except Exception as e:
            # Manual fallback
            try:
                expected_sig = hmac.new(
                    webhook_secret.encode("utf-8"),
                    raw_body if isinstance(raw_body, bytes) else raw_body.encode("utf-8"),
                    hashlib.sha256
                ).hexdigest()
                if hmac.compare_digest(expected_sig, webhook_signature):
                    return True, None
                return False, "Webhook signature mismatch."
            except Exception as hmac_err:
                logger.error("Webhook fallback verification exception: %s", str(hmac_err))
                return False, "Internal webhook verification failure."

    @classmethod
    def fetch_payment(cls, payment_id: str) -> Dict[str, Any]:
        """Fetch real-time payment details from Razorpay."""
        client = cls.get_client()
        try:
            return client.payment.fetch(payment_id)
        except Exception as e:
            logger.error("Error fetching Razorpay payment %s: %s", payment_id, str(e))
            raise RuntimeError(f"Could not fetch payment details for {payment_id}")

    @classmethod
    def fetch_order(cls, order_id: str) -> Dict[str, Any]:
        """Fetch order details from Razorpay."""
        client = cls.get_client()
        try:
            return client.order.fetch(order_id)
        except Exception as e:
            logger.error("Error fetching Razorpay order %s: %s", order_id, str(e))
            raise RuntimeError(f"Could not fetch order details for {order_id}")

    @classmethod
    def create_refund(
        cls,
        payment_id: str,
        amount_in_rupees: Optional[float] = None,
        notes: Optional[Dict[str, Any]] = None,
        speed: str = "normal"
    ) -> Dict[str, Any]:
        """
        Initiate a refund for a captured payment.

        :param payment_id: The Razorpay payment ID (e.g. 'pay_...')
        :param amount_in_rupees: Optional float amount for partial refund; None for full refund.
        :param notes: Metadata notes dict
        :param speed: 'normal' or 'optimum'
        :return: Razorpay refund response dict
        """
        client = cls.get_client()
        refund_data = {
            "speed": speed,
            "notes": notes or {}
        }
        if amount_in_rupees is not None and float(amount_in_rupees) > 0:
            refund_data["amount"] = cls.rupees_to_paise(amount_in_rupees)

        try:
            logger.info("Initiating Razorpay refund for payment %s (data=%s)", payment_id, refund_data)
            refund_resp = client.payment.refund(payment_id, refund_data)
            logger.info("Refund created successfully: refund_id=%s", refund_resp.get("id"))
            return refund_resp
        except BadRequestError as e:
            logger.error("BadRequestError on refund for %s: %s", payment_id, str(e))
            raise ValueError(f"Refund request rejected: {str(e)}")
        except Exception as e:
            logger.error("Error processing refund for %s: %s", payment_id, str(e))
            raise RuntimeError("Refund processing failed. Please check gateway logs.")

    @classmethod
    def fetch_refund(cls, payment_id: str, refund_id: str) -> Dict[str, Any]:
        """Fetch specific refund status."""
        client = cls.get_client()
        try:
            return client.payment.fetch_refund(payment_id, refund_id)
        except Exception as e:
            logger.error("Error fetching refund %s for payment %s: %s", refund_id, payment_id, str(e))
            raise RuntimeError(f"Could not fetch refund details: {str(e)}")
