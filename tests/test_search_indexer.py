
from unittest.mock import patch, MagicMock

import pytest

from data_access_objects import SearchIndexerDao

@pytest.fixture
def mock_dao():
    with patch("azure.search.documents.indexes.SearchIndexerClient") as mock_client_class:
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        dao = SearchIndexerDao()
        dao.client = mock_client
        yield dao


def test_list_indexers(mock_dao):
    mock_dao.client.get_indexer_names.return_value = ["indexer1", "indexer2"]

    result = mock_dao.list_indexers()

    assert result == ["indexer1", "indexer2"]
    mock_dao.client.get_indexer_names.assert_called_once()


def test_get_indexer(mock_dao):
    mock_indexer = MagicMock()
    mock_indexer.serialize.return_value = {"name": "indexer1"}

    mock_dao.client.get_indexer.return_value = mock_indexer

    result = mock_dao.get_indexer("indexer1")

    assert result == {"name": "indexer1"}
    mock_dao.client.get_indexer.assert_called_once_with("indexer1")


def test_create_indexer(mock_dao):
    mock_indexer = MagicMock()
    mock_indexer.serialize.return_value = {"name": "new-indexer"}

    mock_dao.client.create_indexer.return_value = mock_indexer

    result = mock_dao.create_indexer(mock_indexer)

    assert result == {"name": "new-indexer"}
    mock_dao.client.create_indexer.assert_called_once_with(mock_indexer)


def test_delete_indexer(mock_dao):
    mock_dao.delete_indexer("test-indexer")

    mock_dao.client.delete_indexer.assert_called_once_with("test-indexer")


def test_list_data_sources(mock_dao):
    mock_dao.client.get_data_source_connection_names.return_value = ["source1", "source2"]

    result = mock_dao.list_data_sources()

    assert result == ["source1", "source2"]
    mock_dao.client.get_data_source_connection_names.assert_called_once()


def test_get_data_source(mock_dao):
    mock_data_source = MagicMock()
    mock_data_source.serialize.return_value = {"name": "source1"}

    mock_dao.client.get_data_source_connection.return_value = mock_data_source

    result = mock_dao.get_data_source("source1")

    assert result == {"name": "source1"}
    mock_dao.client.get_data_source_connection.assert_called_once_with(name="source1")


def test_list_skill_sets(mock_dao):
    mock_dao.client.get_skillset_names.return_value = ["skillset1", "skillset2"]

    result = mock_dao.list_skill_sets()

    assert result == ["skillset1", "skillset2"]
    mock_dao.client.get_skillset_names.assert_called_once()


def test_get_skill_set(mock_dao):
    mock_skillset = MagicMock()
    mock_skillset.serialize.return_value = {"name": "skillset1"}

    mock_dao.client.get_skillset.return_value = mock_skillset

    result = mock_dao.get_skill_set("skillset1")

    assert result == {"name": "skillset1"}
    mock_dao.client.get_skillset.assert_called_once_with("skillset1")
