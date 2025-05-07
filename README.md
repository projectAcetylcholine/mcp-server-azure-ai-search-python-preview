#  Experimental MCP Service for Azure AI Search

This experimental MCP service provides you with the following capabilities:

- Retrieve a List of AI Search Indices from your Service
- Get Details about the Schema and Configuration of a Specific AI Search Service
- Create new Indices
- Update Existing Indices
- Run Queries against specific AI Search Indices
- Create and Update indexers

### Important Disclaimers

We are still implementing and testing out these capabilities. 

Some of the tool groups described above are not yet available but would be coming soon.

We are continuously working on adding and upgrading the service capabilities. More tools are going to be added in the near future.

These tools have the ability to modify data in your AI Search Service. 

Please note that all tools are currently marked `experimental` and may change behavior `without advanced notice`.

You should always review and verify all AI-generated content for accuracy and correctness.

Please proceed with caution and use at your own risk.

### Available Tools

For the time being, the following tools are available from the service:

| Tool Name             | Tool Group      | Tool Description                                                                 |
|-----------------------|-----------------|----------------------------------------------------------------------------------|
| list_index_names      | READ_INDEX      | Retrieve all names of indexes from the AI Search Service                         |   
| list_index_schemas    | READ_INDEX      | Retrieve all index schemas from the AI Search Service                            | 
| retrieve_index_schema | READ_INDEX      | Retrieve the schema for a specific index from the AI Search Service              | 
| create_index          | WRITE_INDEX     | Creates a new index                                                              |
| delete_index          | WRITE_INDEX     | Removes an existing index                                                        |
| add_document          | WRITE_DOCUMENTS | Adds a document to the index                                                     |
| delete_document       | WRITE_DOCUMENTS | Removes a document from the index                                                |
| query_index           | READ_DOCUMENTS  | Searches a specific index to retrieve matching documents                         |
| get_document_count    | READ_DOCUMENTS  | Returns the total number of documents in the index                               |
| list_indexers         | READ_INDEXER    | Retrieve all names of indexers from the AI Search Service                        |
| get_indexer           | READ_INDEXER    | Retrieve the full definition of a specific indexer from the AI Search Service    |
| create_indexer        | WRITE_INDEXER   | Create a new indexer in the Search Service with the skill, index and data source |
| delete_indexer        | WRITE_INDEXER   | Delete an indexer from the AI Search Service by name                             |
| list_data_sources     | READ_INDEXER    | Retrieve all names of data sources from the AI Search Service                    |
| get_data_source       | READ_INDEXER    | Retrieve the full definition of a specific data source                           |
| list_skill_sets       | READ_INDEXER    | Retrieve all names of skill sets from the AI Search Service                      |
| get_skill_set         | READ_INDEXER    | Retrieve the full definition of a specific skill set                             |

### MCP Service Tool Groups

We do not want your MCP Host to be overwhelmed with the amount of tools coming from this service.

These are the available tool groups and their purposes:

- READ_OPERATIONS - tools used for read-only operations
- WRITE_OPERATIONS - tools that are used for creating, modifying or removing entries. Alias for ALL
- READ_INDEX - tools used to list and describe the indices in the service
- WRITE_INDEX - tools used to Create, delete, update, or configure indices
- READ_DOCUMENTS - tools used to query the indices to retrieve documents
- WRITE_DOCUMENTS - tools for Adding, Updating or Deleting documents from an index
- WRITE_INDEXERS - tools used to configure indexers,  data sources & skill sets
- READ_INDEXERS - tools used to retrieve information about data sources, skill sets and indexers

### Pre-Requisites

You will need to have configured a Service Principal that will be used to authentic against the AI Search service you are interacting with. You may also use the AI Search Key with read/write privilleges on the index dependening on what capabilities you are looking to leverage from the service. 

Python 3.12 or later is needed, and you have to install uv as well to leverage the service.

The repository below contains a Terraform script that can accelerate the provisioning of an AI Search service and service principal necessary to help you get started.

### Installing Dependencies

Follow the links below to install uv, python and the module containing the MCP service

