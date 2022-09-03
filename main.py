import discord
from discord.ext import commands
from bson.objectid import ObjectId
import arrest
import parties
import server_specific
from MongoDB import collection

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)
muted_individuals = {}
bot.remove_command("help")



@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    # COGS GO HERE
    bot.add_cog(arrest.ArrestAndFree())
    bot.add_cog(parties.PoliticalParty())
    bot.add_cog(server_specific.ServerSpecific())
    roles = [i for i in collection.find({"_id": ObjectId('60a4286ff0d244eb0933c58b')})][0]
    del roles["_id"]
    for user in roles:
        user_roles = roles[user]
        user = await bot.fetch_user(user)
        muted_individuals[user] = []
        for role in user_roles:
            muted_individuals[user].append(role)

@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    channel_house = bot.get_channel(894999095771549717)
    channel_vote = bot.get_channel(payload.channel_id)
    congress_role = discord.utils.get(guild.roles, id=889720149974847488)
    if congress_role not in payload.member.roles:
        if channel_house == channel_vote:
            message = await channel_vote.fetch_message(payload.message_id)
            await message.remove_reaction(payload.emoji, payload.member)


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Bot Commands", description="Here are the commands bröther", color=0x0088ff)
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/529776921307774986/882341269697888267/077b6ad17af77954f66a356536bb37c8.jpg")
    embed.add_field(name="arrest", value="Jails the treasonous scum", inline=False)
    embed.add_field(name="free", value="Frees the untreasonous scum ", inline=False)
    embed.add_field(name="party", value="Joins a Political Party", inline=False)
    # embed.add_field(name="enlist", value="Enlist in the glorious army!", inline=False)
    embed.add_field(name="parties", value="shows all the political subparties", inline=False)
    embed.set_footer(text="For more info ask comrade pepi")
    await ctx.send(embed=embed)


@bot.command()
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("go touch grass retard")
# @bot.command()
# async def test(ctx):
#     category = bot.get_channel(882814870486147113)
#
#     for channel in category.text_channels:
#         await channel.edit(sync_permissions=True)
#         print(f"Fixed {channel.name}")

# @bot.command()
# async def test(ctx):
#     balion = discord.utils.get(ctx.guild.roles, id=720451879854669864)
#     avalon = discord.utils.get(ctx.guild.roles, id=720451879183712307)
#     doulant = discord.utils.get(ctx.guild.roles, id=720451880471494709)
#     deported = discord.utils.get(ctx.guild.roles, id=728293785334841354)
#
#
#     for member in ctx.guild.members:
#         if balion not in member.roles and avalon not in member.roles and deported not in member.roles:
#             await member.add_roles(doulant)
#             print(f"{member.name} was restated")


if __name__ == '__main__':
    bot.run('Nzg1OTU3MDQxMDc1NzgxNjQ0.GnELaw.rOoRdZCKGg5rz-DArmWuUR3m91DWoIWv8ixGF0')
#
# NjMyNTY1MjUxMzA0NDU2MjIy.XaHQTA.soWMtpzY3mjKDgjiwTxQOgStQes