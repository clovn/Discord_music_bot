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

        queue.append(song)
    except Exception as e:
        print(e, 'string 38')


@tasks.loop(seconds=2.0)
async def main_loop():
    try:
        if not queue[0].playing and len(queue) > 0:
            await bot.get_channel(queue[0].text_channel).send(embed=queue[0].create_message('playing', len(queue)))
            queue[0].client.play(
                discord.FFmpegPCMAudio(executable="ffmpeg\\ffmpeg.exe", source=queue[0].track, **FFMPEG_OPTIONS),
                after=lambda e: queue.remove(queue[0]))
            queue[0].playing = True
    except:
        pass


@bot.listen()
async def on_ready():
    main_loop.start()


@bot.command()
async def pause(ctx):
    try:
        queue[0].client.pause()
    except Exception as e:
        print(e)


@bot.command()
async def resume(ctx):
    try:
        queue[0].client.resume()
    except Exception as e:
        print(e)


@bot.command()
async def ql(ctx):
    print(len(queue))
    try:
        if len(queue) > 1:
            embed = discord.Embed(title=f'Play next...', description=None, color=discord.Color.green())
            for i in range(1, len(queue)):
                embed.add_field(name=f'#{i}', value=f'{queue[i].title}', inline=False)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f':toolbox: Error', description=f'There is nothing In queue',
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
    except Exception as e:
        print(e)


@bot.command()
async def end(ctx):
    try:
        queue.clear()
        await queue[0].client.disconnect()
    except EOFError as e:
        print(e)


@bot.command()
async def skip(ctx):
    try:
        queue[0].client.stop()
    except Exception as e:
        print(e)


bot.run(TOKEN)
