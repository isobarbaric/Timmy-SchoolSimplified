import asyncio
import datetime
import json
import logging
from datetime import datetime, timedelta

import discord
from core import database
from core.checks import is_botAdmin
from discord.ext import commands
from redbot.core.utils.tunnel import Tunnel
from gtts import gTTS

class SkeletonCMD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.interaction = []
        


    @commands.command(name="interact")
    @is_botAdmin
    async def _interact(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """Start receiving and sending messages as the bot through DM"""
        await ctx.message.delete()

        NE = database.AdminLogging.create(discordID = ctx.author.id, action = "INTERACT")
        NE.save()

        u = ctx.author
        if channel is None:
            if isinstance(ctx.channel, discord.DMChannel):
                await ctx.send(
                    (
                        "You need to give a channel to enable this in DM. You can "
                        "give the channel ID too."
                    )
                )
                return
            else:
                channel = ctx.channel

        if u in self.interaction:
            await ctx.send("A session is already running.")
            return

        message = await u.send(
            (
                "I will start sending you messages from {0}.\n"
                "Just send me any message and I will send it in that channel.\n"
                "React with ❌ on this message to end the session.\n"
                "If no message was send or received in the last 5 minutes, "
                "the request will time out and stop."
            ).format(channel.mention)
        )
        await message.add_reaction("❌")
        self.interaction.append(u)

        while True:

            if u not in self.interaction:
                return

            try:
                message = await self.bot.wait_for("message", timeout=300)
            except asyncio.TimeoutError:
                await u.send("Request timed out. Session closed")
                self.interaction.remove(u)
                return

            if message.author == u and isinstance(message.channel, discord.DMChannel):
                files = await Tunnel.files_from_attatch(message)

                await channel.send(message.content, files=files)
            elif (
                message.channel != channel
                or message.author == channel.guild.me
                or message.author == u
            ):
                pass

            else:
                embed = discord.Embed()
                embed.set_author(
                    name="{} | {}".format(str(message.author), message.author.id),
                    icon_url=message.author.avatar_url,
                )
                embed.set_footer(text=message.created_at.strftime("%d %b %Y %H:%M"))
                embed.description = message.content
                embed.colour = message.author.color

                if message.attachments != []:
                    embed.set_image(url=message.attachments[0].url)

                await u.send(embed=embed)


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user in self.interaction:
            channel = reaction.message.channel
            if isinstance(channel, discord.DMChannel):
                await self.stop_interaction(user)


    async def stop_interaction(self, user):
        self.interaction.remove(user)
        await user.send("Session closed")


    @commands.command()
    @is_botAdmin
    async def say(self, ctx, *, message):
        NE = database.AdminLogging.create(discordID = ctx.author.id, action = "SAY", content = message)
        NE.save()

        await ctx.message.delete()
        await ctx.send(message)

    @commands.command()
    @is_botAdmin
    async def sayvc(self, ctx, *, text=None):
        NE = database.AdminLogging.create(discordID = ctx.author.id, action = "SAYVC", content = text)
        NE.save()
        
        await ctx.message.delete()

        if not text:
            # We have nothing to speak
            await ctx.send(f"Hey {ctx.author.mention}, I need to know what to say please.")
            return

        vc = ctx.voice_client # We use it more then once, so make it an easy variable
        if not vc:
            # We are not currently in a voice channel
            await ctx.send("I need to be in a voice channel to do this, please use the connect command.")
            return

        # Lets prepare our text, and then save the audio file
        tts = gTTS(text=text, lang="en")
        tts.save("text.mp3")

        try:
            # Lets play that mp3 file in the voice channel
            vc.play(discord.FFmpegPCMAudio('text.mp3'), after=lambda e: print(f"Finished playing: {e}"))

            # Lets set the volume to 1
            vc.source = discord.PCMVolumeTransformer(vc.source)
            vc.source.volume = 1

        # Handle the exceptions that can occur
        except discord.ClientException as e:
            await ctx.send(f"A client exception occured:\n`{e}`")

        except TypeError as e:
            await ctx.send(f"TypeError exception:\n`{e}`")

def setup(bot):
    bot.add_cog(SkeletonCMD(bot))



    