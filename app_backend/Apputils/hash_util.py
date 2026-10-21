import hashlib
from ValidationLayer import FeedbackHookValidation

class hasher:
    @staticmethod
    def get_hash(data:FeedbackHookValidation):
        canonical_json = data.model_dump_json(
            by_alias=True, exclude_unset=True
        )
        payload_hash = hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()
        # print(f"Canonical JSON: {canonical_json}")
        print(f"SHA-256 Hash: {payload_hash}")
        return payload_hash

# payload_instance = FeedbackHookValidation(
#     source_id="TICK-99482",
#     channel="zendesk_webhook",
#     raw_text=(
#         "URGENT! My payment failed for subscription ID 4481. My name is John"
#         " Doe, call me at 555-0199 or john@example.com ASAP! Fix this app"
#         " crash!"
#     ),
# )

# hasher.get_hash(payload_instance)