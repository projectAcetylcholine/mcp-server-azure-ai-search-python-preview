#  MCP Service for Azure AI Search

This MCP service provides you with the following capabilities

- Retrieve a List of AI Search Indices from your Service
- Get Details about the Schema and Configuration of a Specific AI Search Service
- Create new Indicies
- Update Existing Indices
- Run Queries against specific AI Search Indices
- Configure and Run Indexers

### Pre-Requisites

You will need to have configured an Service Principal that will be used to authentic against the AI Search service you are interacting with. You may also use the AI Search Key with read/write privilleges on the index dependening on what capabilities you are looking to leverage from the service. 

Python 3.12 or later is needed and you have to install uv as well to leverage the service.

The repository below contains a Terraform script that can accelerate the provisioning of an AI Search service and service principal necessary to help you get started.

### Installing Dependencies

Follow the links below to install uv, python and the module containing the MCP service


## Configuration of Environment Variables in MCP Host

If you are authenticating with a managed identity you will need to pass in the enviroment variables in your MCP host configuration. You can also use the AI Search API Key to Authenticate.

The authentication method and search endpoints needs to be specified. These are required environment variables

If you are authenticating with a service principal, then you should configure the following variable:
- AZURE_AUTHENTICATION_METHOD
- AZURE_AI_SEARCH_ENDPOINT
- AZURE_TENANT_ID
- AZURE_CLIENT_ID
- AZURE_CLIENT_SECRET

If you are authenticating with an API key, then you have to configure the following environment variables:
- AZURE_AUTHENTICATION_METHOD
- AZURE_AI_SEARCH_ENDPOINT
- AZURE_AUTHENTICATION_METHOD
- AZURE_AI_SEARCH_API_KEY

You can also filter the list of tools returned to your MCP host by specifying a comma-delimited list of tool groups in your configuration.
The following tool groups are available for the AZURE_AI_SEARCH_MCP_TOOL_GROUPS variable:

- READ_INDEX - tools used to list all the indices in the service
- READ_DOCUMENTS - tools used to query the indices to retrieve documents
- WRITE_INDEX - tools used to Create, delete, update, or configure indices
- WRITE_DOCUMENTS - tools for Adding, Updating or Deleting Documents documents from an index
- READ_INDEXERS - tools used to list indexers available
- WRITE_INDEXERS - tools used to configure indexers in the service
- RUN_INDEXERS - Start indexers to automatically crawl data sources and view the results

| Environment Variable              | Value Data Type  | Why It Is Needed                                                                                             |
|-----------------------------------|------------------|--------------------------------------------------------------------------------------------------------------|
| AZURE_AUTHENTICATION_METHOD       | `string`         | `"service-principal"` for service principal based, or `"api-search-key"` for key-based access.               |
| AZURE_AI_SEARCH_ENDPOINT          | `string (URL)`   | Specifies the Azure AI Search endpoint URL; used to send REST API requests to the service.                   |
| AZURE_TENANT_ID                   | `string`         | Identifies the Azure Active Directory (AAD) tenant used for authentication via the Service Principal.        |
| AZURE_CLIENT_ID                   | `string`         | The unique identifier of the Service Principal (app registration) used for Azure authentication.             |
| AZURE_CLIENT_SECRET               | `string`         | The secret credential for the Service Principal; used to authenticate and obtain tokens from AAD.            |
| AZURE_AI_SEARCH_API_KEY           | `string`         | Used to authenticate read/write API requests to the Azure AI Search instance; must be kept secure.           |
| AZURE_AI_SEARCH_MCP_TOOL_GROUPS   | `string`         | A comma-delimited list of groups of tools you would like to filter when retrieving tools for your MCP host   |

