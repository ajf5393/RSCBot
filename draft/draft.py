import discord
import re

from discord.ext import commands

class Draft:
    """Used to draft players onto teams and give the the appropriate roles"""

    CONFIG_COG = None
    TRANS_COG = None

    def __init__(self, bot):
        self.bot = bot
        self.CONFIG_COG = self.bot.get_cog("TransactionConfiguration")
        self.TRANS_COG = self.bot.get_cog("Transactions")

    @commands.command(pass_context=True)
    async def draft(self, ctx, user : discord.Member, teamRole : discord.Role):
        """Assigns the team role and league role to a user when they are drafted and posts to the assigned channel"""
        server_dict = self.CONFIG_COG.get_server_dict(ctx)
        if teamRole in user.roles:
            message = "{0} was kept by the {1}".format(user.mention, teamRole.mention)
        else:
            message = "{0} was drafted by the {1}".format(user.mention, teamRole.mention)
        channel = await self.TRANS_COG.add_player_to_team(ctx, server_dict, user, teamRole, None)
        if channel is not None:
            try:
                free_agent_dict = server_dict.setdefault("Free agent roles", {})
                freeAgentRole = self.TRANS_COG.find_free_agent_role(free_agent_dict, user)
                await self.bot.send_message(channel, message)
                if freeAgentRole is not None:
                    await self.bot.remove_roles(user, freeAgentRole)
                await self.bot.say("Done")
            except KeyError:
                await self.bot.say(":x: Free agent role not found in dictionary")
            except LookupError:
                await self.bot.say(":x: Free agent role not found in server")
            return

def setup(bot):
    bot.add_cog(Draft(bot))