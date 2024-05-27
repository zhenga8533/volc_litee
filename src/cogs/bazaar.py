from discord.ext import commands, tasks
from discord.ext.commands import Context
import discord
import requests


class BazaarData():
    def __init__(self):
        self.data = {}
        self.fetch_data.start()

    def fetch_data_once(self):
        print("Fetching data from the API")
        response = requests.get("https://volcaronitee.pythonanywhere.com/bazaar")
        if response.status_code == 200:
            self.data = response.json()
        else:
            print("Failed to fetch data from the API")

    @tasks.loop(hours=1)
    async def fetch_data(self):
        self.fetch_data_once()

    def get_data(self):
        return self.data

bazaar = BazaarData()


class Bazaar(commands.Cog, name="bazaar"):
    def __init__(self, bot) -> None:
        """
        This is the constructor method for the Bazaar class.
        
        :param bot: The discord bot.
        """

        self.bot = bot
        self.bazaar_data = BazaarData(bot)

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
