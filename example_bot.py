# # This example requires the 'message_content' intent.

import discord
import settings
from utils import ai_api_call, parse_expense_data, get_gsheet_client, record_expense

# import logging

# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)

handler = None
token = settings.DISCORD_TOKEN


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):

    async def send_recod_expense_response():
        if record_expense(date, desc, amount, payer):
            await message.channel.send(f"Expense recorded: {desc}, {amount}, {date}, {payer}")
        else:
            await message.channel.send(f"Failed to record the expense.")

    # Check if the message is from a bot
    if message.author.bot:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    elif message.content.startswith('!expense') and not (settings.USE_OPENAI_API or settings.USE_OLLAMA_API):
        parts = message.content.split()
        if len(parts) >= 4:
            desc, amount, date = parts[1], parts[2], parts[3]
            payer = message.author.name
            await send_recod_expense_response()
        else:
            await message.channel.send("Please provide the expense in the format: !expense <description> <amount> <date>")
        
        prompt = f"Extract '{user_input}' into  description, amount, date, and payer. convert date to dd-mm-yyyy. Return only JSON."
        print("Expense command received")
        """ 
        AI API call for expense extraction
        Expected AI response format:
        {
            "description": "<expense description>",
            "amount": "<expense amount>",
            "date": "<dd-mm-yyyy>",
            "payer": "<payer name>"
        }
         """
        user_input = message.content[len('!expense '):]
        prompt = f"Extract '{user_input}' into  description, amount, date, and payer. convert date to dd-mm-yyyy. Return only JSON."
    
    #TODO: add a command to report the expenses
    elif message.content.startswith('!report'):
        await message.channel.send("The report feature is under development and will be available soon!")

    #TODO: add a command to analyze the expenses
    elif message.content.startswith('!analysis'):
        await message.channel.send("The analysis feature is under development and will be available soon!")


    # AI API call
    response = ai_api_call(prompt)
    if response is None:
        await message.channel.send("Sorry, I couldn't process your request.")
        return
    
    #Note that response should be json covertable
    try:
        parsed_data = parse_expense_data(response)
        await message.channel.send(f"Parsed expense: {parsed_data}")
    except (ValueError, TypeError) as e:
        await message.channel.send(f"Failed to parse the AI response. Error: {e}")
        return
    
    if parsed_data is None:
        await message.channel.send("Sorry, I couldn't parse the data.")
        return

    required_keys = ('description', 'amount', 'date')
    if not all(key in parsed_data for key in required_keys):
        await message.channel.send("The AI response is missing some required fields. Please try again.")
        return
    

    desc, amount, date = parsed_data['description'], parsed_data['amount'], parsed_data['date']
    payer = parsed_data.get("payer", message.author.name)

    if record_expense(date, desc, amount, payer):
        await message.channel.send(f"Expense recorded: {desc}, {amount}, {date}, {payer}")
    else:
        await message.channel.send(f"Failed to record the expense.")

client.run(token, log_handler=handler)
