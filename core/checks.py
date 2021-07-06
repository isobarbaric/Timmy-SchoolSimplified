'''
SETUP:

If you require a specific command to be protected, you can use the built in @is_botAdmin check or create your own one here!

If you wish to use the @is_botAdmin check, DM Space.".

Otherwise, use the same format to make your own check. 
'''

from discord.ext import commands
from core import database




def predicate_LV1(ctx):
    adminIDs = []

    query = database.Administrators.select().where(database.Administrators.TierLevel >= 1)
    for admin in query:
        adminIDs.append(admin.discordID)

    return ctx.author.id in adminIDs

is_botAdmin = commands.check(predicate_LV1)



def predicate_LV2(ctx):
    adminIDs = []

    query = database.Administrators.select().where(database.Administrators.TierLevel >= 2)
    for admin in query:
        adminIDs.append(admin.discordID)

    return ctx.author.id in adminIDs

is_botAdmin2 = commands.check(predicate_LV2)



def predicate_LV3(ctx):
    adminIDs = []

    query = database.Administrators.select().where(database.Administrators.TierLevel >= 3)
    for admin in query:
        adminIDs.append(admin.discordID)

    return ctx.author.id in adminIDs

is_botAdmin3 = commands.check(predicate_LV3)