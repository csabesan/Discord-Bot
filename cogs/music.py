import discord
from discord import app_commands
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

    async def play_next(self, interaction):
        if self.queues.get(interaction.guild.id):
            link = self.queues[interaction.guild.id].pop(0)
            await self.play(interaction, link=link)
    
    @app_commands.command(name='play', description="Play a song")
    @app_commands.describe(link="Enter the YouTube URL or song title")
    async def play(self, interaction: discord.Interaction, link: str):
        await interaction.response.defer()
        voice_client = self.voice_clients.get(interaction.guild.id)

        if not voice_client or not voice_client.is_connected():
            if interaction.user.voice and interaction.user.voice.channel:
                try:
                    voice_client = await interaction.user.voice.channel.connect()
                    self.voice_clients[interaction.guild.id] = voice_client
                except Exception as e:
                    print(f"Failed to connect to voice channel: {e}")
                    return
            else:
                await interaction.followup.send("You are not connected to a voice channel.")
                return
        
        try:
            if "www.youtube.com" not in link:
                query_string = urllib.parse.urlencode({'search_query': link})
                content = urllib.request.urlopen(self.youtube_results_url + query_string)
                search_results = re.findall(r'/watch\?v=(.{11})', content.read().decode())
                link = self.youtube_watch_url + search_results[0]
            
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(link, download=False))

            song = data['url']
            songURL = data.get('original_url')
            song_title = data.get('title')
            duration = data.get('duration_string')

            player = discord.FFmpegOpusAudio(song, **self.ffmpeg_options)
            voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(interaction), self.bot.loop))
        except Exception as e:
            print(f"Error during playback: {e}")
            return
            
        def time_string_to_seconds(time_str):
                minutes, seconds = map(int, time_str.split(':'))
                total_seconds = minutes * 60 + seconds
                return total_seconds
        
        embed_message = discord.Embed(colour=discord.Colour.purple(),
                                      description=f"**Now Playing: **\n{song_title}\n\nYouTube URL: {songURL}")
        embed_message.set_author(name=f'Requested by: {interaction.user.name}', icon_url=interaction.user.display_avatar)
        embed_message.set_footer(text=f'Song Duration: {duration}')
        followup_message = await interaction.followup.send(embed=embed_message)
        await asyncio.sleep(time_string_to_seconds(duration) + 5)
        await followup_message.delete()
    
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
