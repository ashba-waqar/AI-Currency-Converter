import os
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent


os.environ["GOOGLE_API_KEY"] = "AIzaSyC2rIYD7tX8AgFLNrVwq_Rnlyc4RYTrzkA"


@tool
def calculator(expression: str) -> str:
    """Useful for answering questions about math."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

@tool
def get_exchange_rate(base_currency: str, target_currency: str) -> str:
    """Useful for looking up the real-time exchange rate between two currencies. Use standard 3-letter currency codes (like USD, PKR, GBP, KWD)."""
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency.upper()}"
        response = requests.get(url)
        data = response.json()
        
        rate = data['rates'].get(target_currency.upper())
        if rate:
            return f"The real-time exchange rate from {base_currency} to {target_currency} is {rate}"
        else:
            return f"Sorry, I couldn't find the rate for {target_currency}."
    except Exception as e:
        return f"Error fetching rate: {str(e)}"

# 3. SETUP THE MODERN LANGGRAPH AGENT
def main():
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    tools = [calculator, get_exchange_rate]
    
    
    agent = create_react_agent(llm, tools)

    print("\n" + "="*50)
    print("🤖 MODERN Live Currency Assistant is READY! (Type 'quit' to exit)")
    print("="*50 + "\n")

    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['quit', 'exit']:
            print("Goodbye! 👋")
            break
            
        try:
            
            response = agent.invoke({
                "messages": [("user", user_input)]
            })
            
            
            print(f"\n🤖 Agent: {response['messages'][-1].content}\n")
            
        except Exception as e:
            print(f"\nOops, an error occurred: {e}\n")

if __name__ == "__main__":
    main()