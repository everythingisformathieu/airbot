import discord
import asyncio
import os

token=os.environ['token']

totu_id=''

class bot(discord.Client):

    async def on_ready(self):
        print('ready!')

    async def on_message(self, message):
        if str(message.author) == '토투#0278':
            totu_id = message.author.id
            print(totu_id)

client = bot()
client.run(token)
