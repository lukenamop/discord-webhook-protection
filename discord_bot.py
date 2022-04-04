#!/usr/bin/env python3

# import libraries
import asyncio
import discord
import time

# import additional files
import config

# extend the commands.AutoShardedBot class
class DiscordBot(commands.Bot):

	def __init__(self):
		# declare Discord bot intents
		client_intents = discord.Intents(
			guilds=True,
			integrations=True,
			webhooks=True
		)
		# initialize Discord client
		super().__init__(
			command_prefix=commands.when_mentioned,
			case_insensitive=True,
			max_messages=None,
			intents=client_intents,
			member_cache_flags=discord.MemberCacheFlags(voice=False),
			chunk_guilds_at_startup=False
		)
		# remove default help command
		self.remove_command('help')

	def run(self):
		super().run(config.DISCORD_TOKEN, reconnect=True)

	async def build_log_embed(self, color, user, channel, action_str):
		embed = discord.Embed(
			color=color,
			title='Webhook Creation')
		if user is not None:
			embed.add_field(name='Created By', value=f'**{user.name}**#{user.discriminator} (ID {user.id})', inline=False)
		else:
			embed.add_field(name='Created By', value='Unknown', inline=False)
		embed.add_field(name='Channel', value=f'{channel.mention}', inline=False)
		embed.add_field(name='Action', value=action_str, inline=False)
		embed.set_footer(text='Protected by Server Supervisor', icon_url='https://i.imgur.com/xCTOwPj.png')
		return embed

# create an instance of the extended commands.AutoShardedBot class
client = DiscordBot()


##### CLIENT EVENTS #####

# client event triggers when webhooks are updated
@client.event
async def on_webhooks_update(channel):
	if channel.guild.id != config.SERVER_ID:
		return
	
	# check webhook protection status in the server
	if not config.ENABLE_WEBHOOK_PROTECTION:
		return

	# find the server's log channel
	try:
		log_channel_id = config.LOG_CHANNEL_ID
		log_channel = channel.guild.get_channel(log_channel_id)
		if log_channel is None:
			log_channel = await channel.guild.fetch_channel(log_channel_id)
	except:
		print(f'webhook-protection log channel not found')
		return

	try:
		# find the most recently created webhook in the channel
		webhooks = await channel.webhooks()
		if len(webhooks) < 1:
			return
		recent_webhook = webhooks[-1]
	except:
		embed = await client.build_log_embed(0xe74c3c, None, channel, '❌ FAILED TO DELETE - MISSING PERMISSIONS')
		await log_channel.send(embed=embed)
		return

	# only process webhooks created within 120 seconds
	if recent_webhook.created_at.timestamp() < (time.time() - 120):
		return

	# don't process channel follows
	if recent_webhook.type == discord.WebhookType.channel_follower:
		return

	# check to see if the webhook was created by a verified bot
	if config.ALLOW_VERIFIED_BOT_WEBHOOKS:
		if recent_webhook.user.public_flags.verified_bot:
			embed = await client.build_log_embed(0x2ecc71, recent_webhook.user, channel, '✅ Verified bot - no action')
			await log_channel.send(embed=embed)
			return

	# attempt to delete all webhooks
	try:
		await recent_webhook.delete(reason='Webhook protection')
	except:
		embed = await client.build_log_embed(0xe74c3c, recent_webhook.user, channel, '❌ FAILED TO DELETE - MISSING PERMISSIONS')
		await log_channel.send(embed=embed)
		return

	# log the webhook deletion
	embed = await client.build_log_embed(0xf1c40f, recent_webhook.user, channel, '✅ Webhook deleted')
	await log_channel.send(embed=embed)
	return


# client event triggers when discord bot client is fully loaded and ready
@client.event
async def on_ready():
	# change discord bot client presence
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='over your server'))

	# send ready confirmation to command line
	print(f'discord logged in as {client.user.name} - {client.user.id}')
	return


##### CODE TO RUN AT LAUNCH #####

def main():
	print('starting discord bot...')

	# start instance of discord bot client
	client.run()

if __name__ == '__main__':
	main()
