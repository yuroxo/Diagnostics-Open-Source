import discord
from discord.ext import commands

class NotRegistered(commands.CheckFailure):
    def __str__(self):
        return "Not registered User"
class AlreadyRegistered(commands.CheckFailure):
    def __str__(self):
        return "Already Registered User"
class JindanNotRegistered(commands.CheckFailure):
    def __str__(self):
        return "Jindan Not Registered"