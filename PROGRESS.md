# Progress

## Decisions made
- Jurisdiction: India
- Interaction model: chat (describe situation) + browse — browse not yet built
- First-version domains: **criminal, consumer complaints, landlord/tenant**
  (more domains later if wanted)
- Landlord/tenant scope: general principles only (Transfer of Property Act),
  no state-specific Rent Control Acts for now
- User accounts + saved search history: deferred to phase 2
- LLM API: Gemini (free tier), swapped from initial Claude API version to
  avoid cost while building
- Retrieval: pure-Python TF-IDF (no scikit-learn) — switched from a
  scikit-learn version after Windows blocked its compiled DLL via an
  Application Control security policy

## Built so far

- [x] Project structure (`app.py`, `rag/`, `data/`)
- [x] `data/sections.json` — 32 sample law sections across the 3 domains
      (20 criminal, 7 consumer, 5 landlord)
- [x] `rag/retrieve.py` — pure-Python TF-IDF search, no external
      dependencies, tested working
- [x] `rag/generate.py` — Gemini API call, strictly grounded in retrieved
      sections only (won't invent section numbers), tested working
- [x] `app.py` — interactive CLI tying retrieval + generation together
- [x] `.env` support via `python-dotenv` for API key storage
- [x] `.gitignore` so the real API key never gets committed

## Not built yet

- [ ] Large-scale data: only 32 sections exist; full BNS / Consumer
      Protection Act / Transfer of Property Act coverage is still needed
- [ ] Browse mode (search/list acts and sections directly, not just chat)
- [ ] Semantic/embedding-based search (current TF-IDF misses situations
      phrased very differently from stored keywords)
- [ ] Deployment (Render hosting discussed, not yet set up)
- [ ] User accounts + saved history (phase 2)
- [ ] Proper UI (currently command-line only)

## Next decision point

Expand `data/sections.json` with more sections per domain, or move to
improving retrieval quality first — whichever Suni prioritizes next.
