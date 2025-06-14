# TDS Virtual TA API

This API answers Tools in Data Science (IIT Madras) questions automatically.

## Setup
```bash
git clone <repo>
cd tds_virtual_ta
pip install -r requirements.txt
python scripts/scrape_and_index.py  # Build data
python run.py  # Start API
```

## Endpoint
POST `/api/ask`

**Payload:**
```json
{
  "question": "Should I use gpt-4o-mini or gpt-3.5?",
  "image": "<optional base64 image>"
}
```

**Response:**
```json
{
  "answer": "Use gpt-3.5 as mentioned.",
  "links": []
}
```

---
# TDS Virtual TA API

This API answers Tools in Data Science (IIT Madras) questions automatically.

## Setup
```bash
git clone <repo>
cd tds_virtual_ta
pip install -r requirements.txt
python scripts/scrape_and_index.py  # Build data
python run.py  # Start API
```

## Endpoint
POST `/api/ask`

**Payload:**
```json
{
  "question": "Should I use gpt-4o-mini or gpt-3.5?",
  "image": "<optional base64 image>"
}
```

**Response:**
```json
{
  "answer": "Use gpt-3.5 as mentioned.",
  "links": []
}
```

---
Let me know if you’d like this exported as a `.zip` or deployed to Render, Railway, or Replit!