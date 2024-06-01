from cogs.utils.format import send_embed
from discord.ext import commands, tasks
from discord.ext.commands import Context
import discord
import requests


INFERNO_ACTION_UPGRADE = 34.5
INFERNO_ACTION_BASE = 1136.5
MAX_INFERNO = 3.41


class Bazaar():
    def __init__(self):
        self.data = {}
        self.fetch_data.start()

    @tasks.loop(hours=1)
    async def fetch_data(self):
        response = requests.get('https://volcaronitee.pythonanywhere.com/bazaar')
        if response.status_code == 200:
            self.data = response.json().get('items', {})
        else:
            print('Failed to fetch data from the API')

    def get_data(self):
        return self.data


class Auction():
    def __init__(self):
        self.data = {}
        self.fetch_data.start()

    @tasks.loop(hours=1)
    async def fetch_data(self):
        response = requests.get('https://volcaronitee.pythonanywhere.com/auction')
        if response.status_code == 200:
            self.data = response.json().get('items', {})
        else:
            print('Failed to fetch data from the API')

    def get_data(self):
        return self.data


class Economy(commands.Cog, name='economy'):
    def __init__(self, bot) -> None:
        """
        This is the constructor method for the Bazaar class.
        
        :param bot: The discord bot.
        """

        self.bot = bot
        self.bazaar = Bazaar()
        self.auction = Auction()
    
    @commands.hybrid_command(
        name='farming',
        description='This command will calculate the profit of farming crops.',
    )
    async def farming(self, context: Context, fortune: float = 0.0) -> None:
        """
        This command will calculate the profit of farming crops.
        
        :param context: The application command context.
        :param fortune: The fortune level of the crops.
        """

        bz = self.bazaar.get_data()

        # Crops that we want to check the prices for. Source: https://hypixel-skyblock.fandom.com/wiki/Farming_Fortune
        CROPS = {
            'TIGHTLY_TIED_HAY_BALE': {
                'craft': 186_624,
                'drops': 1,
                'fortune': 1_997,
                'name': '<:sb_wheat:1245892472471552072> Wheat',
                'npc': 6
            },
            'ENCHANTED_CARROT': {
                'craft': 160,
                'drops': 3.5,
                'fortune': 2_009,
                'name': '<:sb_carrot:1245892494907019367> Carrot',
                'npc': 3
            },
            'ENCHANTED_BAKED_POTATO': {
                'craft': 25_600,
                'drops': 3.5,
                'fortune': 1_997,
                'name': '<:sb_potato:1245892937020080138> Potato',
                'npc': 3
            },
            'POLISHED_PUMPKIN': {
                'craft': 25_600,
                'drops': 1,
                'fortune': 1_792,
                'name': '<:sb_pumpkin:1245893176154259528> Pumpkin',
                'npc': 10
            },
            'ENCHANTED_MELON_BLOCK': {
                'craft': 25_600,
                'drops': 5,
                'fortune': 1_780,
                'name': '<:sb_melon:1245893198685929472> Melon',
                'npc': 2
            },
            'ENCHANTED_HUGE_MUSHROOM_1': {
                'craft': 5_120,
                'drops': 1,
                'fortune': 1_869,
                'name': '<:sb_red_mushroom:1245893226767061022> Mushroom',
                'npc': 10
            },
            'ENCHANTED_HUGE_MUSHROOM_2': {
                'craft': 5_120,
                'drops': 1,
                'fortune': 1_869,
                'name': '<:sb_brown_mushroom:1245893247818272831> Mushroom',
                'npc': 10
            },
            'ENCHANTED_SUGAR_CANE': {
                'craft': 25_600,
                'drops': 2,
                'fortune': 1_997,
                'name': '<:sb_sugar_cane:1245893274527334431> Sugar Cane',
                'npc': 4
            },
            'MUTANT_NETHER_STALK': {
                'craft': 25_600,
                'drops': 3,
                'fortune': 1_997,
                'name': '<:sb_nether_wart:1245893288507215972> Nether Wart',
                'npc': 4
            },
            'ENCHANTED_COCOA': {
                'craft': 160,
                'drops': 3,
                'fortune': 1_800,
                'name': '<:sb_cocoa_beans:1245893316294213652> Cocoa Bean',
                'npc': 3
            },
            'ENCHANTED_CACTUS': {
                'craft': 25_600,
                'drops': 2,
                'fortune': 1_684,
                'name': '<:sb_cactus:1245893338746589305> Cactus',
                'npc': 3
            }
        }
        BPH = 72_000

        # Create the embed.
        embed = discord.Embed(
            title='Farming Profits',
            description='These are the current prices for the farming crops.',
            color=discord.Color.green()
        )

        # Track best crop
        best_npc = {
            'value': 0,
            'name': ''
        }
        best_order = {
            'value': 0,
            'name': ''
        }
        best_insta = {
            'value': 0,
            'name': ''
        }

        # Add the fields to the embed.
        for crop_id in CROPS.keys():
            craft, drops, fortune, name, npc = CROPS[crop_id].values()

            # Calculate the profits
            insta, order = bz.get(crop_id, [0, 0])
            rate = BPH * drops * fortune / 100
            npc_calc = int(npc * rate)
            order_calc = int(order / craft * rate)
            insta_calc = int(insta / craft * rate)

            # Calc seeds if wheat
            if crop_id == 'TIGHTLY_TIED_HAY_BALE':
                seed_isnta, seed_order = bz.get('BOX_OF_SEEDS', [0, 0])
                seed_rate = BPH * 1.5 * fortune / 100
                npc_calc += int(3 * seed_rate)
                order_calc += int(seed_order / 25_600 * seed_rate)
                insta_calc += int(seed_isnta / 25_600 * seed_rate)

            # Add the field to the embed
            value_msg = f'NPC: {npc_calc:,}\nOrder: {order_calc:,}\nInsta: {insta_calc:,}'
            embed.add_field(
                name=name,
                value=value_msg,
                inline=True
            )
            
            # Track best crop
            if npc_calc > best_npc['value']:
                best_npc['value'] = npc_calc
                best_npc['name'] = name
            if order_calc > best_order['value']:
                best_order['value'] = order_calc
                best_order['name'] = name
            if insta_calc > best_insta['value']:
                best_insta['value'] = insta_calc
                best_insta['name'] = name
        
        # Add best crop and send the embed
        embed.add_field(
            name=f'Best Crops',
            value=f'NPC: {best_npc["name"]}\nOrder: {best_order["name"]}\nInsta: {best_insta["name"]}',
            inline=True
        )
        
        await send_embed(context, embed)
    
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
        bz = self.bazaar.get_data()

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

        bz = self.bazaar.get_data()

        def calc_hypergolic(insta: int) -> int:
            """
            Calculate the cost of crafting Hypergolic Fuel.
            
            :param insta: The price type (0 = sell offer, 1 = insta buy).
            :return: The cost of crafting Hypergolic Fuel.
            """

            return int(1202 * bz.get('ENCHANTED_COAL', [0, 0])[insta] + \
                75.125 * bz.get('ENCHANTED_SULPHUR', [0, 0])[insta] + \
                6912 * bz.get('CRUDE_GABAGOOL', [0, 0])[insta]) * count

        # Calculate the profit
        hypergolic = bz.get('HYPERGOLIC_GABAGOOL', [0, 0])
        order_hypergolic = calc_hypergolic(0)
        insta_hypergolic = calc_hypergolic(1)
        p1 = int(hypergolic[0] - order_hypergolic)
        p2 = int(hypergolic[0] - insta_hypergolic)
        p3 = int(hypergolic[1] - order_hypergolic)
        p4 = int(hypergolic[1] - insta_hypergolic)

        # Create the embed
        embed = discord.Embed(title="Hypergolic Craft Profits:", color=0x00ff00)
        embed.add_field(name="<:hypergolic_gabagool:1245169162700066826>  Hypergolic Gabagool:", value="", inline=False)
        embed.add_field(name="Insta Sell:", value=f"{int(hypergolic[0]):,}", inline=True)
        embed.add_field(name="Sell Offer:", value=f"{int(hypergolic[1]):,}", inline=True)
        embed.add_field(name="<:crude_gabagool:1244712977152868462>  Material Cost:", value="", inline=False)
        embed.add_field(name="Buy Order:", value=f"{order_hypergolic:,}", inline=True)
        embed.add_field(name="Insta Buy:", value=f"{insta_hypergolic:,}", inline=True)
        embed.add_field(name="<:inferno_fuel:1244712278025044010>  Total Profit:", value="", inline=False)
        embed.add_field(name="Insta Sell + Buy Order:", value=f"{p1:,}", inline=False)
        embed.add_field(name="Insta Sell + Insta Buy:", value=f"{p2:,}", inline=False)
        embed.add_field(name="Sell Offer + Buy Order:", value=f"{p3:,}", inline=False)
        embed.add_field(name="Sell Offer + Insta Buy:", value=f"{p4:,}", inline=False)

        await context.send(embed=embed)
    
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
        bz = self.bazaar.get_data()

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
        bz = self.bazaar.get_data()

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
            insta = int(prices[1] * count)

            embed.add_field(
                name=icon + ' ' + name,
                value=f'Order: {order:,}\nInsta: {insta:,}',
                inline=True
            )
        
        # Add space helmet and footer to the embed.
        space_helmet = self.auction.get_data().get('DCTR_SPACE_HELM', {})
        embed.add_field(
            name = '<:space_helmet:1244479304813907989> Space Helmet',
            value = f"BIN: {space_helmet.get('lbin', 0):,}",
            inline=True
        )

        await send_embed(context, embed)


async def setup(bot) -> None:
    """
    This function will be called when the cog is loaded.
    
    :param bot: The discord bot.
    """

    await bot.add_cog(Economy(bot))
