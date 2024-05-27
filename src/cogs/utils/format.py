from discord.ext.commands import Context
import discord


async def send_embed(context: Context, embed: discord.Embed) -> None:
    """
    Send an embed to the context.
    
    :param context: The application command context.
    :param embed: The embed to send.
    """

    embed.set_footer(
        icon_url='https://mc-heads.net/avatar/Volcaronitee/100/nohelm.png',
        text='Made by Volcaronitee!'
    )
    await context.send(embed=embed)
