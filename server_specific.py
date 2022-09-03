import discord
import random
from discord.ext import commands
import asyncio
from datetime import timezone, datetime
from main import muted_individuals


reactions = ['👍', '➖', '👎']
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)
class ServerSpecific(commands.Cog):
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member not in muted_individuals:
            role = discord.utils.get(member.guild.roles, id=901688098281373728)
            await member.add_roles(role)
            print("Recognised that a member called " + member.name + " joined")
            state = random.choice(['Balion', 'Doulant', 'Avalon'])
            role = discord.utils.get(member.guild.roles, name=state)
            resident = discord.utils.get(member.guild.roles, name="Resident")
            await member.add_roles(role, resident)
        else:
            role = discord.utils.get(member.guild.roles, id=728293785334841354)
            await member.add_roles(role)

    # @commands.command()
    # async def enlist(self, ctx):
    #     private_role = discord.utils.get(ctx.guild.roles, id=893231306501136384)
    #     await ctx.message.author.add_roles(private_role)
    #     await ctx.send("Welcome in the army, comrade!")


    @commands.command()
    @commands.has_any_role('Speaker of the Senate')
    async def start_vote(self, ctx, *message):
        await ctx.message.delete()
        embed = discord.Embed(title="Vote on this Bill", description=" ".join(message))
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/529776921307774986/792088256748978188/207-2071835_document-icon-png-transparent-png-removebg-preview.png")
        m = await ctx.send(embed=embed)
        for reaction in reactions:
            await m.add_reaction(reaction)

        searched_role = discord.utils.get(ctx.guild.roles, name='Senate')
        ping = await ctx.send(f"{searched_role.mention}")
        await asyncio.sleep(86400)

        without_timezone = datetime.datetime.now()
        x = timezone.localize(without_timezone)
        m = await ctx.fetch_message(m.id)
        counts = {react.emoji: react.count for react in m.reactions}

        result = discord.Embed()
        result.add_field(
            name=f"Called on {x.strftime('%X')} ({x.strftime('%Z')}) of {x.strftime('%A')} {x.strftime('%d')}, {x.strftime('%Y')}",
            value=f"{m.channel}", inline=False)
        result.add_field(name="MOTION TYPE", value="Legislation", inline=False)
        result.add_field(name="CONTENTS",
                         value=f"{' '.join(message)}",
                         inline=False)

        if counts["👍"] > counts["👎"]:
            result.add_field(name="Passes", value=f"{counts['👍'] - 1}-{counts['➖'] - 1}-{counts['👎'] - 1}",
                             inline=False)

        if counts["👍"] == counts["👎"]:
            result.add_field(name="Tied", value=f"{counts['👍'] - 1}-{counts['➖'] - 1}-{counts['👎'] - 1}",
                             inline=False)

        if counts["👍"] < counts["👎"]:
            result.add_field(name="Fails", value=f"{counts['👍'] - 1}-{counts['➖'] - 1}-{counts['👎'] - 1}",
                             inline=False)

        channel = bot.get_channel(770722716507439154)
        president = discord.utils.get(ctx.guild.roles, name='President')
        await channel.send(embed=result)
        await channel.send(f"{president.mention} ")
        await m.delete()
        await ping.delete()
