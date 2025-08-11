from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import ChatRequest, ChatResponse, SuggestionRequest, SuggestionResponse
from .services.okr_suggester import generate_okrs
from .services.chat_assistant import generate_reply

app = FastAPI(title="Selamnew OKR Copilot API", version="0.1.0")

# Allow all origins for MVP; tighten later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/suggest_okrs", response_model=SuggestionResponse)
async def suggest_okrs(request: SuggestionRequest) -> SuggestionResponse:
    objectives = generate_okrs(request)
    return SuggestionResponse(objectives=objectives)


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    reply = generate_reply(request)
    return ChatResponse(reply=reply)