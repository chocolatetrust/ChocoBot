import discord
from discord.ext import commands
import json

from .customizations import Bot
from .commands import Commands
from .memes import Memes

config = {}
with open("settings.json", "r") as f:
    config = json.load(f)

intents = discord.Intents.default()
intents.members = True
bot = Bot(config, command_prefix=",", intents=intents, help_command=None)

for Cog in (Commands, Memes):
    bot.add_cog(Cog(bot))


@bot.command()
async def memes(ctx: commands.Context):
    embed = (
        discord.Embed(color=0xAF2E1A)
        .set_author(name="ChocoBot", icon_url=bot.user.avatar_url)
        .set_thumbnail(url=bot.user.avatar_url)
    )

    groups = {
        "Memes": "\n".join([f",{alias}" for alias in bot.config["memes"].keys()]),
        "Renames": "\n".join([f",{alias}" for alias in bot.config["renames"].keys()]),
        "Commands": "",
    }

    for command in bot.get_cog("Commands").walk_commands():
        if isinstance(command, commands.Group):
            continue

        groups["Commands"] += f",{command.qualified_name}\n"

    for key, value in groups.items():
        embed.add_field(name=key, value=value)

    await ctx.send(embed=embed)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")


def main():
    bot.run(config["token"])


if __name__ == "__main__":
    main()