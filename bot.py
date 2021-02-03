import json
import logging
import logging.config
import os
import datetime
from discord.ext import commands
from dotenv import load_dotenv
import config
import koreanbots
import motor.motor_asyncio
import discord
with open("logging.json") as f:
    logging.config.dictConfig(json.load(f))



class JindanBot(commands.AutoShardedBot):

    async def on_ready(self):
        print(f"Logged in as {self.user} at {str(datetime.datetime.now())[:16]}")
        self.logger.info(f"Logged in as {self.user} at {str(datetime.datetime.now())[:16]}")

    async def on_error(self, event, *args, **kwargs):
        self.logger.exception("")

    def __init__(self, logger):
        print("Starting Up Bot... Wait until next message")
        super().__init__(commands.when_mentioned_or(*config.command_prefixes), intents=discord.Intents.default(), shard_count=8)
        if len(config.mongodb_username) > 1:
            self.dbclient = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{config.mongodb_username}:{config.mongodb_password}@{config.mongodb_host}:{config.mongodb_port}")
        else:
            self.dbclient = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{config.mongodb_host}:{config.mongodb_port}")
        self.db = self.dbclient.JindanBot
        self.KBClient = koreanbots.Client(self, config.koreanbots_token)
        self.logger = logger
        self.logger.info(f"Successfully Connected to mongodb://{config.mongodb_username}:*******@{config.mongodb_host}:{config.mongodb_port}")
        for ext in config.extension_list:
            self.load_extension(ext)


bot = JindanBot(logger=logging.getLogger("bot"))


bot.run(config.bot_token)