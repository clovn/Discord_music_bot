import discord
from discord.ext import commands
from discord.ext import tasks
from discord.utils import get

from CONST import TOKEN
from song import Song

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
queue = []

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'False'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


@bot.command()
async def play(ctx, *, query):
    song = Song(query, ctx.message.channel.id, ctx.message.author.voice.channel,
                get(bot.voice_clients, guild=ctx.guild), ctx.message.author, ctx.message.author.avatar)

    if song.client is None:
        try:
            song.client = await song.voice_channel.connect()
        except Exception as e:
            await ctx.send('Бот подключен к другому каналу')
            print(e, 'string 30')

    try:
        if song.client.is_playing():
            await ctx.send(embed=song.create_message('add_to_queue', len(queue)))
        else:
            await ctx.send(embed=song.create_message('playing', len(queue)))

        queue.append(song)
    except Exception as e:
        print(e, 'string 38')

    # info_list.append(ctx.message.channel.id)
    # info_list.append('')
    # try:
    #     voice_channel = ctx.message.author.voice.channel
    #     info_list[5] = get(bot.voice_clients, guild=ctx.guild)
    #
    #     if info_list[5] and info_list[5].is_connected():
    #         await info_list[5].move_to(voice_channel)
    #     else:
    #         info_list[5] = await voice_channel.connect()
    #
    #     if info_list[5].is_playing():
    #         queue.append(info_list)
    #         embed = discord.Embed(title=f'Position in queue #{int(queue.index(info_list)+1)}', description=f'[{info_list[1]}]({info_list[3]})', color=discord.Color.blue())
    #         embed.set_thumbnail(url=info_list[2])
    #         # embed.set_footer(text=f'Added by {ctx.message.author}', icon_url=ctx.message.author.avatar.url)
    #         await ctx.send(embed=embed)
    #     else:
    #         await ctx.send(embed=create_message('playing', info_list[1], info_list[2], info_list[3], ctx.message.author, ctx.message.author.avatar))
    #         info_list[5].play(discord.FFmpegPCMAudio(executable="ffmpeg\\ffmpeg.exe", source=info_list[0], **FFMPEG_OPTIONS))
    #
    # except EOFError as e:
    #     print(e)


@tasks.loop(seconds=2.0)
async def main_loop():
    try:
        if not queue[0].playing and len(queue) > 0:
            await bot.get_channel(queue[0].text_channel).send(embed=queue[0].create_message('playing', len(queue)))
            queue[0].client.play(discord.FFmpegPCMAudio(executable="ffmpeg\\ffmpeg.exe", source=queue[0].track, **FFMPEG_OPTIONS), after=lambda e: queue.remove(queue[0]))
            queue[0].playing = True

    except Exception as e:
        print(e, 'string 74')


@bot.listen()
async def on_ready():
    main_loop.start()


# @bot.command()
# async def pause(ctx):
#     try:
#         info_list[5].pause()
#     except Exception as e:
#         print(e)


# @bot.command()
# async def resume(ctx):
#     try:
#         info_list[5].resume()
#     except Exception as e:
#         print(e)


@bot.command()
async def ql(ctx):
    try:
        if len(queue) > 0:
            embed = discord.Embed(title=f'Play next...', description=None, color=discord.Color.green())
            for i in range(1, len(queue) + 1):
                embed.add_field(name=f'#{i}', value=f'{queue[i - 1][1]}', inline=False)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f':toolbox: Error', description=f'There is nothing In queue',
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
    except Exception as e:
        print(e)


# @bot.command()
# async def end(ctx):
#     try:
#         info_list[5].stop()
#     except EOFError as e:
#         print(e)
#         await ctx.send("ty eblan")
#
#
# @bot.command()
# async def skip(ctx):
#     try:
#         if info_list[5].is_playing() and len(queue) >= 1:
#             info_list[5].stop()
#             await ctx.send('music skipped')
#         else:
#             embed = discord.Embed(title=f':toolbox: Error', description=f'There is nothing to skip',
#                                   color=discord.Color.red())
#             await ctx.send(embed=embed)
#     except Exception as e:
#         print(e)


# @bot.command()
# async def skip():
#     try:
#         await info_list[5].skip()
#     except Exception as e:
#         print(e)

bot.run(TOKEN)
