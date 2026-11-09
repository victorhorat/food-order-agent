from importlib import resources

from langchain.agents import create_agent
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI

from foodagent.catalog import catalogo_padrao
from foodagent.config import Settings
from foodagent.sessions import Session
from foodagent.tools import make_tools

SYSTEM_PROMPT = resources.files("foodagent.prompts").joinpath("agent.md").read_text("utf-8")


def build_model(settings: Settings) -> ChatOpenAI:
    return ChatOpenAI(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key,
        model=settings.llm_model,
    )


def chat(model: BaseChatModel, session: Session, message: str, settings: Settings) -> str:
    tools = make_tools(session.cart, catalogo_padrao(), settings)
    agent = create_agent(model=model, tools=tools, system_prompt=SYSTEM_PROMPT)

    session.history.append(HumanMessage(content=message))
    result = agent.invoke({"messages": session.history})
    session.history = result["messages"]

    final_message = session.history[-1]
    if isinstance(final_message, AIMessage):
        return final_message.content
    return ""
