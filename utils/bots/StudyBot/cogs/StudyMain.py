from datetime import datetime, timedelta

import discord
import pytz
from core import database
from core.common import hexColors
from core.common import TECH_ID
from discord.ext import commands


time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
EST = pytz.timezone("US/Eastern")


def convert_time_to_seconds(time):
    try:
        value = int(time[:-1]) * time_convert[time[-1]]
    except:
        value = time
    finally:
        if value < 60:
            return None
        else:
            return value


def showFutureTime(time):
    now = datetime.now(EST)
    output = convert_time_to_seconds(time)
    if output is None:
        return None

    add = timedelta(seconds=int(output))
    now_plus_10 = now + add

    return now_plus_10.strftime(r"%I:%M %p")


def showTotalMinutes(dateObj: datetime):
    now = datetime.now(EST)
    dateObj = pytz.timezone("America/New_York").localize(dateObj)

    deltaTime = now - dateObj

    totalmin = deltaTime.total_seconds() // 60

    return totalmin, now


def _getXPForNextLvl(lvl: int):
    """
    Get the XP the user needs to reach the next level.

    :param lvl: The current level of the user.

    :return: The XP: int
    """

    xpNeeded = (5 * lvl * lvl) + (50 * lvl) + 100

    return xpNeeded


async def addLeaderboardProgress(member: discord.Member):
    """
    Updates the data in the database table `StudyVCLeaderboard` of a specific member and adds level roles to the member if needed.

    :param member: The member on which the progress should apply on.

    :return: Whenever the user has been found in the database: bool
    """
    xpPerMinute = 30

    StudySessionQ = database.StudyVCDB.select().where(database.StudyVCDB.discordID == member.id)
    if StudySessionQ.exists():
        StudySessionQ = StudySessionQ.get()
        totalmin, now = showTotalMinutes(StudySessionQ.StartTime)
        leaderboardQuery = database.StudyVCLeaderboard.select().where(database.StudyVCLeaderboard.discordID == member.id)

        isNewLvl = False
        if leaderboardQuery.exists():
            leaderboardQuery = leaderboardQuery.get()
            leaderboardQuery.TTS = totalmin + leaderboardQuery.TTS
            leaderboardQuery.TTSWeek = totalmin + leaderboardQuery.TTSWeek
            leaderboardQuery.totalSessions = leaderboardQuery.totalSessions + 1

            currentLvl = leaderboardQuery.level
            currentXP = leaderboardQuery.xp
            currentTotalXP = leaderboardQuery.totalXP

            xpNeeded = _getXPForNextLvl(currentLvl)
            xpEarned = totalmin * xpPerMinute

            newXP = currentXP + xpEarned
            newTotalXP = currentTotalXP + xpEarned
            newLvl = currentLvl

            if newXP >= xpNeeded:

                isNewLvl = True
                newXPNeeded = xpNeeded
                while newXP >= newXPNeeded:
                    newXP -= newXPNeeded
                    newLvl += 1
                    newXPNeeded = _getXPForNextLvl(newLvl)

            leaderboardQuery.xp = newXP
            leaderboardQuery.totalXP = newTotalXP
            leaderboardQuery.level = newLvl

            leaderboardQuery.save()

        else:
            currentLvl = 0
            currentXP = 0
            currentTotalXP = 0

            xpNeeded = _getXPForNextLvl(currentLvl)
            xpEarned = totalmin * xpPerMinute

            newXP = currentXP + xpEarned
            newTotalXP = currentTotalXP + xpEarned
            newLvl = currentLvl

            if newXP >= xpNeeded:

                isNewLvl = True
                newXPNeeded = xpNeeded
                while newXP >= newXPNeeded:
                    newXP -= newXPNeeded
                    newLvl += 1
                    newXPNeeded = _getXPForNextLvl(newLvl)

            q = database.StudyVCLeaderboard.create(
                discordID=member.id,
                TTS=totalmin,
                totalSessions=0,
                xp=newXP,
                totalXP=newTotalXP,
                level=newLvl,
                TTSWeek=totalmin
            )
            q.save()

        roleStr = ""
        if newLvl < 5:
            pass

        elif newLvl < 10:
            role = None  # TODO: get lvl 5 role and add to user

            if currentLvl < 5:
                roleStr = f"\nYou've earned a new role: {role}"
            pass

        elif newLvl < 20:
            role = None  # TODO: get lvl 10 role and add to user

            if currentLvl < 10:
                roleStr = f"\nYou've earned a new role: {role}"
            pass

        elif newLvl < 30:
            role = None  # TODO: get lvl 20 role and add to user

            if currentLvl < 20:
                roleStr = f"\nYou've earned a new role: {role}"
            pass

        elif newLvl < 40:
            role = None  # TODO: get lvl 30 role and add to user

            if currentLvl < 30:
                roleStr = f"\nYou've earned a new role: {role}"
            pass

        elif newLvl < 50:
            role = None  # TODO: get lvl 40 role and add to user

            if currentLvl < 40:
                roleStr = f"\nYou've earned a new role: {role}"
            pass

        elif newLvl < 60:
            role = None  # TODO: get lvl 50 role and add to user

            if currentLvl < 50:
                roleStr = f"\nYou've earned a new role: {role}"
            pass

        elif newLvl < 70:
            role = None  # TODO: get lvl 60 role and add to user

            if currentLvl < 60:
                roleStr = f"\nYou've earned a new role: {role}"
            pass

        elif newLvl < 80:
            role = None  # TODO: get lvl 70 role and add to user

            if currentLvl < 70:
                roleStr = f"\nYou've earned a new role: {role}"
            pass

        elif newLvl < 90:
            role = None  # TODO: get lvl 80 role and add to user

            if currentLvl < 80:
                roleStr = f"\nYou've earned a new role: {role}"
            pass

        elif newLvl < 100:
            role = None  # TODO: get lvl 90 role and add to user

            if currentLvl < 90:
                roleStr = f"\nYou've earned a new role: {role}"
            pass

        elif newLvl >= 100:
            role = None  # TODO: get lvl 100 role and add to user

            if currentLvl < 100:
                roleStr = f"\nYou've earned a new role: {role}"
            pass

        if isNewLvl:

            dmMSG = f"{member.mention}, you've reached level **{newLvl}** in Study VC!" \
                    f"{roleStr}"
            try:
                await member.send(dmMSG)
            except:
                pass

    else:
        return False

    StudySessionQ = StudySessionQ.get()
    StudySessionQ.StartTime = datetime.now(EST)
    StudySessionQ.Paused = True
    StudySessionQ.save()

    return True


