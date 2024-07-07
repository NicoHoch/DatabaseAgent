from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from models.databaseAgent import SQLCommand
from langchain.tools import tool
import sqlite3
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage


class DatabaseAgentService:
    def __init__(self) -> None:
        self.llm = ChatOpenAI(
            model="gpt-4o", temperature=0, max_tokens=500, max_retries=2
        )

    def get_sql_query(self, userInput: str) -> str:
        systemMessage = SystemMessage(
            content=[
                {
                    "type": "text",
                    "text": "You are an SQL expert. Write an SQL query according to the user's request, sent to a database which was setup with the following schema: 'CREATE TABLE IF NOT EXISTS purchases(purchase_id INTEGER PRIMARY KEY, store_id INTEGER, total_cost FLOAT, FOREIGN KEY(store_id) REFERENCES stores(store_id))' and 'CREATE TABLE IF NOT EXISTS stores(store_id INTEGER PRIMARY KEY, location TEXT, name TEXT)'",
                }
            ]
        )

        humanMessage = HumanMessage(content=[{"type": "text", "text": userInput}])

        chat = [systemMessage, humanMessage]

        structured_llm = self.llm.with_structured_output(SQLCommand)

        response: SQLCommand = structured_llm.invoke(chat)
        return response

    def execute_sql_query(self, sqlQuery: str):
        """Check robot's current position."""
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS purchases(purchase_id INTEGER PRIMARY KEY, store_id INTEGER, total_cost FLOAT, FOREIGN KEY(store_id) REFERENCES stores(store_id))"
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS stores(store_id INTEGER PRIMARY KEY, location TEXT, name TEXT)"
        )

        try:
            cursor.execute(sqlQuery)
        except Exception as e:
            return "Error: " + str(e)

        connection.commit()

        results = cursor.fetchall()
        connection.close()
        return results

    def sql_agent(self, userInput: str) -> str:

        tools = [self.execute_sql_query]

        llm = self.llm
        agent_executor = create_react_agent(llm, tools)

        systemMessage = SystemMessage(
            content=[
                {
                    "type": "text",
                    "text": "You are an SQL expert. Write an SQL query according to the user's request, sent to a database which was setup with the following schema: 'CREATE TABLE IF NOT EXISTS purchases(purchase_id INTEGER PRIMARY KEY, store_id INTEGER, total_cost FLOAT, FOREIGN KEY(store_id) REFERENCES stores(store_id))' and 'CREATE TABLE IF NOT EXISTS stores(store_id INTEGER PRIMARY KEY, location TEXT, name TEXT)'",
                }
            ]
        )

        humanMessage = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": userInput,
                }
            ]
        )

        chat = [systemMessage, humanMessage]
        response = agent_executor.invoke({"messages": chat})

        return response["messages"][len(response["messages"]) - 1].content
