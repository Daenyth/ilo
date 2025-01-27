from discord.ext import commands
from discord.commands import slash_command
from discord import Option

from ilo.defines import borgle_map
from ilo.defines import text
import re


def setup(bot):
    bot.add_cog(CogBorgle(bot))


class CogBorgle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="borgle",
        description=text["DESC_BORGLE"],
    )
    async def slash_borgle(self, ctx, text: Option(str, text["DESC_BORGLE_OPTION"])):
        await ctx.respond(do_text(text))

    @slash_command(
        name="deborgle",
        description=text["DESC_DEBORGLE"],
    )
    async def slash_deborgle(
        self, ctx, text: Option(str, text["DESC_DEBORGLE_OPTION"])
    ):
        await ctx.respond(undo(text))


def do_text(text):
    return "\n".join(do_line(line) for line in text.split("\n"))


def do_line(line):
    return " ".join(do_word(word) for word in line.split())


def do_word(word):
    # coda n
    word = re.sub(r"(?<=[aeiou])n(?![aeiou])", "q", word)
    # sorry yupekosi
    word = word.replace("y", "j")
    # word final unstressed i
    word = re.sub(r"(?<!\b[^aeiou])i(?=\b)", "y", word)
    # plorcly borglar
    return "".join(do_letter(letter) for letter in word)


def do_letter(letter):
    if letter not in borgle_map:
        return letter
    else:
        return borgle_map[letter]


def undo(text):
    for key, value in borgle_map.items():
        text = re.sub(f"(?<!@){value}", f"@{key}", text)
    return text.replace("q", "n").replace("y", "i").replace("@", "")
