# Progress

## Decisions made
- Jurisdiction: India
- Interaction model: chat (describe situation) via a web form + browse —
  browse not yet built
- First-version domains: **criminal, consumer complaints, landlord/tenant**
  (more domains later if wanted)
- Landlord/tenant scope: general principles only (Transfer of Property Act),
  no state-specific Rent Control Acts for now
- User accounts + saved search history: deferred to phase 2
- LLM API: Gemini (free tier), swapped from initial Claude API version to
  avoid cost while building
- Retrieval: TF-IDF via scikit-learn (`TfidfVectorizer` + cosine similarity)
- Stack: Python — FastAPI web app, deployed on Render (free tier)

## Built so far

- [x] `data/sections.json` — 32 sample law sections across the 3 domains
      (20 criminal, 7 consumer, 5 landlord)
- [x] `rag/retrieve.py` — TF-IDF search (scikit-learn), finds closest
      matches even when wording differs
- [x] `rag/generate.py` — Gemini API call, strictly grounded in retrieved
      sections only (won't invent section numbers)
- [x] `web_app.py` — FastAPI single-page web app (form -> answer ->
      matched sections), the main interface
- [x] `templates/index.html` — the web page UI
- [x] `.env` support via `python-dotenv` for API key storage
- [x] `.gitignore` so the real API key never gets committed
- [x] GitHub repo (`sunilms246/law`), auto-redeploy on push
- [x] Deployment live on Render: https://law-b533.onrender.com/
      (verified: page renders, `/health` returns ok)

## Not built yet

- [ ] Large-scale data: only 32 sections exist; full BNS / Consumer
      Protection Act / Transfer of Property Act coverage is still needed
- [ ] Browse mode (search/list acts and sections directly, not just chat)
- [ ] Semantic/embedding-based search (current TF-IDF misses situations
      phrased very differently from stored keywords)
- [ ] User accounts + saved history (phase 2)

## Notes / gotchas

- Render free tier: the service sleeps after ~15 min without traffic and
  takes about a minute to wake on the next visit, so the first request
  after idle is slow.
- Render's filesystem is ephemeral between deploys — all data must live
  in the repo (`data/sections.json`), not in files the app writes at
  runtime.

## Next decision point

Expand `data/sections.json` with more sections per domain, or move to
improving retrieval quality first — whichever Suni prioritizes next.