from langchain_core.pydantic_v1 import BaseModel, Field


class SQLCommand(BaseModel):
    sqlCommand: str = Field(description="The command to execute on the database")
    description: str = Field(description="The description of the command")
