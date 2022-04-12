from discord import *
from discord.ext import commands, tasks
from json import load,dump
from datetime import timedelta, datetime
from copy import deepcopy
from colorama import Fore,init

with open('config.json','r') as file: token = load(file)['token']

init(autoreset=True)
bot = commands.Bot('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

def get_time(): return datetime.now().strftime('%Y/%m/%d %H:%M:%S')

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        with open('messages.json','r') as file: messages = load(file)
        if str(message.channel.id) not in messages: messages[str(message.channel.id)] = {}
        messages[str(message.channel.id)][str(message.id)] = (datetime.now()+timedelta(hours=24)).timestamp()
        with open('messages.json','w') as file: dump(messages,file,indent=4)
        print(f"{Fore.BLUE}INFO{Fore.RESET} - {get_time()} - Message ID({message.id}) in Channel ID({message.channel.id}) saved")

@bot.event
async def on_ready():
    print(f'{Fore.BLUE}INFO{Fore.RESET} - {get_time()} - Logged in as {"#".join([bot.user.name,bot.user.discriminator])}')
    watchdog.start()


@tasks.loop(seconds=5)
async def watchdog():
    with open('messages.json','r') as file: messages = load(file)
    mL = deepcopy(messages)
    for channel in mL:
        for message in mL[channel]:
            if mL[channel][message] < datetime.now().timestamp():
                try: await bot.http.delete_message(int(channel),int(message))
                except NotFound:
                    print(f"{Fore.RED}ERROR{Fore.RESET} - {get_time()} - Message ID({message}) in Channel ID({channel}) not found | Deleted from file")
                    messages[channel].pop(message)
                except: pass
                else:
                    print(f"{Fore.BLUE}INFO{Fore.RESET} - {get_time()} - Message ID({message}) in Channel ID({channel}) deleted")
                    messages[channel].pop(message)
    with open('messages.json','w') as file: dump(messages,file,indent=4)

bot.run(token,bot=False)