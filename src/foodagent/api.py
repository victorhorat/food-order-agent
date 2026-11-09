from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from langchain_core.language_models.chat_models import BaseChatModel
from pydantic import BaseModel

from foodagent.agent import build_model, chat
from foodagent.config import Settings, load_settings
from foodagent.sessions import SessionStore

_state: dict[str, object] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = load_settings()
    _state["settings"] = settings
    _state["model"] = build_model(settings)
    _state["sessions"] = SessionStore()
    yield
    _state.clear()


app = FastAPI(
    title="food-order-agent",
    description="Agente conversacional de pedidos de comida com tool calling",
    version="0.1.0",
    lifespan=lifespan,
)


def get_settings() -> Settings:
    return _state["settings"]  # type: ignore[return-value]


def get_model() -> BaseChatModel:
    return _state["model"]  # type: ignore[return-value]


def get_sessions() -> SessionStore:
    return _state["sessions"]  # type: ignore[return-value]


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str
    carrinho: list[dict]
    subtotal: float


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(
    request: ChatRequest,
    model: BaseChatModel = Depends(get_model),
    settings: Settings = Depends(get_settings),
    sessions: SessionStore = Depends(get_sessions),
) -> ChatResponse:
    session = sessions.get(request.session_id)
    reply = chat(model, session, request.message, settings)
    return ChatResponse(
        reply=reply,
        carrinho=session.cart.list_items(),
        subtotal=session.cart.subtotal(),
    )
