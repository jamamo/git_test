# git_test

## Azure Function: GrammarCheck

This repo includes a Python Azure Function that checks grammar for Power Automate fields using the LanguageTool API.

### Folder layout

```
azure-function/
  GrammarCheck/
    __init__.py
    function.json
  host.json
  requirements.txt
```

### Environment variables

* `LANGUAGETOOL_API_URL` (optional) - defaults to `https://api.languagetool.org/v2/check`.

### Request examples

#### Check a single text value

```json
{
  "text": "This are bad sentence.",
  "language": "en-US"
}
```

#### Check multiple Power Automate fields

```json
{
  "language": "en-US",
  "fields": {
    "title": "This are bad sentence.",
    "description": "He go to store yesterday."
  }
}
```

### Response example

```json
{
  "results": {
    "title": {
      "matches": [
        {
          "message": "This looks like a grammar error.",
          "shortMessage": "",
          "offset": 5,
          "length": 3,
          "replacements": ["is"],
          "rule": "SUBJECT_VERB_AGREEMENT"
        }
      ],
      "language": "English"
    }
  },
  "language": "en-US"
}
```

### Notes for Power Automate

* Use the HTTP action to call the function endpoint.
* Pass the fields you want to validate in the `fields` object.
* The response returns a `results` object keyed by field name so you can loop through and decide which field needs correction.
