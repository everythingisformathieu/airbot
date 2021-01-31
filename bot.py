import discord
import asyncio
import os
import json
import time
#is_looping=False
msg_list=['!ㅊㅊ','!출첵','!출석','!출석체크']
attendance_list=['!ㅊㅊ','!출첵','!출석','!출석체크']
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

        async def on_member_join(self, member):
        await member.guild.get_channel(792733880356044813).send('안녕하세요')
        print(dir(member))

'''
class bot(discord.Client):

    async def on_ready(self):
        print('ready!')
        await client.change_presence(status=discord.Status.online, activity=discord.Game('에어봇'))

    async def on_message(self, message):
        if message.content in msg_list:
            if str(message.guild) == "토하'-'":
                if str(message.channel.id) != '804391461105041518':
                    await message.channel.purge(limit=1)
                    refuse=await message.channel.send('출석체크방에서 해주세요.')
                    await asyncio.sleep(5)
                    await refuse.delete()
                    return
        if message.content in attendance_list:
            daytime=int(time.strftime('%d'))
            hourtime=int(time.strftime('%H'))
            print(hourtime)
            if hourtime >= 15:
                daytime+=1
            hourtime-=9
            print(hourtime)
            if hourtime<0:
                hourtime = 24+hourtime
            print(hourtime)
            if message.author.name not in check_list.keys():
                check_list[message.author.name]={'current_time':'','times':0}
            if daytime != check_list[message.author.name]['current_time']:
                check_list[message.author.name]['current_time']=daytime
                check_list[message.author.name]['times']+=1
                will_send=time.strftime('%m월 ')+str(daytime)+'일 '+str(hourtime)+'시 '+time.strftime('%M분 %S초에 출석 하셨습니다.')
                will_send=will_send.replace('00','㏇').replace('0','').replace('㏇','0')
                embed = discord.Embed(title=message.author.nick+'님',description=will_send, color=0x00aaaa)
                embed.set_footer(text=str(check_list[message.author.name]['times'])+'번 출석하셨습니다')
                await message.channel.send(embed=embed)
            else:
                await message.channel.send('이미 출석 했습니다.')

        if message.content.startswith('air '):
            if message.author.name == 'night_life_':
                try:
                    #await message.channel.send('@everyone')
                    a=await message.channel.send(eval(message.content.replace('air ','')))
                    await asyncio.sleep(10)
                    #await a.delete()
                except Exception as e:
                    await message.channel.send(e)
            else:
                await message.channel.send('권한이 없습니다')
client = bot()
client.run(token)
