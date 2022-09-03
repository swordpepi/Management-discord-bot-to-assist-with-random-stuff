import discord as discord
from discord.ext import commands

from MongoDB import muted_individuals, save


class ArrestAndFree(commands.Cog):
    @commands.command()
    @commands.has_role('Handcuffs (Arrest Perms)')  # NOTE: Add mod role here. Can also make a special mod list
    async def arrest(self, ctx, member: discord.Member):
        if ctx.message.author == member:
            await ctx.send("self harm is not allowed smh")
        else:
            muted_role = discord.utils.get(member.guild.roles, name='Arrested (Muted)')
            if member is None:
                await ctx.send("Pass a valid user bitte")
                return
            roles = [role for role in member.roles if role.name != '@everyone']
            muted_individuals[member] = roles
            try:
                await member.remove_roles(*roles)
            finally:
                await member.add_roles(muted_role)
                await ctx.send(
                    f"{member.mention}\nhttps://tenor.com/view/hornyjail-bonk-baseballbat-kitty-cat-gif-19401897")
            save()

    @arrest.error
    async def jail_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send("https://tenor.com/view/access-denied-warhammer40k-gif-18486442")


    @commands.command()
    @commands.has_any_role('Handcuffs (Arrest Perms)')
    async def free(self, ctx, member: discord.Member):  # muted role can be gotten from outside
        if member is None or member not in muted_individuals:
            await ctx.send("Pass a valid user bitte")
            return
        muted_role = discord.utils.get(member.guild.roles, name='Arrested (Muted)')
        prev_roles = muted_individuals[member]
        muted_individuals.pop(member)

        await member.remove_roles(muted_role)
        try:
            await member.add_roles(*prev_roles)
        finally:
            await ctx.send(f"{member.mention} has been freed from hell")
            save()

    @free.error
    async def free_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send("https://tenor.com/view/access-denied-warhammer40k-gif-18486442")


    @commands.command()
    @commands.has_any_role('Handcuffs (Arrest Perms)')
    async def clear(self, ctx, *person):
        person = " ".join(person)
        for member in muted_individuals:
            if member.name == person:
                muted_individuals.pop(member)
                await ctx.send("Member cleared")
                person = ""
        if person != "":
            await ctx.send("That dude ain't in jail lmao")
        save()

    @free.error
    async def free_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send("https://tenor.com/view/access-denied-warhammer40k-gif-18486442")

    @commands.command()
    async def show_jail(self, ctx):
        if muted_individuals:
            jail_list = [member.display_name for member in muted_individuals]
            embed = discord.Embed(title="The Gulag", color=0x0088ff)
            embed.add_field(name="Here are the traitors comrade", value="\n".join(jail_list), inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Blin where is all the crime")