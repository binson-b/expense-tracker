import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
import sys
import example_bot

# Patch sys.modules to mock discord, settings, and utils before importing the bot
sys.modules['discord'] = MagicMock()
sys.modules['settings'] = MagicMock()
sys.modules['utils'] = MagicMock()


@pytest.fixture(autouse=True)
def setup_mocks(monkeypatch):
    # Patch settings
    example_bot.settings.DISCORD_TOKEN = "dummy_token"
    example_bot.settings.OpenAI_API = False
    example_bot.settings.OLLAMA_API = False
    example_bot.settings.USE_OLLAMA_API = False
    example_bot.settings.USE_OPENAI_API = False

    # Patch Google Sheet client
    sheet_mock = MagicMock()
    monkeypatch.setattr(example_bot, "sheet", sheet_mock)
    return sheet_mock

@pytest.mark.asyncio
async def test_on_message_hello(monkeypatch):
    message = MagicMock()
    message.author.bot = False
    message.content = "$hello"
    message.channel.send = AsyncMock()

    await example_bot.on_message(message)
    message.channel.send.assert_awaited_with("Hello!")

@pytest.mark.asyncio
async def test_on_message_expense_valid(monkeypatch, setup_mocks):
    message = MagicMock()
    message.author.bot = False
    message.author.name = "Alice"
    message.content = "!expense lunch 12.5 01-06-2024"
    message.channel.send = AsyncMock()

    await example_bot.on_message(message)
    setup_mocks.append_row.assert_called_with(["01-06-2024", "lunch", "12.5", "Alice"])
    message.channel.send.assert_awaited_with("Expense recorded: lunch, 12.5, 01-06-2024, Alice")

@pytest.mark.asyncio
async def test_on_message_expense_invalid(monkeypatch):
    message = MagicMock()
    message.author.bot = False
    message.content = "!expense lunch 12.5"
    message.channel.send = AsyncMock()

    await example_bot.on_message(message)
    message.channel.send.assert_awaited_with(
        "Please provide the expense in the format: !expense <description> <amount> <date>"
    )

@pytest.mark.asyncio
async def test_on_message_expense_with_ollama(monkeypatch):
    # Enable OLLAMA_API
    example_bot.settings.USE_OLLAMA_API = True
    example_bot.settings.USE_OPENAI_API = False

    message = MagicMock()
    message.author.bot = False
    message.author.name = "Bob"
    message.content = "!expense coffee 5 02-06-2024"
    message.channel.send = AsyncMock()

    # Patch ollama_api_call and parse_expense_data
    monkeypatch.setattr(example_bot, "ollama_api_call", lambda prompt: '{"description": "coffee", "amount": "5", "date": "02-06-2024", "payer": "Bob"}')
    monkeypatch.setattr(example_bot, "parse_expense_data", lambda resp: {"description": "coffee", "amount": "5", "date": "02-06-2024", "payer": "Bob"})

    await example_bot.on_message(message)
    message.channel.send.assert_any_await("Parsed expense: {'description': 'coffee', 'amount': '5', 'date': '02-06-2024', 'payer': 'Bob'}")
    message.channel.send.assert_any_await("Expense recorded: coffee, 5, 02-06-2024, Bob")

@pytest.mark.asyncio
async def test_on_message_expense_with_openai(monkeypatch):
    # Enable OpenAI API
    example_bot.settings.USE_OLLAMA_API = False
    example_bot.settings.USE_OPENAI_API = True

    message = MagicMock()
    message.author.bot = False
    message.content = "!expense tea 3 03-06-2024"
    message.channel.send = AsyncMock()

    # Patch openai_api_call
    monkeypatch.setattr(
        example_bot, "openai_api_call",
        lambda prompt: {"choices": [{"message": {"content": '{"description": "tea", "amount": "3", "date": "03-06-2024", "payer": "Eve"}'}}]}
    )

    await example_bot.on_message(message)
    message.channel.send.assert_any_await('Parsed expense: {"description": "tea", "amount": "3", "date": "03-06-2024", "payer": "Eve"}')

@pytest.mark.asyncio
async def test_on_message_bot_author(monkeypatch):
    message = MagicMock()
    message.author.bot = True
    message.content = "$hello"
    message.channel.send = AsyncMock()

    await example_bot.on_message(message)
    message.channel.send.assert_not_awaited()