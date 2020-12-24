import random
import json

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
        # Prevent biased random by combining all arrays in the hash map to one array
        all_quotes = []
        for user_quotes in moments_dic.values():
            all_quotes += user_quotes

        gamer_moment_sentence = random.choice(all_quotes)
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

def make_gamer_moments(channel_messages, guild_id):
    """Creates gamer moments from a list of discord.Message

    Args:
        channel_messages (discord.Message*): list of discord messages
        guild_id (int): id of guild with messages

    Returns:
        int: amount of gamer moments created
    """
    data = {}
    gamer_moments_count = 0
    gamermoments_file = open_gamer_moments_file(guild_id, 'w+')

    for message in channel_messages:
        if message.content.startswith(('>', '<')):
            continue

        if message.author.bot:
            continue

        gamerwords_file = open_gamer_words_file(guild_id, 'r+')
        
        for word in gamerwords_file:
            if word.strip() in message.content:
                user = message.author
                
                string = '\"{}\" - {} {}/{}-{}'.format(message.content, message.author.name, message.created_at.day, message.created_at.month, message.created_at.year)
                if get_username_format(user) not in data:
                    data[get_username_format(user)] = []
                
                if string in data[get_username_format(user)]:
                    continue

                gamer_moments_count += 1
                data[get_username_format(user)].append(string)
        
        gamerwords_file.close()
    
    json.dump(data, gamermoments_file)

    gamermoments_file.close()

    return gamer_moments_count
