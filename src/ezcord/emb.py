from typing import Union

import discord
from discord import Embed, Color


async def _send_embed(ctx, embed, view):
    if view is None:
        try:
            await ctx.response.send_message(embed=embed, ephemeral=True)
        except discord.InteractionResponded:
            await ctx.followup.send(embed=embed, ephemeral=True)
    else:
        try:
            await ctx.response.send_message(embed=embed, ephemeral=True, view=view)
        except discord.InteractionResponded:
            await ctx.followup.send(embed=embed, ephemeral=True, view=view)


async def error(
        ctx: Union[discord.ApplicationContext, discord.Interaction],
        txt: str,
        view: discord.ui.View = None
):
    """Send an error message.

    Parameters
    ----------
    ctx:
        The application context or the interaction to send the message to.
    txt:
        The text to send.
    view:
        The view to send with the message.

    """
    embed = Embed(
        description=txt,
        color=Color.red()
    )
    await _send_embed(ctx, embed, view)


async def success(
        ctx: Union[discord.ApplicationContext, discord.Interaction],
        txt: str,
        view: discord.ui.View = None
):
    """Send a success message.

    Parameters
    ----------
    ctx:
        The application context or the interaction to send the message to.
    txt:
        The text to send.
    view:
        The view to send with the message.

    """
    embed = Embed(
        description=txt,
        color=Color.green()
    )
    await _send_embed(ctx, embed, view)
