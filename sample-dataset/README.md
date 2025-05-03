## Sample Dataset for Contoso Grocery

We have dataset for the following areas
- Grocery Store Departments
- Product SKUs
- Product SKU Pricing
- Product SKU Inventory Levels
- Net Sales for Each SKU

In our demos and tests, we are going to upload the following data set to our Azure Blob Store storage account
- Grocery Store Departments

Then we are going to upload the following data set to the respective Cosmos DB containers:
- Net Sales
- Product Inventory
- Product Pricing
- Product SKUs

Then we will set up Indexes for all 5 data sets in our AI Search Service
- Grocery Store Departments
- Product SKUs
- Product SKU Pricing
- Product SKU Inventory Levels
- Net Sales for Each SKU
  
Finally we will configure Skillsets and Data Sources for indexers that will migrate our datasets from the data sources into our AI Search instance

We can now test how to create/retrieve/delete indices, documents and indexers from the MCP service
