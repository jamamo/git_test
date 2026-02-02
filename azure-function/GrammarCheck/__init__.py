import json
import logging
import os
from typing import Any, Dict, List, Tuple

import azure.functions as func
import requests

DEFAULT_LANGUAGE = "en-US"
DEFAULT_API_URL = "https://api.languagetool.org/v2/check"


def _build_matches(matches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    cleaned = []
    for match in matches:
        cleaned.append(
            {
                "message": match.get("message"),
                "shortMessage": match.get("shortMessage"),
                "offset": match.get("offset"),
                "length": match.get("length"),
                "replacements": [r.get("value") for r in match.get("replacements", [])],
                "rule": match.get("rule", {}).get("id"),
            }
        )
    return cleaned


def _check_text(text: str, language: str, api_url: str) -> Tuple[bool, Dict[str, Any]]:
    payload = {"text": text, "language": language}
    try:
        response = requests.post(api_url, data=payload, timeout=10)
    except requests.RequestException as exc:
        logging.exception("Grammar API request failed")
        return False, {"error": str(exc)}

    if response.status_code != 200:
        logging.error("Grammar API returned %s: %s", response.status_code, response.text)
        return False, {
            "error": "Grammar API returned a non-200 response",
            "status": response.status_code,
            "details": response.text,
        }

    data = response.json()
    matches = _build_matches(data.get("matches", []))
    return True, {"matches": matches, "language": data.get("language", {}).get("name")}


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("GrammarCheck function processed a request.")

    try:
        body = req.get_json()
    except ValueError:
        body = {}

    language = body.get("language", DEFAULT_LANGUAGE)
    api_url = os.getenv("LANGUAGETOOL_API_URL", DEFAULT_API_URL)

    if "fields" in body:
        fields = body.get("fields", {})
        if not isinstance(fields, dict):
            return func.HttpResponse(
                json.dumps({"error": "fields must be an object of string values"}),
                status_code=400,
                mimetype="application/json",
            )

        results: Dict[str, Any] = {}
        for key, value in fields.items():
            if not isinstance(value, str):
                results[key] = {"error": "value must be a string"}
                continue

            success, payload = _check_text(value, language, api_url)
            results[key] = payload if success else {"error": payload.get("error")}

        return func.HttpResponse(
            json.dumps({"results": results, "language": language}),
            status_code=200,
            mimetype="application/json",
        )

    text = body.get("text") or req.params.get("text")
    if not text:
        return func.HttpResponse(
            json.dumps(
                {
                    "error": "Provide a 'text' string or 'fields' object in the request body.",
                    "example": {"text": "This are bad sentence."},
                }
            ),
            status_code=400,
            mimetype="application/json",
        )

    success, payload = _check_text(text, language, api_url)
    if not success:
        return func.HttpResponse(
            json.dumps(payload),
            status_code=502,
            mimetype="application/json",
        )

    return func.HttpResponse(
        json.dumps({"results": payload, "language": language}),
        status_code=200,
        mimetype="application/json",
    )
