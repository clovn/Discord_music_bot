import discord
from discord.ext import tasks
from song import searcher, update_audio_url
from discord.ext import commands
from discord.utils import get
from CONST import TOKEN

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
music_list = []


YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'False'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

@bot.command()
async def play(ctx, *, arg):
    global vc
    global info_list

    info_list = searcher(arg) # [audio_url, title, image_url, video_url, chanel_id]
    info_list.append(ctx.message.channel.id)
    info_list.append('')
    try:
        voice_channel = ctx.message.author.voice.channel
        info_list[5] = get(bot.voice_clients, guild=ctx.guild)

        if info_list[5] and info_list[5].is_connected():
            await info_list[5].move_to(voice_channel)
        else:
            info_list[5] = await voice_channel.connect()

        if info_list[5].is_playing():
            music_list.append(info_list)
            embed = discord.Embed(title=f'Position in queue #{int(music_list.index(info_list)+1)}', description=f'[{info_list[1]}]({info_list[3]})',color=discord.Color.blue())
            embed.set_thumbnail(url=info_list[2])
            # embed.set_footer(text=f'Added by {ctx.message.author}', icon_url=ctx.message.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=':musical_note: Now playing', description=f'[{info_list[1]}]({info_list[3]})', color=discord.Color.blue())
            embed.set_thumbnail(url=info_list[2])
            # embed.set_footer(text=f'Added by {ctx.message.author}', icon_url=ctx.message.author.avatar.url)
            await ctx.send(embed=embed)


            info_list[5].play(discord.FFmpegPCMAudio(executable="ffmpeg\\ffmpeg.exe", source=info_list[0], **FFMPEG_OPTIONS))



    except EOFError as e:
        print(e)

@tasks.loop(seconds=5.0)
async def main_loop():
    print(len(music_list))
    try:
        if info_list[5].is_connected() and not info_list[5].is_playing() and len(music_list) >= 1:

                embed = discord.Embed(title='Now playing', description=f'[{music_list[0][1]}]({music_list[0][3]})',
                                      color=discord.Color.blue())
                embed.set_thumbnail(url=music_list[0][2])
                # embed.set_footer(text=f'Added by {user.message.author}', icon_url=user.message.author.avatar.url)
                await bot.get_channel(info_list[4]).send(embed=embed)
                # music_list[0][0] = update_audio_url(music_list[0][3])
                info_list[5].play(discord.FFmpegPCMAudio(executable="ffmpeg\\ffmpeg.exe", source=music_list[0][0], **FFMPEG_OPTIONS))
                music_list.remove(music_list[0])
    except Exception as e:
        print(e)
@bot.listen()
async def on_ready():
    main_loop.start()
# @main_loop.before_loop # Это необходимо, чтобы ваш таск ждал, пока бот полностью запустится.
# async def yourname2(): # Назвать эту функцию можно тоже как угодно.
#     await bot.wait_until_ready()

@bot.command()
async def pause(ctx):
    try:
        info_list[5].pause()
    except Exception as e:
        print(e)

@bot.command()
async def resume(ctx):
    try:
        info_list[5].resume()
    except Exception as e:
        print(e)

@bot.command()
async def ql(ctx):
    try:
        if len(music_list) >= 1:
            embed = discord.Embed(title=f'Play next...', description=None, color=discord.Color.green())
            for i in range(1, len(music_list)+1):
                embed.add_field(name=f'#{i}', value=f'{music_list[i-1][1]}', inline=False)
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
        info_list[5].stop()
    except EOFError as e:
        print(e)
        await ctx.send("ty eblan")

@bot.command()
async def skip(ctx):
    try:
        if info_list[5].is_playing() and len(music_list) >= 1:
            info_list[5].stop()
            await ctx.send('music skipped')
        else:
            embed = discord.Embed(title=f':toolbox: Error', description=f'There is nothing to skip',
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
    except Exception as e:
        print(e)

# @bot.command()
# async def skip():
#     try:
#         await vc.skip()
#     except Exception as e:
#         print(e)

bot.run(TOKEN)
