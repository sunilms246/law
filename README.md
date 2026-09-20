# Legal Section Finder (India) — prototype

A RAG (retrieval + LLM) tool that takes a plain-language description of a
situation and finds which Indian law sections apply, using Gemini's free
API to explain the match and suggest next steps.

Currently covers three domains:
- **Criminal** — Bharatiya Nyaya Sanhita (BNS), 2023
- **Consumer complaints** — Consumer Protection Act, 2019
- **Landlord/tenant** — Transfer of Property Act, 1882 (general principles only, no state-specific rent control law yet)

## Live demo

Deployed on Render: **https://law-b533.onrender.com/**

## How it works

1. You type your situation into the web form
2. `rag/retrieve.py` searches `data/sections.json` using TF-IDF (a
   classic word-importance-weighted search — no AI needed for this step)
   and returns the closest-matching sections
3. `rag/generate.py` sends only those retrieved sections to Gemini,
   which explains them in plain language and says what to do — it's
   instructed to never invent a section number that wasn't retrieved
4. If nothing matches well, the app says so instead of forcing an answer

## Folder structure

```
legal/
├── web_app.py           entry point — FastAPI web app (run this)
├── requirements.txt
├── render.yaml          Render deploy config
├── .env                 your real API key (you create this — not committed)
├── env.example          template showing the expected format
├── .gitignore
├── data/
│   └── sections.json    the law "database" — one entry per section
├── rag/
│   ├── retrieve.py      TF-IDF search over the sections
│   └── generate.py      LLM call (Gemini)
└── templates/
    └── index.html       the web page (form + answer)
```

## Setup

1. **Install dependencies**
   ```
   python -m pip install -r requirements.txt
   ```
   (Use `python -m pip`, not just `pip`, to make sure packages install
   into the same Python that runs the script — on Windows especially,
   these can silently point to different installs.)

2. **Get a free Gemini API key**
   Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey),
   sign in with a Google account, create a key. No card required.

3. **Create your `.env` file**
   In the project's root folder, create a file named exactly `.env`:
   ```
   GEMINI_API_KEY=your-actual-key-here
   ```

4. **Run it**
   ```
   python web_app.py
   ```
   Open http://localhost:8000 and type a situation
   (e.g. "my landlord won't fix the leaking roof").

## Extending the data

The law "database" is just `data/sections.json` — a list of entries like:

```json
{
  "domain": "criminal",
  "act": "Bharatiya Nyaya Sanhita, 2023",
  "section": "303",
  "title": "Theft",
  "summary": "Plain-language explanation of what the section covers.",
  "what_to_do": "Practical next step for the user.",
  "punishment": "What the law prescribes.",
  "cognizable": true,
  "bailable": true,
  "keywords": ["words", "a user", "might type"]
}
```

Add more entries in the same format to expand coverage — the retrieval
and generation code doesn't need to change as the dataset grows.

## Known limitations (current prototype stage)

- Only 32 sample sections loaded — real coverage requires a much larger dataset
- TF-IDF matching is exact-word-based; it can miss situations phrased very
  differently from the stored keywords (upgrading to semantic/embedding
  search is a planned next step)
- Landlord/tenant law is state-specific in India; this prototype only
  covers general central-law principles, not any state's Rent Control Act
- No user accounts or saved search history yet (planned for phase 2)
- Deployed on Render's free tier: after ~15 min without traffic the app
  sleeps and takes about a minute to wake on the next visit
- This tool gives general legal information, not legal advice — every
  answer should end by pointing the user to a licensed advocate

## Roadmap

See `PROGRESS.md` for what's been built so far and what's next.