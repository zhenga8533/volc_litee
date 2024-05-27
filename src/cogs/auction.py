from discord.ext import commands
from discord.ext.commands import Context
import discord


class Auction(commands.Cog, name="auction"):
    def __init__(self, bot) -> None:
        """
        This is the constructor method for the Auction class.
        
        :param bot: The discord bot.
        """

        self.bot = bot

    @commands.hybrid_command(
        name="gdrag",
        description="This is a testing command that does nothing.",
    )
    async def gdrag(self, context: Context) -> None:
        """
        This is a testing command that does nothing.

        :param context: The application command context.
        """

        pass


async def setup(bot) -> None:
    """
    This function will be called when the cog is loaded.
    
    :param bot: The discord bot.
    """

    await bot.add_cog(Auction(bot))
