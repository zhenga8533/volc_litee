from cogs.utils.format import send_embed
from discord.ext import commands, tasks
from discord.ext.commands import Context
import discord
import requests


INFERNO_ACTION_UPGRADE = 34.5
INFERNO_ACTION_BASE = 1136.5
MAX_INFERNO = 3.41


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
        name='gabagool',
        description='This command will calculate the profit of using Heavy Fuel.',
    )
    async def gabagool(self, context: Context, tier: int = 5, count: int = 31) -> None:
        """
        This command will calculate the profit of using Heavy Gabagool.
        
        :param context: The application command context.
        :param tier: Level of the minions (1-11). Default is 5.
        :param count: Number of minions. Default is 31.
        """

        # Constants
        ACTION_15 = 1.1 * (INFERNO_ACTION_BASE - (tier * INFERNO_ACTION_UPGRADE)) / MAX_INFERNO / 16
        bz = bazaar.get_data()

        # Calculate the profit
        gabagool = int(count * 86_400 / (2 * ACTION_15) * bz['CRUDE_GABAGOOL'][1])
        price = int(count * (
            bz['HEAVY_GABAGOOL'][0] +
            6 * bz['CRUDE_GABAGOOL_DISTILLATE'][0] +
            2 * bz['INFERNO_FUEL_BLOCK'][0]
        ))
        profit = gabagool - price

        # Create the embed
        embed = discord.Embed(
            title=f'Heavy Gabagool {count}x T{tier}  <:heavy_gabagool:1244700225705345074>',
            description='Please note that these calculations are done with max upgrades!',
            color=discord.Color.green() if profit > 0 else discord.Color.red()
        )

        # Add the fields to the embed
        embed.add_field(
            name='Profit',
            value=f'{gabagool:,}',
            inline=True
        )
        embed.add_field(
            name='Price',
            value=f'{price:,}',
            inline=True
        )
        embed.add_field(
            name='Total',
            value=f'{profit:,}',
            inline=True
        )
        
        await send_embed(context, embed)

    @commands.hybrid_command(
        name='hypergolic',
        description='This command will calculate the profit of crafting Hypergolic Fuel.',
    )
    async def hypergolic(self, context: Context, tier: int = 5, count: int = 31) -> None:
        """
        This command will calculate the profit of using Hypergolic Fuel.
        
        :param context: The application command context.
        :param tier: Level of the minions (1-11). Default is 5.
        :param count: Number of minions. Default is 31.
        """

        # Constants
        bz = bazaar.get_data()
        
        price = (1202 * bz.get('ENCHANTED_COAL', [0, 0])[0] + \
            75.125 * bz.get('ENCHANTED_SULPHUR', [0, 0])[0] + \
            6912 * bz.get('CRUDE_GABAGOOL', [0, 0])[0]) * count
    
    @commands.command(
        name='inferno',
        description='This command will calculate the profit of using Inferno Fuel.',
    )
    async def inferno(self, context: Context, tier: int = 5, count: int = 31) -> None:
        """
        This command will calculate the profit of using Inferno Fuel.

        :param context: The application command context.
        :param tier: Level of the minions (1-11). Default is 5.
        :param count: Number of minions. Default is 31.
        """

        EYEDROP = 1.3
        ACTION_20 = 1.1 * (INFERNO_ACTION_BASE - (tier * INFERNO_ACTION_UPGRADE)) / MAX_INFERNO / 21
        ACTIONS = count * 86400 / (2 * ACTION_20)
        bz = bazaar.get_data()

        # Calculate the drops
        drops = {
            'GABAGOOL': ACTIONS,
            'CHILI': ACTIONS / (156 / EYEDROP) * 1.15,
            'VERTEX': round(ACTIONS / (16364 / EYEDROP) * 2.8, 2),
            'APEX': round(ACTIONS / (1570909 / EYEDROP) * 1.2 * (2 if tier >= 10 else 1), 2),
            'REAPER': round(ACTIONS / (458182 / EYEDROP), 2)
        }

        # Calculate the profit
        profit = {
            'GABAGOOL': int(drops['GABAGOOL'] * bz.get('CRUDE_GABAGOOL', [0, 0])[1]),
            'CHILI': int(drops['CHILI'] * bz.get('CHILI_PEPPER', [0, 0])[1]),
            'VERTEX': int(drops['VERTEX'] * bz.get('INFERNO_VERTEX', [0, 0])[1]),
            'APEX': int(drops['APEX'] * bz.get('INFERNO_APEX', [0, 0])[1]),
            'REAPER': int(drops['REAPER'] * bz.get('REAPER_PEPPER', [0, 0])[1])
        }

        # Calculate the fuel cost
        fuel = count * (
            bz.get('HYPERGOLIC_GABAGOOL', [0, 0])[1] +
            6 * bz.get('CRUDE_GABAGOOL_DISTILLATE', [0, 0])[1] +
            2 * bz.get('INFERNO_FUEL_BLOCK', [0, 0])[1] +
            bz.get('CAPSAICIN_EYEDROPS_NO_CHARGES', [0, 0])[1]
        )

        # Calculate the net profit
        net = sum(profit.values()) - fuel

        # Create the embed
        embed = discord.Embed(
            title=f'Inferno Minions {count}x T{tier}', 
            description='Please note that these calculations are done with max upgrades!',
            color=discord.Color.green() if net > 0 else discord.Color.red()
        )
        embed.add_field(
            name=f"<:crude_gabagool:1244712977152868462> Crude Gabagool", 
            value=f"[{round(drops['GABAGOOL'], 2):,}]: {profit['GABAGOOL']:,}", inline=False
        )
        embed.add_field(
            name=f"<:chili_pepper:1244712282425000028> Chili Pepper", 
            value=f"[{round(drops['CHILI'], 2):,}]: {profit['CHILI']:,}", inline=False
        )
        embed.add_field(
            name=f"<:inferno_vertex:1244712281477222450> Inferno Vertex", 
            value=f"[{round(drops['VERTEX'], 2):,}]: {profit['VERTEX']:,}", inline=False
        )
        embed.add_field(
            name=f"<:inferno_apex:1244712280415797288> Inferno Apex", 
            value=f"[{round(drops['APEX'], 2):,}]: {profit['APEX']:,}", inline=False
        )
        embed.add_field(
            name=f"<:reaper_pepper:1244712279543644160> Reaper Pepper", 
            value=f"[{round(drops['REAPER'], 2):,}]: {profit['REAPER']:,}", inline=False
        )
        embed.add_field(name=f"Fuel Price", value=f"-{int(fuel):,}", inline=True)
        embed.add_field(name=f"Total Profit", value=f"{int(net):,}", inline=True)

        await send_embed(context, embed)

    @commands.hybrid_command(
        name='spaceman',
        description='This command will display the current prices for the spaceman crops.',
    )
    async def spaceman(self, context: Context) -> None:
        """
        This command will display the current prices for the spaceman crops.

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

        await send_embed(context, embed)


async def setup(bot) -> None:
    """
    This function will be called when the cog is loaded.
    
    :param bot: The discord bot.
    """

    await bot.add_cog(Bazaar(bot))
