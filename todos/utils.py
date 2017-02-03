from rest_framework_jwt.settings import api_settings


def generate_token(payload):
  jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
  jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
  token_payload = jwt_payload_handler(payload)
  return jwt_encode_handler(token_payload)
