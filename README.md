# Webhook Protection
This is a standalone version of [Server Supervisor](https://discord-security.gitbook.io/server-supervisor/)'s Webhook Protection feature.

# Installation
1. This bot uses the Pycord library (https://github.com/Pycord-Development/pycord) to communicate with the Discord API. Follow Pycord's instructions for installation on your system.
2. You'll need to create an application at https://discord.com/developers/applications, then create a bot inside your application.
3. After you've created the bot, you can get a link to add it to your server in the OAuth2 -> URL Generator by selecting "bot" and then "Administrator" and copying the link.
4. Download this repository to your system, update the `DISCORD_TOKEN` and `LOG_CHANNEL_ID` variables in `config.py`, and use `python3 discord_bot.py` to start the bot.

If you need help, feel free to reach out at https://twitter.com/lukenamop.
