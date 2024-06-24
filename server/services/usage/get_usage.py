import asyncio
from fastapi import FastAPI, HTTPException
from typing import List, Optional

import httpx

from services.usage.data_schema import MessageItem, MessagesResponse, ReportItem, UsageItem
from services.usage.calculate_cost import calculate_total_cost
from services.usage.constans import MESSAGES_URL, REPORTS_URL


async def get_messages() -> List[MessageItem]:
    """
    Fetches messages from an external API asynchronously using HTTP GET request.

    Returns:
        List[MessageItem]: List of messages fetched from the API.

    Raises:
        HTTPException: If the HTTP request to the API fails or returns an error status code.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(MESSAGES_URL)
            response.raise_for_status()
            data = response.json()
            validated_data = MessagesResponse(**data)
            return validated_data.messages
        except httpx.HTTPStatusError as http_err:
            # Handle HTTP errors (4xx, 5xx) here
            raise HTTPException(status_code=http_err.response.status_code, detail=str(http_err))
        except (httpx.RequestError, ValueError) as err:
            # Handle other types of errors (connection errors, JSON decoding errors) here
            raise HTTPException(status_code=500, detail=str(err))


async def get_report(report_id: int) -> Optional[ReportItem]:
    """
    Fetches a report from an external API asynchronously using HTTP GET request.

    Args:
        report_id (int): The ID of the report to fetch.

    Returns:
        ReportItem or None: ReportItem containing the report data if successful, or None if unsuccessful.
    """
    report_url = REPORTS_URL.format(report_id)
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(report_url)
            response.raise_for_status()
            data = response.json()
            validated_data = ReportItem(**data)
            return validated_data
        except httpx.HTTPStatusError as http_err:
            if http_err.response.status_code == 404:
                # Log the error and return None if report does not exist
                print(f"Report with ID {report_id} does not exist.")
                return None
            raise HTTPException(status_code=http_err.response.status_code, detail=str(http_err))
        except (httpx.RequestError, ValueError) as err:
            raise HTTPException(status_code=500, detail=str(err))


async def get_usage() -> List[UsageItem]:
    messages = await get_messages()
    usage_data = []

    async def fetch_report(report_id):
        if report_id:
            return await get_report(report_id)
        return None

    # Fetch reports for all messages concurrently
    report_tasks = [fetch_report(message.report_id) for message in messages]
    reports = await asyncio.gather(*report_tasks)

    for message, report in zip(messages, reports):
        try:
            if report:
                report_name = report.name
                credits_used = float(report.credit_cost)
            else:
                report_name = None
                credits_used = calculate_total_cost(message.text)

            usage_item = UsageItem(
                message_id=message.id,
                timestamp=message.timestamp,
                report_name=report_name,
                credits_used=credits_used
            )
            usage_data.append(usage_item)

        except KeyError as e:
            raise HTTPException(status_code=500, detail=f"Error processing message: {message.id}. Details: {str(e)}")

    return usage_data
