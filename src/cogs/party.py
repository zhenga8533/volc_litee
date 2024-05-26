from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands, Color, Embed
import requests

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
        self.bot = bot

    @commands.hybrid_command(
        name='w',
        description='This is a testing command that does nothing.',
    )
    @app_commands.describe(tag='Select a tag')
    @app_commands.choices(tag=[
        app_commands.Choice(name=tag.capitalize(), value=tag) for tag in SFW_TAGS
    ], sfw=[
        app_commands.Choice(name=t.upper(), value=t) for t in WAIFU_TYPES
    ])
    async def w(self, context: Context, tag: str = 'waifu', sfw: str = 'sfw') -> None:
        """
        This is a testing command that does nothing.

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
