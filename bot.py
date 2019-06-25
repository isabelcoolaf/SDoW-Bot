#! /usr/bin/env python3.6

"""
Made by Isabel Lomas for DISCORD HACK WEEK 2019!
"""

import aiohttp
import asyncio
from datetime import datetime
import discord
from discord.ext import commands
import json

c = json.load(open('config.json'))

b = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or('sdow-'), case_insensitive=True, activity=discord.Game(name='Six Degrees of Wikipedia!'))
b.remove_command('help')

async def g(s, t, o, e, m):
    def k(t):
        return 'https://en.wikipedia.org/wiki/' + t.replace(' ', '_')
    d = '{"source": "%s", "target": "%s"}' % (s, t)
    l = str(len(d))
    h = {"Content-Type": "application/json", "Content-Length": l}
    async with aiohttp.ClientSession() as p:
        async with p.post('https://api.sixdegreesofwikipedia.com/paths', data=d.encode('UTF-8'), headers=h) as r:
            pagel = []
            e.timestamp = datetime.utcnow()
            d = await r.json()
            if r.status == 400:
                e.color = discord.Color.red()
                e.title = 'Error'
                e.description = d['error']
                pagel.append(e)
            if r.status == 200:
                e.color = discord.Color.green()
                e.title = f'Links from {d["sourcePageTitle"]} to {d["targetPageTitle"]}'
                if len(d['paths']) == 0:
                    e.color = discord.Color.red()
                    e.title = 'Error'
                    e.description = f"There are no paths of Wikipedia links between {d['sourcePageTitle']} and {d['targetPageTitle']}."
                    pagel.append(e)
                else:
                    pp = ''
                    pd = ''
                    pps = ''
                    if len(d['paths']) != 1:
                        pp = 's'
                    if len(d['paths'][0])-1 != 1:
                        pd = 's'
                    surl = k(d['sourcePageTitle'])
                    turl = k(d['targetPageTitle'])
                    fs = {"0": ""}
                    page = 0
                    for path in d['paths']:
                        rs = ""
                        for i in path:
                            t = d['pages'][str(i)]['title']
                            rs += f"- [{t}]({d['pages'][str(i)]['url']}) "
                        if (len(fs[str(page)]) + len(rs) + 1) <= 1024:
                            fs[str(page)] += rs + "\n"
                        else:
                            page += 1
                            fs[str(page)] = rs + "\n"
                    egi = -1
                    for _, k in fs.items():
                        if len(e) >= 6000:
                            e.remove_field(egi)
                            pagel.append(e)
                            e = discord.Embed(color=discord.Color.green(), title=f'Links from {d["sourcePageTitle"]} to {d["targetPageTitle"]}', description=f"{len(d['paths'])} path{pp} with {len(d['paths'][0])-1} degree{pd} of separation.\n{len(pagel)} page{pps}.")
                            e.clear_fields()
                            e.add_field(name='Original Articles', value=f'- [{d["sourcePageTitle"]}]({surl})\n- [{d["targetPageTitle"]}]({turl})', inline=False)
                            egi = -1
                        if egi == 23:
                            pagel.append(e)
                            e = discord.Embed(color=discord.Color.green(), title=f'Links from {d["sourcePageTitle"]} to {d["targetPageTitle"]}', description=f"{len(d['paths'])} path{pp} with {len(d['paths'][0])-1} degree{pd} of separation.\n{len(pagel)} page{pps}.")
                            e.clear_fields()
                            e.add_field(name='Original Articles', value=f'- [{d["sourcePageTitle"]}]({surl})\n- [{d["targetPageTitle"]}]({turl})', inline=False)
                            egi = -1
                        egi += 1
                        e.add_field(name='Paths', value=k, inline=False)
                    pagel.append(e)
                    pi = 0
                    de = ""
                    for j in pagel:
                        pi += 1
                        if len(pagel) != 1:
                            de = f"\n{pi}/{len(pagel)} pages."
                        j.description = f"{len(d['paths'])} path{pp} with {len(d['paths'][0])-1} degree{pd} of separation." + de
            await m.edit(embed=pagel[0])

@b.command(name='info')
async def i(o):
    e = discord.Embed(color=0x68ceff, description='Made by Isabel#0002', title='About SDoW')
    e.add_field(name='About', value='Six Degrees of Wikipedia (The Discord Bot) is made for Discord Hack Week in 2019.\nThe bot is based off the [Six Degrees of Wikipedia](https://sixdegreesofwikipedia.com) game.', inline=False)
    e.add_field(name='Links', value='[discord.py](https://github.com/Rapptz/discord.py)\n[GitHub (for this bot)](https://github.com/Mippy/SDOW-Bot)\n[Six Degrees of Wikipedia](https://sixdegreesofwikipedia.com)\n[GitHub (for the site above)](https://github.com/jwngr/sdow)', inline=False)
    e.set_thumbnail(url='https://raw.githubusercontent.com/wikimedia/portals/master/dev/wikipedia.org/assets/img/Wikipedia-logo-v2.png')
    e.timestamp = datetime.utcnow()
    e.set_footer(text=f'Requested by {o.author} ({o.author.id})')
    await o.send(embed=e)

@b.command(name='help')
async def h(o):
    a = o.author
    # TODO
    e = discord.Embed(color=0x68ceff, title='SDoW Help', description='tbd')
    e.timestamp = datetime.utcnow()
    try:
        await a.send(embed=e)
        if o.guild:
            await o.send(f'{a.mention} check your DMs :eyes:')
    except discord.Forbidden:
        await o.send(f'{a.mention} could you check your privacy settings and try again? I need to be able to DM you ( ‘ ͡ . ͜ ʖ ͡ . )')

@b.command(name='play')
async def p(o):
    a = o.author
    def c(m):
        return m.author.id == a.id and m.channel.id == o.channel.id
    async def i(s):
        if s:
            q = await o.send(f'{a.mention} What is the first article?')
        else:
            q = await o.send(f'{a.mention} What is the second article?')
        try:
            m = await b.wait_for('message', check=c, timeout=60)
        except asyncio.TimeoutError:
            await o.send(f'{a.mention} action timed out.')
            await q.delete()
            return
        await q.delete()
        if not m.content:
            try:
                await m.delete()
            except: pass
            await o.send(f'{a.mention} why?? why are you doing this to me? i just want to function normally then i have to make an edge case because *someone* decided to upload an image or post a game/spotify invite. grrRRRRRR :japanese_goblin:')
            return
        v = m.content
        try:
            await m.delete()
        except: pass
        return v
    s = await i(True)
    if not s:
        return
    t = await i(False)
    if not t:
        return
    e = discord.Embed(color=0x68ceff, title='Processing', description='Processing possible paths... Hang tight!\nThis might take a while if there are a lot of paths.')
    e.timestamp = datetime.utcnow()
    e.set_footer(text=f'Requested by {a} ({a.id})')
    m = await o.send(embed=e)
    await g(s, t, o, e, m)

b.run(c['token'])