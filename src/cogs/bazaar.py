from discord.ext import commands
from discord.ext.commands import Context
import discord


class Bazaar(commands.Cog, name="bazaar"):
    def __init__(self, bot) -> None:
        """
        This is the constructor method for the Bazaar class.
        
        :param bot: The discord bot.
        """

        self.bot = bot

    @commands.hybrid_command(
        name="copper",
        description="This is a testing command that does nothing.",
    )
    async def copper(self, context: Context) -> None:
        """
        This is a testing command that does nothing.

        :param context: The application command context.
        """

        pass

    @commands.hybrid_command(
        name="spaceman",
        description="This is a testing command that does nothing.",
    )
    async def spaceman(self, context: Context) -> None:
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

    await bot.add_cog(Bazaar(bot))
