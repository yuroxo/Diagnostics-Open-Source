import discord
from discord.ext import commands
import motor.motor_asyncio
from . import exceptions
class check:
    def __init__(self, db: motor.motor_asyncio.AsyncIOMotorClient):
        self.db = db
    
    async def registered(self, ctx):
        db_user = await self.db.users.find_one({"discordId": ctx.author.id})
        if db_user:
            return True
        raise exceptions.NotRegistered

    async def jindanRegistered(self, ctx):
        db_user = await self.db.users.find_one({"discordId": ctx.author.id})
        if not db_user:
            raise exceptions.NotRegistered
        if not db_user.get("token", None):
            raise exceptions.JindanNotRegistered
        return True