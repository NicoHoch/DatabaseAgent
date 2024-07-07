import os
from dotenv import load_dotenv

from services.databaseAgent import DatabaseAgentService


load_dotenv()
langchainKey = os.getenv("LANGCHAIN_API_KEY")
openaiKey = os.getenv("OPENAI_API_KEY")

databaseAgentService = DatabaseAgentService()

result = databaseAgentService.sql_agent(
    "Create a new store called 'REWE' with the location 'Munich' and insert two purchases each with the total cost of 7.30 at this store. Additionally, insert a purchase with the total cost of 12.50 at the stores 'Aldi Süd' in Freiburg. If the store does not exist, create them. Return the sum of all purchases in all stores"
)

print(result)
