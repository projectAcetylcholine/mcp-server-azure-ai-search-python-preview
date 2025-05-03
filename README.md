#  MCP Service for Azure AI Search

This MCP service provides you with the following capabilities

- Retrieve a List of AI Search Indices from your Service
- Get Details about the Schema and Configuration of a Specific AI Search Service
- Create new Indices
- Update Existing Indices
- Run Queries against specific AI Search Indices
- Create and Update indexers


### Available Tools

We are continuously working on adding and upgrading the service capabilities. More tools are going to be added in the near future.

For the time being, the following tools are available from the service:

| Tool Name              | Tool Group     | Tool Description                                                              |
|------------------------|----------------|-------------------------------------------------------------------------------|
| retrieve_index_names   | READ_INDEX     | Retrieve all names of indexes from the AI Search Service                      |   
| retrieve_index_schemas | READ_INDEX     | Retrieve all index schemas from the AI Search Service                         | 
| retrieve_index_schema  | READ_INDEX     | Retrieve the schema for a specific index from the AI Search Service           | 
| query_index            | READ_DOCUMENTS | Retrieve the schema for a specific index from the AI Search Service           |


### MCP Service Tool Groups

We do not want your MCP Host to be overwhelmed with the amount of tools coming from this service.

These are the available tool groups and their purposes:

- READ_INDEX - tools used to list and describe the indices in the service
- WRITE_INDEX - tools used to Create, delete, update, or configure indices
- READ_DOCUMENTS - tools used to query the indices to retrieve documents
- WRITE_DOCUMENTS - tools for Adding, Updating or Deleting documents from an index
- READ_INDEXERS - tools used to list indexers available
- WRITE_INDEXERS - tools used to configure indexers,  data sources & skill sets
- READ_INDEXERS - tools used to retrieve information about data sources, skill sets and indexers

### Pre-Requisites

You will need to have configured a Service Principal that will be used to authentic against the AI Search service you are interacting with. You may also use the AI Search Key with read/write privilleges on the index dependening on what capabilities you are looking to leverage from the service. 

Python 3.12 or later is needed, and you have to install uv as well to leverage the service.

The repository below contains a Terraform script that can accelerate the provisioning of an AI Search service and service principal necessary to help you get started.

### Installing Dependencies

Follow the links below to install uv, python and the module containing the MCP service

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

