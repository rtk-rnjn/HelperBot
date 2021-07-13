import disocrd
from lib.core import Cog, HelperBot
from discord import Webhook, AsyncWebhookAdapter
from pytchat import LiveChatAsync
from datetime import datetime

class OnReady(Cog):
	def __init__(self, bot: HelperBot):
		self.bot = bot

	async def main(self):
		livechat = LiveChatAsync("uIx8l2xlYVY", callback = self.func)
		while livechat.is_alive():
			await asyncio.sleep(1.5)
	
	async def func(self, chatdata):
		for c in chatdata.items:
			color = discord.Colour.default()
			footer = "Normal User"
			if c.author.isChatModerator: 
				color = discord.Colour.blue()
				footer = "Chat Moderator"
			if c.author.isCharOwner: 
				color = discord.Colour.orange()
				footer = "Chat Owner"
			date_obj = datetime.strptime(c.datetime, "%Y-%m-%d %H:%M:%S")
			embed = discord.Embed( 
						description=f"```\n{c.message}\n```", 
						color=color, 
						timestamp=date_obj
					)
			embed.set_author(name=f"{c.author.name}", url=c.author.channelUrl)
			embed.set_thumbnail(url=c.author.imageUrl)
			embed.set_footer(text=footer)
			for hook in ['https://discord.com/api/webhooks/864089656701485066/4FSi8EfR3WzwY729i2_bm8QF8SVfoEpukcMZAsg_yJcE9H5sHLeU6lZHxlMCBoYAjdpU', 'https://discord.com/api/webhooks/864089652410318850/l9A8JqNXqTZrWDkkm5ow9kKGUf3gDc_Sp7POw96tSWFrdV3zDV_6421uZVjTsPXD9XfL']
				async def send_webhook():
					async with aiohttp.ClientSession() as session:
						webhook = Webhook.from_url(hook, adapter=AsyncWebhookAdapter(session))
					try:
						await webhook.send(embed=embed)
						break
					except Exception:
						pass
	
	@Cog.listener()
	async def on_ready(self):
		await self.main()

def setup(bot):
	bot.add_cog(OnReady(bot))