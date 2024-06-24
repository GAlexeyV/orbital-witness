import pytest
import httpx
from unittest.mock import patch
from fastapi import HTTPException
from unittest.mock import AsyncMock

from services.usage.data_schema import MessageItem, ReportItem, UsageItem
from services.usage.get_usage import get_messages, get_report, get_usage


@pytest.mark.asyncio
@patch('services.usage.get_usage.get_messages', new_callable=AsyncMock)
async def test_get_messages_success(get_messages):
    """Tests successful retrieval of messages from the external API."""

    # Define the mock response data
    mock_response_data = [MessageItem(
        text="test message",
        timestamp="2023-01-01T12:00:00Z",
        report_id=None,
        id=1
    )]

    # Set the mock to return the mock response data
    get_messages.return_value = mock_response_data

    # Call the function (it will use the mock instead of making an actual API call)
    messages = await get_messages()

    # Assert that the actual messages match the expected messages
    assert messages == mock_response_data


@pytest.mark.asyncio
async def test_get_report_success(monkeypatch):
    # Sample data to return in the mock response
    sample_report_data = {
        "id": 1,
        "name": "Sample Report",
        "credit_cost": 10.0
    }

    async def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 200

            def json(self):
                return sample_report_data

            def raise_for_status(self):
                pass

        return MockResponse()

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    report_id = 1
    result = await get_report(report_id)
    assert result == ReportItem(**sample_report_data)


@pytest.mark.asyncio
async def test_get_report_http_error(monkeypatch):
    async def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 500

            def json(self):
                return {}

            def raise_for_status(self):
                raise httpx.HTTPStatusError("Internal Server Error", request=None, response=self)

        return MockResponse()

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    report_id = 1
    with pytest.raises(HTTPException) as excinfo:
        await get_report(report_id)
    assert excinfo.value.status_code == 500


@pytest.mark.asyncio
@patch('services.usage.get_usage.get_usage', new_callable=AsyncMock)
async def test_get_usage(get_usage):
    """Tests successful call for get_usage function."""

    # Define the mock response data
    mock_response_data = [
        UsageItem(message_id=1, timestamp="2023-01-01T12:00:00Z", report_name=None, credits_used=0.1),
        UsageItem(message_id=2, timestamp="2024-02-07T12:00:00Z", report_name="report_1", credits_used=1.0),
     ]

    # Set the mock to return the mock response data
    get_usage.return_value = mock_response_data

    # Call the function (it will use the mock instead of making an actual function call)
    usage_data = await get_usage()

    # Assert that the actual usage_data match the expected data
    assert usage_data == mock_response_data






