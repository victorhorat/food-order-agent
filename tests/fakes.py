from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from pydantic import PrivateAttr


class ScriptedToolCallingChatModel(BaseChatModel):
    """Fake chat model que devolve mensagens roteirizadas, suportando bind_tools.

    O BaseChatModel padrão levanta NotImplementedError em bind_tools, o que
    quebra create_agent (ele sempre chama bind_tools nos modelos). Aqui a
    gente só ignora as tools e devolve o próprio modelo.
    """

    responses: list[BaseMessage]
    _index: int = PrivateAttr(default=0)

    def bind_tools(self, tools, **kwargs):
        return self

    def _generate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:
        message = self.responses[self._index]
        self._index += 1
        return ChatResult(generations=[ChatGeneration(message=message)])

    @property
    def _llm_type(self) -> str:
        return "scripted-tool-calling-fake"
