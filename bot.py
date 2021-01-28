import discord
import asyncio
import os
import json
import time
#is_looping=False
msg_list=['!ㅊㅊ','!출첵','!출석','!출석체크']
token=os.environ['token']
check_list={}
'''
async def twitch_totu():
    channel = client.get_channel(760895834698022915)
    while True:
        if will_stop==True:
            break
        await channel.send('방송중')
        await asyncio.sleep(15)
'''
class bot(discord.Client):

    async def on_ready(self):
        print('ready!')

    async def on_message(self, message):
        if message.content in msg_list:
            if str(message.guild) == "토하'-'":
                if str(message.channel.id) != '804391461105041518':
                    refuse=await message.channel.send('출석체크는 출석체크방에서 하셔야 합니다.')
                    await asyncio.sleep(5)
                    await refuse.delete()
                    return
            if message.author.name not in check_list.keys():
                check_list[message.author.name]={'current_time':'','times':0}
            if time.strftime('%d') != check_list[message.author.name]['current_time']:
                check_list[message.author.name]['current_time']=time.strftime('%d')
                check_list[message.author.name]['times']+=1
                await message.channel.send(message.author.nick+'님')
                will_send=time.strftime('%m월 %d일 %H시 %M분 %S초에 출석 하셨습니다.')
                will_send=will_send.replace('00','㏇').replace('0','').replace('㏇','0')
                await message.channel.send(will_send)
            else:
                await message.channel.send('이미 출석 했습니다.')
        if message.content.startswith('air '):
            if message.author.name == 'night_life_':
                try:
                    #await message.channel.send('@everyone')
                    a=await message.channel.send(eval(message.content.replace('air ','')))
                    await asyncio.sleep(10)
                    await a.delete()
                except Exception as e:
                    await message.channel.send(e)
            else:
                await message.channel.send('권한이 없습니다')
client = bot()
client.run(token)