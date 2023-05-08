"""Utility functions for the ready event."""

import discord

from ..enums import ReadyEvent
from ..logs import log


class Style:
    TL = "╭"  # top left
    TR = "╮"  # top right
    BL = "╰"  # bottom left
    BR = "╯"  # bottom right
    H = "─"  # horizontal
    V = "│"  # vertical
    M = "┼"  # middle
    L = "├"  # left
    R = "┤"  # right
    T = "┬"  # top
    B = "┴"  # bottom


class Bold(Style):
    TL, TR, BL, BR, H, V, M, L, R, T, B = "╔", "╗", "╚", "╝", "═", "║", "╬", "╠", "╣", "╦", "╩"


def print_ready(bot: discord.Bot, style: ReadyEvent):
    cmds = [
        cmd for cmd in bot.walk_application_commands() if type(cmd) != discord.SlashCommandGroup
    ]

    infos = {
        "User": f"{bot.user}",
        "ID": f"{bot.user.id}",
        "Pycord": discord.__version__,
        "Commands": f"{len(cmds):,}",
        "Guilds": f"{len(bot.guilds):,}",
        "Latency": f"{round(bot.latency * 1000):,}ms",
    }

    txt = f"Bot is online!"
    colon_infos = {key + ":": value for key, value in infos.items()}

    style_cls = Style()
    if "bold" in style.name:
        style_cls = Bold()

    if style == ReadyEvent.box or style == ReadyEvent.box_bold:
        txt += box(colon_infos, style_cls)
        log.info(txt)
    elif style == ReadyEvent.logs:
        log.info(txt)
        logs(colon_infos)
    else:
        if style == ReadyEvent.table or style == ReadyEvent.table_bold:
            info_list = [list(infos.keys()), list(infos.values())]
        else:
            info_list = [list(item) for item in infos.items()]
        txt += "\n" + tables(info_list, style_cls)
        log.info(txt)


def box(infos: dict[str, str], s: Style = Style()):
    longest = max([str(i) for i in infos.values()], key=len)
    formatter = f"<{len(longest)}"
    longest_key = max([len(i) for i in infos.keys()]) + 1

    txt = f"\n{s.TL}{(len(longest) + 2 + longest_key) * s.H}{s.TR}\n"
    for key, info in infos.items():
        key = f"{key:<{longest_key}}"
        txt += f"{s.V} {key}{info:{formatter}} {s.V}\n"
    txt += f"{s.BL}{(len(longest) + 2 + longest_key) * s.H}{s.BR}"
    return txt


def logs(infos: dict[str, str]):
    for key, info in infos.items():
        log.info(f"{key} **{info}**")


def tables(rows: list[list[str]], s: Style = Style()):
    length = [max([len(value) for value in column]) for column in zip(*rows)]
    table = ""
    for index, row in enumerate(rows):
        table += s.V

        middle_row = ""
        for max_length, content in zip(length, row):
            space_content = f" {content} "
            table += space_content + " " * (max_length - len(content)) + s.V
            middle_row += s.H * (max_length - len(content) + len(space_content)) + s.M

        middle_row = middle_row[:-1]
        if index == 0:
            top_row = middle_row.replace(s.M, s.T)
            table = s.TL + top_row + s.TR + "\n" + table

        if index != len(rows) - 1:
            table += "\n" + s.V + middle_row + s.V + "\n"
        else:
            bottom_row = middle_row.replace(s.M, s.B)
            table += "\n" + s.BL + bottom_row + s.BR

    return table