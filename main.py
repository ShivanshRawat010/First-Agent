from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI
from langchain.messages import HumanMessage, ToolMessage, SystemMessage
from weather_tool import get_weather
from news_tool import get_news
from rich import print

# model = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")
model = ChatMistralAI(model = "mistral-small-latest")

llm_with_tools = model.bind_tools([get_weather,get_news])

tools = {
  "get_weather" : get_weather,
  "get_news" : get_news
}

messages = []

print("----Scout AI----\n")
print("Type \"exit\" to exit\n")

while True:

  message = input("You: ")

  if message == "exit":
    break

  messages.append(HumanMessage(message))

  response = llm_with_tools.invoke(messages)

  messages.append(response)

  if response.tool_calls:
    for tool_call in response.tool_calls:
      
      permission = input(f"System: Allow access to {tool_call["name"]} (yes/no): ")

      if permission == "no":
        messages.append(SystemMessage("Permission denied to access tools."))
        print("System: Permission denied to access tools.")
        break

      elif permission == "yes":
        tool_result = tools[tool_call["name"]].invoke(tool_call["args"])
        tool_message = ToolMessage(
          content=str(tool_result),
          tool_call_id=tool_call["id"]
        )
        messages.append(tool_message)
      
      else:
        print("System: Invalid input!")
        break
    
    result = llm_with_tools.invoke(messages)
    print(f"AI: {result.content}")
    messages.append(result)

  else:
    print(f"AI: {response.content}")
