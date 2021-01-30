import discord
from discord.ext import commands

class NotRegistered(commands.CheckFailure):
    def __str__(self):
        return "Not registered User"