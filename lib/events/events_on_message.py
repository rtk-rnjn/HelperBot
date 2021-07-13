import discord
from core import Cog, HelperBot


class OnMessage(Cog):
	def __init__(self, bot: HelperBot):
		self.bot = bot

	@Cog.listener()
	async def on_message(self, message):
		if not message.guild or message.author.bot: return
		
		channel = discord.utils.get(message.guild.channels, name='mod-mail')
		
		if str(message.channel.type) == 'private':
			await channel.send(f"**{message.author.name}#{message.author.discriminator} ({message.author.id})** {message.content}")
		
		if message.channel is channel:
			if str(message.content).startswith('<'):
				user = message.mentions[0]
				await user.send(f"**{message.author.name}#{message.author.discriminator}** {message.content}")

def setup(bot):
	bot.add_cog(OnMessage(bot))