from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain_mistralai import ChatMistralAI
from langchain.messages import HumanMessage, ToolMessage, SystemMessage
from weather_tool import get_weather
from news_tool import get_news
from rich import print

import threading

# model = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")
model = ChatMistralAI(model = "mistral-small-latest")

input_lock = threading.Lock()

@wrap_tool_call
def human_approval(request,handler):
  """Ask for human approval before every tool call."""

  tool_name = request.tool_call["name"]

  with input_lock:
    confirm = input(
        f"\n🤖 Agent wants to call '{tool_name}'.\n👉 Approve? (yes/no): "
    )

    if confirm.lower() != "yes":
        print(f"❌ Access denied for {tool_name}.\n")
        return ToolMessage(
            content="Access denied by user.",
            tool_call_id=request.tool_call["id"]
        )

    # Execute the tool and capture its prints completely within the lock
    result = handler(request)
    return result


agent = create_agent(
  model=model, 
  tools=[get_weather,get_news], 
  middleware=[human_approval],
  system_prompt="You are a helpful agent that assists with news and weathers details of a city."
)

print("----Scout AI----\n")
print("Type \"exit\" to exit\n")

while True:
  user_input = input("You: ")

  if user_input == "exit":
    break

  try:
    result = agent.invoke({
        "messages": [
            {"role": "human", "content": user_input}
        ]
    })

    print("Bot:", result["messages"][-1].content)

  except Exception as e:
      print("ERROR:", e)