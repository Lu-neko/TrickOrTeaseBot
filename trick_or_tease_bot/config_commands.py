import discord
from discord import app_commands
import random
import json

from . import config as configuration

def save_config():
    with open("config.json", "w") as file:
        json.dump(configuration, file)

config = app_commands.Group(name="config", description="Configure the bot", guild_only=True,
    default_permissions=discord.Permissions(administrator=True))

@config.command(description="Enable the bot")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(enabled="If you want to enable the bot or not")
async def set_enable(interaction: discord.Interaction, enabled: bool):
    if enabled and not interaction.client.channel:
        return await interaction.response.send_message("You can't enable the bot before configuring the channel", ephemeral=True)

    interaction.client.enabled = enabled
    await interaction.response.send_message(f"The bot has been {'enabled' if enabled else 'disabled'}", ephemeral=True)
    save_config()

@config.command(description="Set the chance for a rare monster to appear")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(chance="The probability for the monster to be rare (between 0.0 and 1.0)")
async def set_chance(interaction: discord.Interaction, chance: float):
    if 0 <= chance <= 1:
        interaction.client.rare_chance = chance
        configuration["rare_chance"] = chance
        await interaction.response.send_message("Chance set!", ephemeral=True)
        return save_config()
    await interaction.response.send_message("The chance probability should be between 0.0 and 1.0", ephemeral=True)

@config.command(description="Set the channel for the bot to send message")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(channel="The channel for the bot to send messages into")
async def set_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    interaction.client.channel = channel
    configuration["channel"] = str(channel.id)
    await interaction.response.send_message("Channel set!", ephemeral=True)
    save_config()

@config.command(description="Define the time between messages, in minutes")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(min="The minimum time (in minutes)", max="The maximum time (in minutes)")
async def set_timing(interaction: discord.Interaction, min: int, max: int):
    if 0 <= min <= max and max != 0:
        interaction.client.min_timing = min
        configuration["min_timing"] = min
        interaction.client.max_timing = max
        configuration["max_timing"] = max
        interaction.client.current = random.randint(min*60, max*60)

        await interaction.response.send_message("Timing set!", ephemeral=True)
        return save_config()
    
    await interaction.response.send_message("Invalid time value", ephemeral=True)