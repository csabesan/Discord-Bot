import discord
from discord.ext import commands
import os
import asyncio
import yt_dlp
from dotenv import load_dotenv
import urllib.parse, urllib.request, re

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}
        self.voice_clients = {}
        
        load_dotenv()
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)
        self.youtube_base_url = "https://www.youtube.com/"
        self.youtube_results_url = self.youtube_base_url + 'results?'
        self.youtube_watch_url = self.youtube_base_url + 'watch?v='
        self.yt_dl_options = {"format": "bestaudio/best"}
        self.ytdl = yt_dlp.YoutubeDL(self.yt_dl_options)
        self.ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn -filter:a "volume=0.25"', 'executable': 'C:/ffmpeg/ffmpeg.exe'}

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music cog loaded")

    async def play_next(self, ctx):
        if self.queues.get(ctx.guild.id):
            link = self.queues[ctx.guild.id].pop(0)
            await self.play(ctx, link=link)

    @commands.command(name="play")
    async def play(self, ctx, *, link):
        try:
            voice_client = await ctx.author.voice.channel.connect()
            self.voice_clients[voice_client.guild.id] = voice_client
        except Exception as e:
            print(e)

        try:
            if "www.youtube.com" not in link:
                query_string = urllib.parse.urlencode({'search_query': link})
                content = urllib.request.urlopen(self.youtube_results_url + query_string)
                search_results = re.findall(r'/watch\?v=(.{11})', content.read().decode())
                link = self.youtube_watch_url + search_results[0]

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(link, download=False))

            song = data['url']
            player = discord.FFmpegOpusAudio(song, **self.ffmpeg_options)
            self.voice_clients[ctx.guild.id].play(player, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop))
        except Exception as e:
            print(e)

    @commands.command(name="clear")
    async def clear_queue(self, ctx):
        if self.queues.get(ctx.guild.id):
            self.queues[ctx.guild.id].clear()
            await ctx.send("Queue cleared!")
        else:
            await ctx.send("There is no queue to clear")

    @commands.command(name="pause")
    async def pause(self, ctx):
        try:
            self.voice_clients[ctx.guild.id].pause()
        except Exception as e:
            print(e)

    @commands.command(name="resume")
    async def resume(self, ctx):
        try:
            self.voice_clients[ctx.guild.id].resume()
        except Exception as e:
            print(e)

    @commands.command(name="stop")
    async def stop(self, ctx):
        try:
            self.voice_clients[ctx.guild.id].stop()
            await self.voice_clients[ctx.guild.id].disconnect()
            del self.voice_clients[ctx.guild.id]
        except Exception as e:
            print(e)

    @commands.command(name="queue")
    async def queue(self, ctx, *, url):
        if ctx.guild.id not in self.queues:
            self.queues[ctx.guild.id] = []
        self.queues[ctx.guild.id].append(url)
        await ctx.send("Added to queue!")
    
    @commands.command(name="skip")
    async def skip(self, ctx):
        try:
            self.voice_clients[ctx.guild.id].stop()
            await self.play_next(ctx)
            await ctx.send("Skipped current track!")
        except Exception as e:
            print(e)

async def setup(bot):
    await bot.add_cog(MusicCog(bot))
