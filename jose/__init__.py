import base64
import json
import hmac
import hashlib

class JWTError(Exception):
    pass

class jwt:
    @staticmethod
    def encode(payload, key, algorithm="HS256"):
        if algorithm != "HS256":
            raise JWTError("Unsupported algorithm")
        header = {"alg": algorithm, "typ": "JWT"}
        def b64(data):
            return base64.urlsafe_b64encode(json.dumps(data).encode()).rstrip(b"=").decode()
        header_b64 = b64(header)
        payload_b64 = b64(payload)
        signing_input = f"{header_b64}.{payload_b64}".encode()
        signature = hmac.new(key.encode(), signing_input, hashlib.sha256).digest()
        sig_b64 = base64.urlsafe_b64encode(signature).rstrip(b"=").decode()
        return f"{header_b64}.{payload_b64}.{sig_b64}"

    @staticmethod
    def decode(token, key, algorithms=None):
        if algorithms and "HS256" not in algorithms:
            raise JWTError("Unsupported algorithm")
        try:
            header_b64, payload_b64, sig_b64 = token.split(".")
        except ValueError:
            raise JWTError("Invalid token")
        signing_input = f"{header_b64}.{payload_b64}".encode()
        signature = base64.urlsafe_b64decode(sig_b64 + "===")
        expected = hmac.new(key.encode(), signing_input, hashlib.sha256).digest()
        if not hmac.compare_digest(signature, expected):
            raise JWTError("Invalid signature")
        payload_json = base64.urlsafe_b64decode(payload_b64 + "===")
        return json.loads(payload_json)
