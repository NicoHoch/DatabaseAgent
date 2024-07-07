## SQL Database Agent
This agentic system utilizes the LangChain Tools to facilitate the retrieval and manipulation of data from a SQL database. It provides functionality to retrieve information as well as insert and update data in the database. 

To get started, follow these steps:

1. Import the necessary modules from the requirements.txt file:
    ```pip install -r requirements.txt```

2. To configure the environment variables, follow these steps:

    - Copy the `.env.template` file and rename it to `.env`.
    - Update the values in the `.env` file according to your specific configuration.

    Make sure to provide the correct values for your environment variables to ensure proper functionality.


2. Change the input string for the function ```databaseAgentService.sql_agent("input string")``` inside the src/main.py file.

3. Run the project.

For more detailed documentation and examples, refer to the [LangChain Tools documentation](https://langchain-tools-docs.example.com).
