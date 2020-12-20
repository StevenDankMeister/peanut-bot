import random
import discord
import json
import bot_token as tokens
from discord.ext import commands
from datetime import datetime

bot = commands.Bot(command_prefix='>')

def get_gamer_moment_message(guild, user_id):
    with open('./{}_quotes.json'.format(str(guild.id)), 'r', encoding='utf-8') as f:
        data = json.load(f)
        if user_id == None:
            random_user_id = random.choice(list(data))
            return random.choice(data[random_user_id])
        else:
            return random.choice(data[user_id])
            


def add_moment(strings, guild):
    with open('./{}_gamerwords.txt'.format(str(guild.id)), 'a+', encoding='utf-8') as f:
        for string in strings:
            f.write(string.strip())
            f.write('\n')

def get_all_gamer_words(guild):
    gamer_words = []
    with open('./{}_gamerwords.txt'.format(str(guild.id)), 'r', encoding='utf-8') as f:
        for line in f:
            gamer_words.append(line.strip())

    return gamer_words

def remove_duplicate_gamer_words(guild):
    words = []
    
    with open('./{}_gamerwords.txt'.format(str(guild.id)), 'r+', encoding='utf-8') as f:
        for line in f:
            words.append(line.strip())
        f.truncate(0)

    words = list(dict.fromkeys(words))

    add_moment(words, guild)

@bot.command()
async def getgamerwords(ctx):
    await ctx.send('Here are the gamer words for this server: {}'.format(str(get_all_gamer_words(ctx.guild))))

@bot.command()
async def moment(ctx, *args):
    try:
        quote = ''
        if len(args) > 0:
            id = args[0]
            id = id.replace("<@!","")
            id = id.replace(">","")
            quote = get_gamer_moment_message(ctx.guild, id)
        else:
            quote = get_gamer_moment_message(ctx.guild, None)

        await ctx.send(quote)
    except:
        await ctx.send('Gamer moments are empty. Please create gamer moments using the command >makegamermoments :)')

@bot.command()
async def add(ctx, *args):
    add_moment(args, ctx.guild)
    await ctx.send('Added {} new gamer words: {}'.format(len(args), ', '.join(args)))

@bot.command()
async def makegamermoments(ctx):
    remove_duplicate_gamer_words(ctx.guild)
    await ctx.send('Making epic gamer moments... Please wait. I will tell you when I am done, hihi :). That is if I don\'t crash... :). You can still use me while I am working, but I may be slow :(')
    channel_messages = await ctx.history(limit=50000).flatten()
    data = {}
    gamer_moments_count = 0
    with open('./{}_quotes.json'.format(str(ctx.guild.id)), 'w+', encoding='utf-8') as f:
        for message in channel_messages:

            if message.author == bot.user:
                continue

            if message.content.startswith('>'):
                continue

            if message.author.bot:
                continue

            with open('./{}_gamerwords.txt'.format(str(ctx.guild.id)), 'r+', encoding='utf-8') as f_:
                for word in f_:
                    if word.strip() in message.content:
                        gamer_moments_count += 1
                        string = '\"{}\" - {} {}/{}-{}'.format(message.content, message.author.name, message.created_at.day, message.created_at.month, message.created_at.year)
                        if message.author.id not in data:
                            data[message.author.id] = []
                        data[message.author.id].append(string)
        print(data)
        json.dump(data, f)

    await ctx.send('できました！ {} gamer moments have been created :)'.format(gamer_moments_count))

@bot.event
async def on_command_error(ctx, exception):
    await ctx.send('I am sorry, but an error occured :(. I don\'t understand special characters :(. If you used >makegamermoments, please try again, okay? hihi :)\nError: {}'.format(exception))


@bot.event
async def on_ready():
    print('ready')

bot.run(tokens.bot_token)
