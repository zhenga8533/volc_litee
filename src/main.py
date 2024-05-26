from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response


load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Set up the bot
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

async def send_response(message: Message, user_message: str) -> None:
    """
    Send a response to the user based on their message.
    
    :param message: The message object that triggered the bot.
    :param user_message: The message content from the user.
    """

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]
    
    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        await message.channel.send(f"An error occurred: {e}")

@client.event
async def on_ready() -> None:
    """
    Print a message when the bot is ready.
    """
    
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message: Message) -> None:
    """
    Respond to messages sent in the server.
    
    :param message: The message object that triggered the bot.
    """
    
    if message.author == client.user:
        return

    await send_response(message, message.content)

def main() -> None:
    """
    Run the bot.
    """
    
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
