import discord
from discord.ext import commands
from uptime import uptime
import requests
import psutil
import cpuinfo
import json

with open('config/config.json', 'r') as f:
    config = json.load(f)

Token = config['Token']
Prefix = config['Prefix']

cpu = cpuinfo.get_cpu_info()["brand_raw"]
threads = cpuinfo.get_cpu_info()["count"]

Client = commands.Bot(command_prefix=f'{Prefix}', intents=discord.Intents.all())

@Client.event
async def on_ready():
    print(f"✦ Logged in as {Client.user}\n✦ Py-cord version: {discord.__version__}")
    await Client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="servers"))

@Client.command(name="ping")
async def ping(ctx):
    await ctx.trigger_typing()
    await ctx.reply(f"My Ping Is **{round(Client.latency * 1000)}ms**")

@Client.command(name='status')
async def host(ctx):
    up = uptime()
    time = float(up)
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    response = requests.get(f"http://ip-api.com/json/").json()
    uptime_stamp = ("%dd %dh %dm %ds" % (day, hour, minutes, seconds))
    cpu_usage = f"CPU Usage: {psutil.cpu_percent(interval=1)}%"
    ram_usage = f"Ram Usage: {round(psutil.virtual_memory().used/1000000000, 2)}GB / {round(psutil.virtual_memory().total/1000000000, 2)}GB"
    swap_usage = f"SWAP Usage: {round(psutil.swap_memory().used/1000000000, 2)}GB / {round(psutil.swap_memory().total/1000000000, 2)}GB"
    disk_usage = f"Disk Usage: {round(psutil.disk_usage('/').used/1000000000, 2)}GB / {round(psutil.disk_usage('/').total/1000000000, 2)}GB"

    Embed = discord.Embed()
    Embed.set_author(name="SysInfo", url="https://s10.gifyu.com/images/SrfeN.png", icon_url="https://s10.gifyu.com/images/SrfeN.png")
    Embed.add_field(name=f"⎯ CPU ⎯",value=f"**Model**: {cpu}\n**Cores**: {threads}", inline=True)
    Embed.add_field(name=f"⎯ RAM ⎯", value=f"**Total RAM**: {round(psutil.virtual_memory().total/1000000000, 2)}GB\n**Total Swap**: {psutil.swap_memory().total /1024 /1024 / 1024}GB",inline=True)
    Embed.add_field(name=f"⎯ UPTIME ⎯", value=f"{uptime_stamp}", inline=True)
    Embed.add_field(name= f"⎯ HOST ⎯", value= f"**Organization**: {response['isp']}\n**IP Address**: {response['query']}")
    Embed.add_field(name= f"⎯ USAGES ⎯", value= f"\n**```\n\n{cpu_usage} \n{ram_usage}\n{swap_usage}\n{disk_usage}```**", inline=False)
    Embed.set_footer(text=f"Requested by {ctx.author.display_name} | Created by adriichu#0", icon_url=ctx.author.display_avatar.url)
    await ctx.trigger_typing()
    await ctx.reply(embed=Embed)

Client.run(Token)
