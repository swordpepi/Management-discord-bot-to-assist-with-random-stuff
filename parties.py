import discord
from bson.objectid import ObjectId
from discord.ext import commands
from pymongo import MongoClient
import ssl

cluster = MongoClient("mongodb+srv://Chinggis:Goshonia@cluster0.hmojs.mongodb.net/test", ssl_cert_reqs=ssl.CERT_NONE)
db = cluster["UserData"]
collection = db["UserData"]
class PoliticalParty(commands.Cog):
    def __init__(self):
        self.parties = [i for i in collection.find({"_id": ObjectId('600ef237c6b028476dcb67b0')})][0]
        del self.parties["_id"]

    @commands.command()
    @commands.has_any_role('Administrator')
    async def party_create(self, ctx, *party_name):
        party_name = " ".join(party_name)
        if discord.utils.get(ctx.guild.roles, name=party_name) and party_name in self.parties['parties']:
            await ctx.send("Role already exists")  # if party exists and is in list

        elif discord.utils.get(ctx.guild.roles, name=party_name):  # if party exists
            self.parties['parties'].append(party_name)
            await ctx.send("Party added.")
            collection.replace_one({'_id': ObjectId('600ef237c6b028476dcb67b0')}, self.parties)


        else:  # if party does not exist
            self.parties['parties'].append(party_name)
            await ctx.guild.create_role(name=party_name)
            await ctx.send("Party added.")
            collection.replace_one({'_id': ObjectId('600ef237c6b028476dcb67b0')}, self.parties)

    @commands.command()
    @commands.has_any_role('Administrator')
    async def party_delete(self, ctx, *party_name):
        party_name = " ".join(party_name)
        if party_name in self.parties['parties']:
            self.parties['parties'].remove(party_name)
            role = discord.utils.get(ctx.message.guild.roles, name=party_name)
            collection.replace_one({'_id': ObjectId('600ef237c6b028476dcb67b0')}, self.parties)
            await role.delete()
            await ctx.send("Party deleted.")
        else:
            await ctx.send("Party does not exist")

    @commands.command()
    async def parties(self, ctx):
        try:
            if self.parties['parties']:
                embed = discord.Embed(title="Parties", description="Here are the server parties:", color=0x04ff00)
                for party in self.parties['parties']:
                    role = discord.utils.get(ctx.message.guild.roles, name=party)
                    embed.add_field(name=party, value=str(len(role.members)))
                embed.set_footer(text='To join a party type !party + "desired party"')
                await ctx.send(embed=embed)
            else:
                await ctx.send("No parties detected")
        except(AttributeError):
            await ctx.send("Party role missing | Contact an admin to resolve this issue")


    @commands.command()
    async def party(self, ctx, *party_name):
        party_name = " ".join(party_name)
        member = ctx.message.author
        role = discord.utils.get(ctx.message.guild.roles, name=party_name)
        if role in member.roles and party_name in self.parties['parties']:  # removes party role
            await member.remove_roles(role)
            await ctx.send("You have left the party")

        elif party_name in self.parties['parties']:  # adds party role
            await member.add_roles(role)
            await ctx.send("There you go, comrade!")

        elif party_name not in self.parties['parties']:
            await ctx.send("Party not detected")