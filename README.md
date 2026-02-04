# git_test

This repository demonstrates basic Git usage and now includes a simple
medical chatbot using the OpenAI API.

## Medical Chatbot

The `medical_chatbot.py` script allows you to ask general medical
questions. The bot attempts to answer in a professional manner while
reminding you to always seek advice from a qualified healthcare
professional.

### Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`
- An `OPENAI_API_KEY` environment variable containing your OpenAI API key. Copy
  `.env.example` to `.env` and add your key (the `.env` file is ignored by Git
  via `.gitignore`).

### Running

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the chatbot:

```bash
python medical_chatbot.py
```

Type your question and press Enter. Type `exit` or `quit` to stop.

**This tool does not replace professional medical advice. Always consult
a healthcare professional for medical concerns.**
