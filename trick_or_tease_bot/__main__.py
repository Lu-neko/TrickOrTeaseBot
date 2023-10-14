import os
from . import client

from .config_commands import config
from .commands import connect, leaderboard, rank

client.tree.add_command(config)

client.tree.add_command(connect)
client.tree.add_command(leaderboard)
client.tree.add_command(rank)

client.run(os.getenv("DISCORD_TOKEN"))