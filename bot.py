#! /usr/bin/env python3.6

"""
Made by Isabel Lomas for DISCORD HACK WEEK 2019!

For some reason vscode marks "HACK" as another color than the comment color in python's multiline comments.
"""

from datetime import datetime
import discord
from discord.ext import commands
import json
import requests

config = json.load(open('config.json'))

bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or('sdow-'), case_insensitive=True, activity=discord.Game(name='Six Degrees of Wikipedia!'))
bot.remove_command('help')

bot.run(config['token'])