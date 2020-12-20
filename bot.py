import random
import discord
import json
import bot_token as tokens
import re
from discord.ext import commands
from datetime import datetime

bot = commands.Bot(command_prefix='>')


def open_gamer_moments_file(guild_id, mode):
    """Open gamer moments file for a guild

    Args:
        guild_id (int): id of the guild
        mode (char*): mode to open the file

    Returns:
        file object: the opened file
    """
    return open('./{}_quotes.json'.format(str(guild_id)), mode, encoding='utf-8')

def open_gamer_words_file(guild_id, mode):
    """Open gamer words file for a guild

    Args:
        guild_id (int): id of the guild
        mode (char*): mode to open the file

    Returns:
        file object: the opened file
    """
    return open('./{}_gamerwords.txt'.format(str(guild_id)), mode, encoding='utf-8')

def get_gamer_moment_message(guild_id, user_name=None):
    """Get a gamer moment string from a guild

    Args:
        guild_id (int): id of the guild
        user_name (char*, optional): name of user to get moment from. Defaults to None.

    Returns:
        char*: The gamer moment string
    """
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

def add_gamer_word(strings, guild_id):
    """Add gamer word(s) to a guild

    Args:
        strings (char*): gamer word(s) to add
        guild_id (int): id of the guild
    """
    f = open_gamer_words_file(guild_id, 'a+')
    
    for string in strings:
        f.write(string.strip())
        f.write('\n')

    f.close()

def get_all_gamer_words(guild):
    
    """Get all gamer words for a guild

    Args:
        guild (discord.Guild): guild to get gamer words from

    Returns:
        char**: A list of all gamer words in a guild
    """
    gamer_words = []
    f = open_gamer_words_file(guild.id, 'r')

    for line in f:
        gamer_words.append(line.strip())
    
    f.close()
    
    return gamer_words

def remove_duplicate_gamer_words(guild):
    """Remove duplicate gamer words for a guild

    Args:
        guild (discord.Guild): guild to remove gamer words from
    """
    words = []
    
    f = open_gamer_words_file(guild.id, 'r+')

    for line in f:
        words.append(line.strip())
    # clear the entire file
    f.truncate(0)
    f.close()

    # remove duplicates
    words = list(dict.fromkeys(words))

    add_gamer_word(words, guild.id)

def get_username_format(user):
    """Get formatted username

    Args:
        user (discord.User): the user to get username from

    Returns:
        char*: username with format name#discriminator
    """
    return '{}#{}'.format(user.name, user.discriminator).lower()

def remove_gamer_word(guild_id, word_to_remove):
    """Remove a gamer word from a guild

    Args:
        guild_id (int): the guild to remove from
        word_to_remove (char*): the word to remove
    """
    f = open_gamer_words_file(guild_id, 'r')

    words = []
    for word in f:
        if word.strip() != word_to_remove: 
            words.append(word.strip())

    f.close()
    f = open_gamer_words_file(guild_id, 'w+')
    f.truncate(0)
    f.close()
    
    add_gamer_word(words, guild_id)

class GamerMoments(commands.Cog, name='Gamer Moments'):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def add(self, ctx, *args):
        """Add a gamer word"""
        add_gamer_word(args, ctx.guild.id)
        await ctx.send('Added {} new gamer words: {}'.format(len(args), ', '.join(args)))

    @commands.command()
    async def remove(self, ctx, arg):
        """Remove a gamer word"""
        remove_duplicate_gamer_words(ctx.guild)
        remove_gamer_word(ctx.guild.id, arg)
        await ctx.send('Removed gamer word: {}'.format(arg))

    @commands.command()
    async def gamerwords(self, ctx):
        """List all gamer words"""
        await ctx.send('Here are the gamer words for this server: {}'.format(str(get_all_gamer_words(ctx.guild))))

    @commands.command()
    async def moment(self, ctx, *args):
        """Post a gamer moment from a random user. Pass a user's username#discriminator as a parameter to post gamer moment for a specific user."""
        quote = ''
        if len(args) > 0:
            user_name = args[0]
            quote = get_gamer_moment_message(ctx.guild.id, user_name.lower())
        else:
            quote = get_gamer_moment_message(ctx.guild.id)

        await ctx.send(quote)

    @commands.command()
    async def makegamermoments(self, ctx):
        """Create a list of gamer moments. Messages are retrieved from the channel the command is run on. Expensive operation. Overwrites previous gamer moments."""
        amount = 50000
        remove_duplicate_gamer_words(ctx.guild)
        await ctx.send('Making epic gamer moments... Please wait. I will tell you when I am done, hihi :). That is if I don\'t crash... :). You can still use me while I am working, but I may be slow :(')
        channel_messages = await ctx.history(limit=amount).flatten()
        await ctx.send('Status: I have now received {} messages :). I humbly ask of you to wait just a little longer... Please... :). Also, please refrain from adding or removing words until I have finished. :)'.format(len(channel_messages)))
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

@bot.command()
async def github(ctx):
    """Posts the GitHub repository for this bot."""
    await ctx.send('You can find me at: https://github.com/StevenDankMeister/peanut-bot >_<')

@bot.event
async def on_command_error(ctx, exception):
    await ctx.send('Sorry, I made a mistake >_<... If you used >makegamermoments, please try again, okay? It\'s a very hard and demanding task...\nError: {}'.format(exception))


@bot.event
async def on_ready():
    print('ready')

bot.add_cog(GamerMoments(bot))
bot.run(tokens.bot_token)
