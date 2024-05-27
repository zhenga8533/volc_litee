from cogs.party_util.coinflip import Coin
from cogs.party_util.rps import RockPaperScissorsView
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands, Color, Embed
import discord
import random
import requests


# Tags for the waifu.pics API
SFW_TAGS = [
    'waifu', 'neko', 'shinobu', 'megumin', 'cuddle', 'cry', 'hug', 'kiss', 'lick', 'pat', 'smug', 'bonk', 'blush', 
    'smile', 'wave', 'highfive', 'handhold', 'bite', 'slap', 'kick', 'happy', 'wink', 'poke', 'dance', 'cringe'
]
NSFW_TAGS = [
    'waifu', 'neko', 'trap', 'blowjob'
]
WAIFU_TYPES = ['sfw', 'nsfw']

class Party(commands.Cog, name='party'):
    def __init__(self, bot) -> None:
        """
        Initializes the Party cog.

        :param bot: The instance of the bot that the cog is being added to.
        """

        self.bot = bot
    
    # 8ball Command
    @commands.hybrid_command(
        name="8ball",
        description="Ask any question to the bot.",
    )
    @app_commands.describe(question="The question you want to ask.")
    async def eight_ball(self, context: Context, *, question: str) -> None:
        """
        Ask any question to the bot.

        :param context: The hybrid command context.
        :param question: The question that should be asked by the user.
        """

        answers = [
            "It is certain.",
            "It is decidedly so.",
            "You may rely on it.",
            "Without a doubt.",
            "Yes - definitely.",
            "As I see, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again later.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful.",
        ]
        embed = discord.Embed(
            title="**My Answer:**",
            description=f"{random.choice(answers)}",
            color=0xBEBEFE,
        )
        embed.set_footer(text=f"The question was: {question}")
        await context.send(embed=embed)
    
    # Coinflip Command
    @commands.hybrid_command(
        name="coinflip", description="Make a coin flip, but give your bet before."
    )
    async def coinflip(self, context: Context) -> None:
        """
        Make a coin flip, but give your bet before.

        :param context: The hybrid command context.
        """
        buttons = Coin()
        embed = discord.Embed(description="What is your bet?", color=0xBEBEFE)
        message = await context.send(embed=embed, view=buttons)
        await buttons.wait()  # We wait for the user to click a button.
        result = random.choice(["heads", "tails"])
        if buttons.value == result:
            embed = discord.Embed(
                description=f"Correct! You guessed `{buttons.value}` and I flipped the coin to `{result}`.",
                color=0xBEBEFE,
            )
        else:
            embed = discord.Embed(
                description=f"Woops! You guessed `{buttons.value}` and I flipped the coin to `{result}`, better luck next time!",
                color=0xE02B2B,
            )
        await message.edit(embed=embed, view=None, content=None)
    
    # Rock Paper Scissors Command
    @commands.hybrid_command(
        name="rps", description="Play the rock paper scissors game against the bot."
    )
    async def rock_paper_scissors(self, context: Context) -> None:
        """
        Play the rock paper scissors game against the bot.

        :param context: The hybrid command context.
        """
        view = RockPaperScissorsView()
        await context.send("Please make your choice", view=view)

    # Waifu Command
    @commands.hybrid_command(
        name='w',
        description='Get a random image from the waifu.pics API.',
    )
    @app_commands.describe(tag='Select a tag')
    @app_commands.choices(tag=[
        app_commands.Choice(name=tag.capitalize(), value=tag) for tag in SFW_TAGS
    ], sfw=[
        app_commands.Choice(name=t.upper(), value=t) for t in WAIFU_TYPES
    ])
    async def w(self, context: Context, tag: str = 'waifu', sfw: str = 'sfw') -> None:
        """
        Get a random image from the waifu.pics API.

        :param context: The application command context.
        :param tag: The tag selected by the user.
        """

        # Check if tag is valid
        if tag not in SFW_TAGS or sfw not in WAIFU_TYPES or (sfw == 'nsfw' and tag not in NSFW_TAGS):
            embed = Embed(
                title="Invalid Tag",
                description="The selected tag is not valid.",
                color=Color.red()
            )
            await context.send(embed=embed)
            return

        # Check if the channel is NSFW
        if sfw == 'nsfw' and not context.channel.is_nsfw():
                embed = Embed(
                    title="NSFW Content",
                    description="Cannot send NSFW content in a non-NSFW channel.",
                    color=Color.red()
                )
                await context.send(embed=embed)
                return
        
        # Fetch image from API
        response = requests.get(f'https://api.waifu.pics/{sfw}/{tag}')
        if response.status_code == 200:
            data = response.json()
            image_url = data['url']
            embed = Embed(
                title=tag.capitalize(),
                description=image_url,
                color=Color.green()
            )
            embed.set_image(url=image_url)
        else:
            embed = Embed(
                title="API Error",
                description="Failed to fetch image from API.",
                color=Color.red()
            )

        # Send the embed
        await context.send(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(Party(bot))
