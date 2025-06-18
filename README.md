# Women-Assistance-AI

As part of HackViolet '25, we developed Women-Assistance-AI - Sheroes, which is an AI-driven platform designed to assist women in making informed decisions about jobs, locations, and local resources with a focus on safety and trust. The platform leverages advanced language models, web search, and Reddit data to provide comprehensive, trustworthy, and actionable information.

---

## Project Structure
- **Backend**: FastAPI
- **AI Frameworks**: LangChain, LangGraph
- **Frontend**: JavaScript, HTML, CSS
- **Gen AI Agents**: DeepSeek R1, Llama 3.2

---

## Setup & Installation

### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- Azure CLI & Terraform for cloud deployment
- API keys for Tavily, Reddit, and any other required services (set in `.env` files)

### Environment Variables
For Reddit integration, create a `.env` file in `reddit/` with:
```
CLIENT_ID=your_reddit_client_id
CLIENT_SECRET=your_reddit_client_secret
USERNAME=your_reddit_username
PASSWORD=your_reddit_password
USER_AGENT=your_user_agent
```

### Local Development (Manual)
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the API service:
   ```bash
   uvicorn app:app --reload --port 8000
   ```
3. Run the Reddit service:
   ```bash
   cd reddit
   uvicorn app:app --reload --port 8001
   ```
4. Open `static/index.html` in your browser for the frontend (or serve via Nginx).

5. Access the frontend at [http://localhost](http://localhost)

---

## API Endpoints

### Main API (FastAPI)
- `POST /api` — Submit user input, receive orchestrated AI response.
  - Request: `{ "user_input": "I am moving to Chicago, what should I know?" }`
  - Response: `{ "response": "..." }`

### Reddit API
- `GET /posts?subreddits=women&subreddits=safety&limit=5` — Get posts from subreddits.
- `GET /post/{post_id}` — Get content of a specific Reddit post.

---