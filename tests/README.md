
## Running The Unit Tests

```bash

# Install pytest in your environment
pip install pytest

# if you are using uv
uv pip install pytest

````

### Running with Pytest
From the root of the test run the following command:

```bash
# All the tests
pytest

# Specific file
pytest tests/test_search_client.py

# Specific test
pytest tests/test_search_client.py::test_query_index_with_all_params
````


### Running with uv
From the root of the test run the following command:

```bash
# All the tests
uv run pytest

# Specific file
uv run pytest tests/test_search_client.py

# Specific test
uv run pytest tests/test_search_client.py::test_query_index_with_all_params
````