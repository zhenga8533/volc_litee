from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Message
from discord.ext import commands
from commands import *
from responses import get_response


# Initialize the client
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Set up the bot
intents: Intents = Intents.default()
intents.message_content = True
bot: commands.Bot = commands.Bot(command_prefix='/', intents=intents)

async def send_response(message: Message, user_message: str) -> None:
    """
    Send a response to the user based on their message.
    
    :param message: The message object that triggered the bot.
    :param user_message: The message content from the user.
    """
    
    try:
        response: str = get_response(user_message)
        await message.channel.send(response)
    except Exception as e:
        await message.channel.send(f"An error occurred: {e}")

@bot.hybrid_command()
async def sync(ctx: commands.Context) -> None:
    """
    Sync the commands with the Discord API.
    
    :param ctx: The context of the command.
    """
    
    try:
        synced = await bot.tree.sync()
        await ctx.send(f'Synced {len(synced)} commands')
    except Exception as e:
        await ctx.send(f'An error occurred: {e}')

@bot.hybrid_command()
async def ping(ctx: commands.Context) -> None:
    """
    Respond to a ping command.
    
    :param ctx: The context of the command.
    """
    
    res: str = ping_command()
    await ctx.send(res)

@bot.hybrid_command()
async def w(ctx: commands.Context) -> None:
    """
    Respond to a weather command.
    
    :param ctx: The context of the command.
    """
    
    res: str = w_command()
    await ctx.send(res)

@bot.event
async def on_message(message: Message) -> None:
    """
    Handle messages sent by users.
    """

    if message.author == bot.user or not message.content.startswith('?'):
        return

    user_message = message.content
    await send_response(message, user_message)

    await bot.process_commands(message)

@bot.event
async def on_ready() -> None:
    """
    Print a message when the bot is ready.
    """
    
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(f'An error occurred: {e}')

def main() -> None:
    """
    Run the bot.
    """
    
    bot.run(token=TOKEN)

if __name__ == '__main__':
    main()