async def endSession(member: discord.Member):
    """
    Ends the session by kicking the user out of the voice channel and removing the user from the database table `StudyVCDB`.

    :param member: The member which should get removed from the database.

    :return: Whenever the user has been found in the database: bool
    """

    StudySessionQ = database.StudyVCDB.select().where(database.StudyVCDB.discordID == member.id)
    if StudySessionQ.exists():
        StudySessionQ = StudySessionQ.get()
        StudySessionQ.delete_instance()
        StudySessionQ.save()

        if member.voice:
            await member.move_to(None)

    else:
        return False

    return True


class StudyToDo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.StudyVCGuildID = TECH_ID.g_tech


    @commands.group(aliaseS=["study-todo"])
    async def studytodo(self, ctx: commands.Context):
        if ctx.message.content == "+studytodo":
            subcommands = "/".join(
                sorted(subcommand.name for subcommand in self.studytodo.commands)
            )
            signature = f"{ctx.prefix}{ctx.command.qualified_name} <{subcommands}>"

            embed = discord.Embed(
                color=hexColors.red_error,
                title="Missing/Extra Required Arguments Passed In!",
                description=f"You have missed one or several arguments in this command"
                f"\n\nUsage:"
                f"\n`{signature}`",
            )
            embed.set_footer(
                text="Consult the Help Command if you are having trouble or call over a Bot Manager!"
            )
            await ctx.send(embed=embed)

    @studytodo.command()
    async def set(self, ctx: commands.Context, *, item):
        """
        Adds an item to the study to-do list of the author/owner.
        """

        query: database.StudyVCDB = database.StudyVCDB.select().where(database.StudyVCDB.discordID==ctx.author.id)
        if query.exists():
            query = query.get()
            query.studyTodo = item
            query.save()
            embed = discord.Embed(
                title="Successfully Added Item!",
                description=f"`{item}` has been added successfully with the id `{str(query.id)}`.",
                color=hexColors.green_confirm,
            )
            embed.set_footer(text="StudyBot")
            await ctx.send(embed=embed)
        else:
            return await ctx.send(f"You don't have a study session yet! Make one by joining any StudyVC!")


    @studytodo.command()
    async def end(self, ctx: commands.Context):
        """
        Removes an item from the study to-do list of the author/owner.
        """
        console: discord.TextChannel = await self.bot.fetch_channel(954516809577533530)

        isInDatabase = await addLeaderboardProgress(ctx.author)

        if isInDatabase:
            if ctx.author.voice:
                await endSession(ctx.author)
                await ctx.send(f"{ctx.author.mention} Your study session ended. To make one again, join any StudyVC!")

        else:
            await ctx.send(f"You don't have a study session yet! Make one by joining any StudyVC!")


    @studytodo.command()
    async def list(self, ctx):
        query = database.StudyToDo.select().where(
            database.StudyToDo.discordID == ctx.author.id
        )
        if query.exists():
            query = query.get()
            embed = discord.Embed(
                title="Study To-Do List",
                description=f"Your current goal: {query.studyTodo}",
                color=hexColors.blue_main,
            )
            embed.set_footer(
                text="You can use +studytodo set (item) to modify this!"
            )
            await ctx.send(embed=embed)

        else:
            return await ctx.send(f"You don't have a study session yet! Make one by joining any StudyVC!")
    
    @studytodo.command(aliases=["lb"])
    async def leaderboard(self, ctx):
        lb = []

        for entry in database.StudyVCLeaderboard.select().order_by(database.StudyVCLeaderboard.totalXP.desc(),
                                                                   database.StudyVCLeaderboard.xp.desc()):
            i = 1
            totalmin = entry.TTS
            if totalmin > 60:
                totalmin = totalmin // 60
                totalmin = f"{totalmin} hour(s)"
            else:
                totalmin = f"{totalmin} minute(s)"
            user = await self.bot.fetch_user(entry.discordID)
            lb.append(f"{str(i)}. {user.name} -> {totalmin}")
            i += 1

        FormattedList = "\n".join(lb)
        embed = discord.Embed(
            title="Study Leaderboard",
            description=f"```\n{FormattedList}\n```",
            color=hexColors.ss_blurple,
        )
        embed.set_footer(
            text="StudyBot"
        )
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(StudyToDo(bot))