- [Installing uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Installing Python if Necessary with uv](https://docs.astral.sh/uv/guides/install-python/)

You can install the mcp service as follows:

````bash

uv build

pip install dist/mcp_server_azure_ai_search_preview-0.3.1-py3-none-any.whl 

# Once installed we can run in from any directory in your MCP host configuration in VSCODE .vscode/mcp.json file
uv run -m mcp_server_azure_ai_search_preview --transport stdio --envFile .env

# If you are running in SSE mode, you can run it as:
uv run -m mcp_server_azure_ai_search_preview --transport sse --envFile .env --host 127.0.0.1 --port 8000
````

The environment file, host and ports are optional. The default values will be used if you do not specify them

You can also clone this git repo and install the service via the main.py file in this repo


## Configuration of Environment Variables in MCP Host

If you are authenticating with a managed identity you will need to pass in the environment variables in your MCP host configuration. You can also use the AI Search API Key to Authenticate.

The authentication method and search endpoints needs to be specified. These are required environment variables

If you are authenticating with a service principal, then you should configure the following variable:
- AZURE_AUTHENTICATION_METHOD - default is "api-search-key"
- AZURE_AI_SEARCH_ENDPOINT
- AZURE_TENANT_ID
- AZURE_CLIENT_ID
- AZURE_CLIENT_SECRET

If you are authenticating with an API key, then you have to configure the following environment variables:
- AZURE_AUTHENTICATION_METHOD - default is "api-search-key"
- AZURE_AI_SEARCH_ENDPOINT
- AZURE_AUTHENTICATION_METHOD
- AZURE_AI_SEARCH_API_KEY

You can also filter the list of tools returned to your MCP host by specifying a comma-delimited list of tool groups in your configuration.

| Environment Variable            | Value Data Type  | Why It Is Needed                                                                                           |
|---------------------------------|------------------|------------------------------------------------------------------------------------------------------------|
| AZURE_AUTHENTICATION_METHOD     | `string`         | `"service-principal"` for service principal based, or `"api-search-key"` for key-based access.             |
| AZURE_AI_SEARCH_ENDPOINT        | `string (URL)`   | Specifies the Azure AI Search endpoint URL; used to send REST API requests to the service.                 |
| AZURE_TENANT_ID                 | `string`         | Identifies the Azure Active Directory (AAD) tenant used for authentication via the Service Principal.      |
| AZURE_CLIENT_ID                 | `string`         | The unique identifier of the Service Principal (app registration) used for Azure authentication.           |
| AZURE_CLIENT_SECRET             | `string`         | The secret credential for the Service Principal; used to authenticate and obtain tokens from AAD.          |
| AZURE_AI_SEARCH_API_KEY         | `string`         | Used to authenticate read/write API requests to the Azure AI Search instance; must be kept secure.         |
| AZURE_AI_SEARCH_API_VERSION     | `string`         | API Version to use.                                                                                        |
| AZURE_AI_SEARCH_MCP_TOOL_GROUPS | `string`         | A comma-delimited list of groups of tools you would like to filter when retrieving tools for your MCP host |


### MCP Host Configuration 

This is an example of the MCP configuration for VScode Agent Mode

````json

{
    "inputs": [
        {
            "type": "promptString",
            "id": "AZURE_AI_SEARCH_API_KEY",
            "description": "AZURE_AI_SEARCH_API_KEY",
            "password": true
        }
    ],
    "servers": {

        "ai_search_mcp": {
            "type": "stdio",
            "command": "uv",

            "args": [
                "run",
                "--directory",
                "/Users/isekpo/Microsoft/mcp-server-azure-ai-search",
                "__main__.py",
                "--transport",
                "stdio"
            ],
            "env": {
                "AZURE_AI_SEARCH_MCP_TOOL_GROUPS": "ALL",
                "AZURE_AI_SEARCH_ENDPOINT": "https://{service_name}.search.windows.net",
                "AZURE_AI_SEARCH_API_VERSION": "2025-03-01-preview",
                "AZURE_AUTHENTICATION_METHOD": "api-search-key",
                "AZURE_AI_SEARCH_API_KEY":  "${input:AZURE_AI_SEARCH_API_KEY}"
            }
        }
    }
}

````

### Running from Agent Frameworks like Pydantic AI

To run this sample Python MCP client, you first need to make sure that the MCP SSE server is up and running. Once it is up and running then you can kick off the MCP client

```bash

# If you have installed the codebase as a pip module you can run it like this to start up the MCP server
uv run -m mcp_server_azure_ai_search_preview --transport sse --envFile .env --host 127.0.0.1 --port 8000

# If you have not yet installed it as a pip module, you can run it as follows to start up the server
cd mcp-server-azure-ai-search/mcp_server_azure_ai_search_preview
uv run __main__.py --transport sse --envFile .env --host 127.0.0.1 --port 8000

```

After the SSE server is up and running, you can now run the MCP client code below:

In this example we have the following python code that can be run as follows:

Go to a different folder and create a requirements.txt file 

These are the contents of the requirements.txt file

````text

pydantic
pydantic-ai

````

Create a Python file called "mcp_agent.py" 

````bash

pip install -r requirements.txt
python mcp_agent.py 

````

````python 

from openai import AsyncAzureOpenAI
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerHTTP
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from rich.prompt import Prompt

server = MCPServerHTTP(url='http://127.0.0.1:8000/sse')

model_name = 'gpt-4o-mini'

client = AsyncAzureOpenAI()
model = OpenAIModel(model_name, provider=OpenAIProvider(openai_client=client))
agent = Agent(model, mcp_servers=[server])

server.headers = {"client-id": "izzyacademy.msft"}

global_message = """
Hello AI Search Developer,
I am a helpful assistant and I can answer questions about Contoso Groceries - an online grocery service where shopping is a pleasure. 
I have access to the AI Search Index for Contoso Groceries and can help developers interact with the data and resources in the AI Search service.
Please let me know how I can help you. 
Ask me to show you what tools I have available to support your development efforts. If you forget the tools, please ask me again.

"""
prompt = """
How can I help you?"""

print(global_message)


async def main():
    async with agent.run_mcp_servers():

        while True:
            # Prompt the user for input
            # and send it to the agent for processing
            # Use rich prompt for better user experience
            question = Prompt.ask(prompt)
            result = await agent.run(question)
            print(result.output)

if __name__ == '__main__':
    import asyncio
    import sys
    asyncio.run(main())

````
