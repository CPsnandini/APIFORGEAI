# APIForge AI

An AI-assisted backend workspace for testing and managing REST APIs, with Gemini-powered
documentation generation, HTTP error explanation, and automated test case generation.

## Tech Stack
- **Backend:** Flask, Flask-SQLAlchemy, Flask-JWT-Extended
- **AI:** Google Gemini API (`google-genai`)
- **Database:** SQLite (dev) / PostgreSQL (production)
- **Frontend:** Vanilla HTML/CSS/JS (no framework, no build step)

## Features
- Secure signup/login with JWT authentication
- Send arbitrary HTTP requests (GET/POST/PUT/PATCH/DELETE) to any URL and inspect the response
- Save and manage frequently used API endpoints
- Automatic request history logging, scoped per user
- AI-generated API documentation for any saved endpoint
- Plain-language explanations of HTTP error codes
- AI-generated test cases for any saved endpoint

## Local setup
\`\`\`bash
git clone https://github.com/your-username/APIForgeAI.git
cd APIForgeAI
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\Activate.ps1
pip install -r requirements.txt
\`\`\`

Create a `.env` file:
\`\`\`
SECRET_KEY=your-random-secret
JWT_SECRET_KEY=your-random-jwt-secret
GEMINI_API_KEY=your-gemini-api-key
\`\`\`

\`\`\`bash
python app.py
\`\`\`
Visit `http://127.0.0.1:5000`.

## API Overview
| Route | Method | Description |
|---|---|---|
| `/auth/signup` | POST | Create a user |
| `/auth/login` | POST | Get a JWT |
| `/api/send` | POST | Execute an arbitrary HTTP request |
| `/api/endpoints` | GET/POST | List or save endpoints |
| `/api/history` | GET | View recent request history |
| `/ai/generate-docs/<id>` | POST | Generate docs for a saved endpoint |
| `/ai/explain-error` | POST | Explain an HTTP status code |
| `/ai/generate-tests/<id>` | POST | Generate test cases for a saved endpoint |

## Live demo
https://apiforgeai.onrender.com