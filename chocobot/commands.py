from .customizations import Cog
from discord.ext import commands
from typing import Optional, Union
import discord
import random
import re


class Commands(Cog):
    @commands.command()
    async def sponge(self, ctx: commands.Context, *, phrase: Optional[str]):
        if not phrase:
            phrase = "You forgot a message to mock"

        phrase = [random.choice((char.upper(), char.lower())) for char in phrase]
        await ctx.send("".join(phrase))

    @commands.command()
    async def katcase(self, ctx: commands.Context, *, phrase: Optional[str]):
        if not phrase:
            phrase = "You forgot a message to katcase"

        phrase = phrase.upper()
        await ctx.send(phrase)

    @commands.command()
    async def ban(self, ctx: commands.Context, *, what: Optional[str]):
        if not what:
            await ctx.send("ban what now?")
            return

        if re.match(r"<@!?\d+>", what):
            await ctx.send(f"{what} get fucked lmmmmao")
        else:
            await ctx.send(f"{what} is now illegal")

    # generic rename command, will silently fail if invoked without an alias
    async def xname(self, ctx: commands.Context, *, nick: str):
        user_id, genitive = tuple(self.bot.config["renames"][ctx.invoked_with])
        if not nick or len(nick) > 32:
            await ctx.reply("Name must be ≥2 and ≤32 characters")
            return

        member = ctx.guild.get_member(user_id)
        old_nick = member.nick
        await ctx.guild.get_member(user_id).edit(nick=nick)
        if ctx.invoked_with == "hagname":
            await ctx.send(
                f"{genitive} nickname updated from **{old_nick}** to **{nick}**"
                + ("." * random.randrange(3, 17))
            )
        else:
            await ctx.send(
                f"{genitive} nickname updated from **{old_nick}** to **{nick}**"
            )

    @Cog.listener()
    async def on_ready(self):
        self.bot.add_command(
            commands.command(aliases=list(self.bot.config["renames"].keys()))(
                self.xname
            )
        )

    STORIES = {}

    @Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.channel in self.STORIES and not msg.content.startswith(",story"):
            try:
                content = self.STORIES[msg.channel].content
                if content == "*Once upon a time…*":
                    content = ""

                await msg.delete()
                await self.STORIES[msg.channel].edit(
                    content=content + " " + msg.clean_content
                )
            except discord.HTTPException:
                await msg.add_reaction("❌")

    @commands.group()
    async def story(self, ctx):
        pass

    @commands.command(parent=story)
    @commands.bot_has_permissions(manage_messages=True)
    async def start(self, ctx: commands.Context):

        self.STORIES[ctx.channel] = await ctx.send("*Once upon a time…*")

    @commands.command(parent=story)
    @commands.bot_has_permissions(manage_messages=True)
    async def stop(self, ctx):
        if ctx.channel in self.STORIES:
            message = self.STORIES.pop(ctx.channel)
            await message.pin()
            async for msg in ctx.history(limit=5):
                if msg.author == ctx.bot.user and msg.is_system():
                    await msg.delete()
                    break