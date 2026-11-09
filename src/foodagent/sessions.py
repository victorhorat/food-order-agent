from dataclasses import dataclass, field

from langchain_core.messages import BaseMessage

from foodagent.cart import Cart


@dataclass
class Session:
    cart: Cart = field(default_factory=Cart)
    history: list[BaseMessage] = field(default_factory=list)


class SessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}

    def get(self, session_id: str) -> Session:
        if session_id not in self._sessions:
            self._sessions[session_id] = Session()
        return self._sessions[session_id]
