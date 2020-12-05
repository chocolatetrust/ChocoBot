from .customizations import Cog
from discord.ext import commands
import discord


class Memes(Cog):
    # generic meme, will silently fail if invoked without alias
    async def xmeme(self, ctx: commands.Context):
        filename, text = self.bot.config["memes"][ctx.invoked_with]
        await ctx.send(text, file=discord.File("res/" + filename))

    @Cog.listener()
    async def on_ready(self):
        self.bot.add_command(
            commands.command(aliases=list(self.bot.config["memes"].keys()))(self.xmeme)
        )
