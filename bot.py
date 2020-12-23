import discord
import bot_token as tokens
import gamer_moments as gamer_moments
from discord.ext import commands

bot = commands.Bot(command_prefix='>')

class GamerMoments(commands.Cog, name='Gamer Moments'):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def add(self, ctx, *args):
        """Add a gamer word"""
        gamer_moments.add_gamer_word(args, ctx.guild.id)
        await ctx.send('Added {} new gamer words: {}'.format(len(args), ', '.join(args)))

    @commands.command()
    async def remove(self, ctx, arg):
        """Remove a gamer word"""
        gamer_moments.remove_duplicate_gamer_words(ctx.guild)
        gamer_moments.remove_gamer_word(ctx.guild.id, arg)
        await ctx.send('Removed gamer word: {}'.format(arg))

    @commands.command()
    async def gamerwords(self, ctx):
        """List all gamer words"""
        await ctx.send('Here are the gamer words for this server: {}'.format(str(gamer_moments.get_all_gamer_words(ctx.guild))))

    @commands.command()
    async def moment(self, ctx, *args):
        """Post a gamer moment from a random user. Pass a user's username#discriminator as a parameter to post gamer moment for a specific user."""
        quote = ''
        if len(args) > 0:
            user_name = args[0]
            quote = gamer_moments.get_gamer_moment_message(ctx.guild.id, user_name.lower())
        else:
            quote = gamer_moments.get_gamer_moment_message(ctx.guild.id)

        await ctx.send(quote)

    @commands.command()
    async def makegamermoments(self, ctx, arg):
        """Create a list of gamer moments from a specific channel ID. Messages are retrieved from the channel the command is run on. Expensive operation. Overwrites previous gamer moments."""
        amount = 20
        gamer_moments.remove_duplicate_gamer_words(ctx.guild)
        
        channel = await bot.fetch_channel(arg)

        if channel == None:
            await ctx.send('Could not find channel with id: {}'.format(arg))
            return
            
        await ctx.send('Making epic gamer moments in: **{}**. Please wait. I will tell you when I am done, hihi :). That is if I don\'t crash... :). You can still use me while I am working, but I may be slow :('
                        .format(channel.name))

        channel_messages = await channel.history(limit=amount).flatten()
        await ctx.send('Status: I have now received {} messages :). I humbly ask of you to wait just a little longer... Please... :). Also, please refrain from adding or removing words until I have finished. :)'.format(len(channel_messages)))
        
        gamer_moments_count = gamer_moments.make_gamer_moments(channel_messages, ctx.guild.id)
        
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
