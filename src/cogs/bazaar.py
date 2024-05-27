from discord.ext import commands, tasks
from discord.ext.commands import Context
import discord
import requests


class BazaarData():
    def __init__(self):
        self.data = {}
        self.fetch_data.start()

    def fetch_data_once(self):
        response = requests.get('https://volcaronitee.pythonanywhere.com/bazaar')
        if response.status_code == 200:
            self.data = response.json().get('items', {})
        else:
            print('Failed to fetch data from the API')

    @tasks.loop(hours=1)
    async def fetch_data(self):
        self.fetch_data_once()

    def get_data(self):
        return self.data

bazaar = BazaarData()


class Bazaar(commands.Cog, name='bazaar'):
    def __init__(self, bot) -> None:
        """
        This is the constructor method for the Bazaar class.
        
        :param bot: The discord bot.
        """

        self.bot = bot

    @commands.hybrid_command(
        name='copper',
        description='This is a testing command that does nothing.',
    )
    async def copper(self, context: Context) -> None:
        """
        This is a testing command that does nothing.

        :param context: The application command context.
        """

        pass

    @commands.hybrid_command(
        name='spaceman',
        description='This is a testing command that does nothing.',
    )
    async def spaceman(self, context: Context) -> None:
        """
        This is a testing command that does nothing.

        :param context: The application command context.
        """

        # Crops that we want to check the prices for.
        CROPS = {
            'TIGHTLY_TIED_HAY_BALE': {
                'count': 893,
                'icon': '<:tightly_tied_hay_bale:1244474560250777704>',
                'name': 'Tightly Tied Hay'
            },
            'ENCHANTED_GOLDEN_CARROT': {
                'count': 16_276,
                'icon': '<:enchanted_golden_carrot:1244478740029902859>',
                'name': 'E. Golden Carrot'
            },
            'ENCHANTED_BAKED_POTATO': {
                'count': 13_021,
                'icon': '<:enchanted_baked_potato:1244476153432117391>',
                'name': 'E. Baked Potato'
            },
            'POLISHED_PUMPKIN': {
                'count': 3_906,
                'icon': '<:polished_pumpkin:1244476096922128424>',
                'name': 'Polished Pumpkin'
            },
            'ENCHANTED_SUGAR_CANE': {
                'count': 9_766,
                'icon': '<:enchanted_sugar_cane:1244476124738621563>',
                'name': 'E. Sugar Cane'
            },
            'ENCHANTED_MELON_BLOCK': {
                'count': 19_531,
                'icon': '<:enchanted_melon_block:1244476063325880440>',
                'name': 'E. Melon Block'
            },
            'ENCHANTED_CACTUS': {
                'count': 13_021,
                'icon': '<:enchanted_cactus:1244476029523857560>',
                'name': 'E. Cactus'
            },
            'ENCHANTED_COOKIE': {
                'count': 16_260,
                'icon': '<:enchanted_cookie:1244476005721313312>',
                'name': 'E. Cookie'
            },
            'ENCHANTED_HUGE_MUSHROOM_1': {
                'count': 19_531,
                'icon': '<:enchanted_red_mushroom_block:1244475963153190976>',
                'name': 'E. Red Mushroom'
            },
            'ENCHANTED_HUGE_MUSHROOM_2': {
                'count': 19_531,
                'icon': '<:enchanted_brown_mushroom_block:1244475916604805131>',
                'name': 'E. Brown Mushroom'
            },
            'MUTANT_NETHER_STALK': {
                'count': 9_766,
                'icon': '<:mutant_nether_wart:1244475872573128736>',
                'name': 'Mutant Nether Wart'
            }
        }
        bz = bazaar.get_data()

        # Create the embed.
        embed = discord.Embed(
            title='Spaceman Prices  <:spaceman:1244480367675707412>',
            description='These are the current prices for the spaceman crops.',
            color=discord.Color.green()
        )

        # Add the fields to the embed.
        for crop_id in CROPS.keys():
            count, icon, name = CROPS[crop_id].values()
            prices = bz.get(crop_id, [0, 0])
            order = int(prices[0] * count)
            instant = int(prices[1] * count)

            embed.add_field(
                name=icon + ' ' + name,
                value=f'Order: {order:,}\nInstant: {instant:,}',
                inline=True
            )
        
        # Add space helmet and footer to the embed.
        embed.add_field(
            name = '<:space_helmet:1244479304813907989> Space Helmet',
            value = 'placeholder',
            inline=True
        )

        embed.set_footer(
            icon_url='https://mc-heads.net/avatar/Volcaronitee/100/nohelm.png',
            text='Made by Volcaronitee!'
        )

        await context.send(embed=embed)


async def setup(bot) -> None:
    """
    This function will be called when the cog is loaded.
    
    :param bot: The discord bot.
    """

    await bot.add_cog(Bazaar(bot))
