import random
import discord
import json
import bot_token as tokens
import re
from discord.ext import commands
from datetime import datetime

bot = commands.Bot(command_prefix='>')

def open_gamer_moments_file(guild_id, mode):
    return open('./{}_quotes.json'.format(str(guild_id)), mode, encoding='utf-8')

def open_gamer_words_file(guild_id, mode):
    return open('./{}_gamerwords.txt'.format(str(guild_id)), mode, encoding='utf-8')

def get_gamer_moment_message(guild_id, user_name):
    f = open_gamer_moments_file(guild_id, 'r')

    moments_dic = json.load(f)

    gamer_moment_sentence = ''

    if user_name == None:
        random_user_id = random.choice(list(moments_dic))
        gamer_moment_sentence = random.choice(moments_dic[random_user_id])
    else:
        gamer_moment_sentence = random.choice(moments_dic[user_name]) 

    f.close()
    return gamer_moment_sentence 

def add_moment(strings, guild):
    f = open_gamer_words_file(guild.id, 'a+')
    for string in strings:
        f.write(string.strip())
        f.write('\n')

    f.close()

def get_all_gamer_words(guild):
    gamer_words = []
    f = open_gamer_words_file(guild.id, 'r')

    for line in f:
        gamer_words.append(line.strip())
    
    f.close()
    
    return gamer_words

def remove_duplicate_gamer_words(guild):
    words = []
    
    f = open_gamer_words_file(guild.id, 'r+')

    for line in f:
        words.append(line.strip())
    # clear the entire file
    f.truncate(0)

    # remove duplicates
    words = list(dict.fromkeys(words))

    add_moment(words, guild)

def get_username_format(user):
    return '{}#{}'.format(user.name, user.discriminator)

@bot.command()
async def gamerwords(ctx):
    await ctx.send('Here are the gamer words for this server: {}'.format(str(get_all_gamer_words(ctx.guild))))

@bot.command()
async def moment(ctx, *args):
    quote = ''
    if len(args) > 0:
        user_name = args[0]
        quote = get_gamer_moment_message(ctx.guild.id, user_name)
    else:
        quote = get_gamer_moment_message(ctx.guild.id, None)

    await ctx.send(quote)

@bot.command()
async def add(ctx, *args):
    add_moment(args, ctx.guild)
    await ctx.send('Added {} new gamer words: {}'.format(len(args), ', '.join(args)))

@bot.command()
async def makegamermoments(ctx):
    amount = 50000
    remove_duplicate_gamer_words(ctx.guild)
    await ctx.send('Making epic gamer moments... Please wait. I will tell you when I am done, hihi :). That is if I don\'t crash... :). You can still use me while I am working, but I may be slow :(')
    channel_messages = await ctx.history(limit=amount).flatten()
    await ctx.send('Status: I have now received {} messages :). I humbly ask of you to wait just a little longer... Please... :). Also, please refrain from addings words until I have finished. :)'.format(len(channel_messages)))
    data = {}
    gamer_moments_count = 0
    gamermoments_file = open_gamer_moments_file(ctx.guild.id, 'w+')

    for message in channel_messages:
        if message.author == bot.user:
            continue

        if message.content.startswith('>'):
            continue

        if message.author.bot:
            continue

        gamerwords_file = open_gamer_words_file(ctx.guild.id, 'r+')
        
        for word in gamerwords_file:
            if word.strip() in message.content:
                gamer_moments_count += 1
                user = message.author
                
                string = '\"{}\" - {} {}/{}-{}'.format(message.content, message.author.name, message.created_at.day, message.created_at.month, message.created_at.year)
                if get_username_format(user) not in data:
                    data[get_username_format(user)] = []
                
                data[get_username_format(user)].append(string)
        
        gamerwords_file.close()
    
    json.dump(data, gamermoments_file)

    gamermoments_file.close()

    await ctx.send('できました！ {} gamer moments have been created :)'.format(gamer_moments_count))

@bot.event
async def on_command_error(ctx, exception):
    await ctx.send('Sorry, I made a mistake >_<... If you used >makegamermoments, please try again, okay? It\'s a very hard and demanding task...\nError: {}'.format(exception))


@bot.event
async def on_ready():
    print('ready')

bot.run(tokens.bot_token)
