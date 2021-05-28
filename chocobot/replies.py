from .customizations import Cog
from discord.ext import commands
import discord
from PIL import Image
import pytesseract


class Society(Cog):
    @Cog.listener()
    async def on_message(self, msg: discord.Message):
        if not msg.channel.id in self.bot.config["allow_replies"]:
            return

        text = f"{msg.clean_content} "
        for embed in msg.embeds:
            text += f"{embed.title} {embed.description} "

        for attachment in [a for a in msg.attachments if a.content_type.startswith("image/")]:
            file = await attachment.to_file()
            text += pytesseract.image_to_string(Image.open(file.fp), timeout=1.0)

        if "society" in text.casefold():
            await msg.channel.send(self.bot.config["society_reply"])
