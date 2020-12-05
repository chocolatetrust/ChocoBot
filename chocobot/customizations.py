from discord.ext import commands


class Cog(commands.Cog):
    "A Cog with the bot reference attached to it."

    def __init__(self, bot):
        self.bot = bot


class Bot(commands.Bot):
    "A Bot with configuration."

    def __init__(self, config, **kwargs):
        self.config = config

        super().__init__(**kwargs)
