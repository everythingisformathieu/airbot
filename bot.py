import discord
import asyncio
import os
import json
import time
import math
#is_looping=False
msg_list=['!ㅊㅊ','!출첵','!출석','!출석체크']
attendance_list=['!ㅊㅊ','!출첵','!출석','!출석체크']
token=os.environ['token']
ttt_game_pad={}
board_num=['\u2460','\u2461','\u2462','\u2463','\u2464','\u2465','\u2466','\u2467','\u2468','\u2469','\u246a','\u246b','\u246c','\u246d','\u246e','\u246f','\u2470','\u2471','\u2472','\u2473']
rlphabet={'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8,'J':9,'K':10}

check_list = {'덩크왕 다리우스': {'current_time': '30', 'times': 1}, '토투': {'current_time': 5, 'times': 4}, '왕자': {'current_time': 3, 'times': 3}, '덩크왕 다리': {'current_time': '30', 'times': 1}, 'night_life_': {'current_time': 4, 'times': 7}, '꿈틀이': {'current_time': 4, 'times': 2}, '권춘팔': {'current_time': 5, 'times': 1}, '어어': {'current_time': 5, 'times': 1}}

def check_horizontal(room,turn,position):
    count = 0
    overlap = []
    position_horizontal = int(position.split(' ')[0])
    position_vertical = int(position.split(' ')[1])
    ox = {0:'●',1:'■'}
    i = position_horizontal
    while(i>-1):
        if ttt_game_pad[room]['board'][position_vertical][i] == ox[turn]:
            count+=1
            overlap.append(str(position_vertical)+' '+str(i))
        i-=1
    i = position_horizontal
    while(i<len(ttt_game_pad[room]['board'][0])):
        hing = ttt_game_pad[room]['board'][position_vertical][i]
        #print(f'가로: {i} 세로: {position_vertical}\n칸: {hing} turn: {ox[turn]}')
        if ttt_game_pad[room]['board'][position_vertical][i] == ox[turn]:
            #print(overlap)
            if (str(position_vertical)+' '+str(i)) not in overlap:
                count+=1
        i+=1
    #print(count)
    if count >= ttt_game_pad[room]['win_line']:
        return True
    else:
        return False

def check_vertical(room,turn,position):
    count = 0
    overlap = []
    position_horizontal = int(position.split(' ')[0])
    position_vertical = int(position.split(' ')[1])
    ox = {0:'●',1:'■'}
    i = position_vertical
    while(i>-1):
        if ttt_game_pad[room]['board'][i][position_horizontal] == ox[turn]:
            count+=1
            overlap.append(str(i)+' '+str(position_horizontal))
        i-=1
    i = position_horizontal
    while(i<len(ttt_game_pad[room]['board'])):
        if ttt_game_pad[room]['board'][i][position_horizontal] == ox[turn]:
            if (str(i)+' '+str(position_horizontal)) not in overlap:
                count+=1
        i+=1
    if count >= ttt_game_pad[room]['win_line']:
        return True
    else:
        return False

def check_diagonal1(room,turn,position):
    count = 0
    overlap = []
    position_horizontal = int(position.split(' ')[0])
    position_vertical = int(position.split(' ')[1])
    ox = {0:'●',1:'■'}
    i = 0
    while(-1<(position_horizontal-i)):
        if (position_vertical-i) > -1:
             if ttt_game_pad[room]['board'][position_vertical-i][position_horizontal-i] == ox[turn]:
                count+=1
                overlap.append(str(position_vertical-i)+' '+str(position_horizontal-i))
        else:
            break
        i+=1
    i = 1
    while(len(ttt_game_pad[room]['board'][0]) > (position_horizontal+i)):
        if (position_vertical+i) < len(ttt_game_pad[room]['board']):
            if ttt_game_pad[room]['board'][position_vertical+i][position_horizontal+i] == ox[turn]:
                if (str(position_vertical+i)+' '+str(position_horizontal+i)) not in overlap:
                    count+=1
        else:
            break
        i+=1
    if count >= ttt_game_pad[room]['win_line']:
        return True
    else:
        return False

def check_diagonal2(room,turn,position):
    count = 0
    overlap = []
    position_horizontal = int(position.split(' ')[0])
    position_vertical = int(position.split(' ')[1])
    ox = {0:'●',1:'■'}
    i = 0
    try:
        while(len(ttt_game_pad[room]['board'][0]) >= (position_horizontal+i)):
            if (position_vertical-i) > -1:
                if ttt_game_pad[room]['board'][position_vertical-i][position_horizontal+i] == ox[turn]:
                    count+=1
                    overlap.append(str(position_vertical-i)+' '+str(position_horizontal+i))
            else:
                break
            i+=1
        i = 1
        while(-1 < (position_horizontal-i)):
            if (position_vertical+i) <= len(ttt_game_pad[room]['board']):
                if ttt_game_pad[room]['board'][position_vertical+i][position_horizontal-i] == ox[turn]:
                    if (str(position_vertical+i)+' '+str(position_horizontal-i)) not in overlap:
                        count+=1
            else:
                break
            i+=1
    except:
        return False
    if count >= ttt_game_pad[room]['win_line']:
        return True
    else:
        return False

def situation_check(room, horizontal, vertical, sender):
    all_filled = 0
    for i in range(len(ttt_game_pad[room]['board'])):
        for o in range(len(ttt_game_pad[room]['board'][i])):
            if ttt_game_pad[room]['board'][i][o] != '○':
                all_filled+=1
    if all_filled >= (len(ttt_game_pad[room]['board'])*len(ttt_game_pad[room]['board'][0])):
        return '모든 자리를 다썼으므로 게임을 종료합니다.'
    else:
        ox = {0:'●',1:'■'}
        turn = ttt_game_pad[room]['turn']
        where=''
        #a=False
        current_location = str(horizontal)+' '+str(vertical)
        a = True if check_horizontal(room,turn,current_location) else True if check_vertical(room,turn,current_location) else True if check_diagonal1(room,turn,current_location) else True if check_diagonal2(room,turn,current_location) else False
        #check_vertical(room,turn,current_location) if (a=True,where='세로') else check_diagonal1(room,turn,current_location) if (a=True,where='대각선') else check_diagonal2(room,turn,current_location) if (a=True,where='대각선2') else False
        if a == True:
            return sender+'(이)가 승리하였습니다.\n'+where
        else:
            return ''

def show_board(room):
    line=str(len(ttt_game_pad[room]['board'][0]))+'x'+str(len(ttt_game_pad[room]['board']))
    reply_list = []
    reply_list.append('│'+''.join(board_num[0:int(line.split('x')[0])])+'│')
    for i in range(int(line.split('x')[1])):
        reply_list.append(board_num[i]+('┼'*int(line.split('x')[0]))+'┤')
    reply_list.append('└'+('┴'*int(line.split('x')[0]))+'┘')
    board=ttt_game_pad[room]['board']
    for i in range(len(board)):
        a = list(reply_list[i+1])
        for o in range(len(board[i])):
            if board[i][o] != '○':
                a[o+1]=board[i][o]
                reply_list[i+1]=''.join(a)
    return '\n'.join(reply_list)



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
            hourtime+=9
            if hourtime >= 24:
                daytime+=1
                hourtime -= 24
            if message.author.name not in check_list.keys():
                check_list[message.author.name]={'current_time':'','times':0}
            if daytime != check_list[message.author.name]['current_time']:
                check_list[message.author.name]['current_time']=daytime
                check_list[message.author.name]['times']+=1
                name = ''
                if not message.author.nick:
                    name = str(message.author.name)
                else:
                    name = str(message.author.nick)
                will_send=time.strftime('%m월 ')+str(daytime)+'일 '+str(hourtime)+'시 '+time.strftime('%M분 %S초에 출석 하셨습니다.')
                will_send=will_send.replace('00','㏇').replace('0','').replace('㏇','0')
                embed = discord.Embed(title=name+'님',description=str(will_send), color=0x00aaaa)
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
        if message.content.startswith('!판'):
            room = message.guild.name
            if room not in ttt_game_pad.keys():
                ttt_game_pad[room]={}
                board_length=3
                win_line=3
                if message.content != '!판':
                    request = message.content.replace('!판 ','')
                    if ' ' in request:
                        request = request.split(' ')
                        if (request[0].isnumeric() and request[1].isnumeric()):
                            a=int(request[0])
                            b=int(request[1])
                            if (a>2 and b>2):
                                board_length = a
                                if a>=b:
                                    win_line = b
                                else:
                                    await message.channel.send('칸 넓이가 더 커야 합니다.')
                                    return
                            else:
                                await message.channel.send('최소 숫자는 3이어야 합니다.')
                                return
                        else:
                            await message.channel.send('숫자가 아닙니다.')
                            return
                ttt_game_pad[room]['board'] = []
                ttt_game_pad[room]['player'] = []
                ttt_game_pad[room]['turn'] = 0
                ttt_game_pad[room]['win_line'] = win_line
                ttt_game_pad[room]['player'].append(message.author.nick)
                ttt_game_pad[room]['mention_list'] = []
                ttt_game_pad[room]['mention_list'].append(message.author.mention)
                for i in range(board_length):
                    ttt_game_pad[room]['board'].append([])
                    for o in range(board_length):
                        ttt_game_pad[room]['board'][i].append('○')
                await message.channel.send('판이 세팅 되었습니다.')
                await message.channel.send(show_board(room))
            else:
                if message.author.nick not in ttt_game_pad[room]['player']:
                    ttt_game_pad[room]['player'].append(message.author.nick)
                    ttt_game_pad[room]['mention_list'].append(message.author.mention)
                    await message.channel.send('틱택토에 참가 하셨습니다.')
                else:
                    await message.channel.send('이미 참가 하셨습니다.')
        if message.content == '!ttt시작':
            room = message.guild.name
            if room in ttt_game_pad.keys():
                if message.author.nick in ttt_game_pad[room]['player']:
                    if len(ttt_game_pad[room]['player']) > 0:
                        await message.channel.send(ttt_game_pad[room]['mention_list'][ttt_game_pad[room]['turn']]+'님 가로 알파벳, 세로 숫자 순으로 놓을 자리를 정해주세요.\n예)!설치 A3')
                        ttt_game_pad[room]['gs'] = True
                    else:
                        await message.channel.send('인원수는 2명 이상이어야 합니다')
                else:
                    message.channel.send('ttt에 참가하지 않으셨습니다.')
        if message.content.startswith('!설치 '):
            room = message.guild.name
            if (room in ttt_game_pad.keys() and ttt_game_pad[room]['gs'] == True):
                request = message.content.replace('!설치 ','')
                if len(list(request)) == 2:
                    if ttt_game_pad[room]['player'][ttt_game_pad[room]['turn']] == message.author.nick:
                        horizontal = int(rlphabet[list(request)[0]])
                        vertical = int(list(request)[1])
                        if (len(ttt_game_pad[room]['board'][0]) > horizontal and len(ttt_game_pad[room]['board']) > vertical):
                            kan = ttt_game_pad[room]['board'][vertical][horizontal]
                            if (kan != '●' and kan != '■'):
                                ox = {0:'●', 1:'■'}
                                ttt_game_pad[room]['board'][vertical][horizontal] = ox[ttt_game_pad[room]['turn']]
                                a = situation_check(room, horizontal, vertical, message.author.nick)
                                if ('승리하였습니다' in a or '모든 자리를' in a):
                                    await message.channel.send(a)
                                    await message.channel.send(show_board(room))
                                    del ttt_game_pad[room]
                                    return
                                ttt_game_pad[room]['turn']+=1
                                if ttt_game_pad[room]['turn'] >= len(ttt_game_pad[room]['player']):
                                    ttt_game_pad[room]['turn'] = 0
                                await message.channel.send(show_board(room))
                                await message.channel.send(ttt_game_pad[room]['mention_list'][ttt_game_pad[room]['turn']]+'님 가로 알파벳, 세로 숫자 순으로 놓을 자리를 정해주세요.\n예)!설치 A3')
                            else:
                                await message.channel.send('이미 설치가 되어있습니다.')
                        else:
                            await message.channel.send('칸을 벗어났습니다.')
                    else:
                        await message.channel.send('당신 차례가 아닙니다.')
                else:
                    await message.channel.send('인자는 알파벳, 숫자 해서 2글자여야 합니다.')
                    
        if message.content.startswith('!삭제 '):
            if message.author.name == 'night_life_':
                await message.channel.purge(limit=int(message.content.replace('!삭제 ','')))
                mymsg=await message.channel.send(message.content.replace('!삭제 ','')+'개의 채팅을 삭제했습니다.')
                await asyncio.sleep(5)
                await mymsg.delete()
            else:
                await message.channel.send('권한이 없습니다.')

client = bot()
client.run(token)
