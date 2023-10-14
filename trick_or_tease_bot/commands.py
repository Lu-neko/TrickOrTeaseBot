import discord
from discord import app_commands
import heapq

from . import client, users_candies

@discord.app_commands.command(description="Connect your toys")
async def connect(interaction: discord.Interaction):
    async with interaction.client.session.get("http://localhost:5000/api/get_qrcode", params={"user_id": interaction.user.id}) as r:
        result = await r.json()

    embed = discord.Embed(color=4579838, title="Connect your toy")
    embed.set_image(url=result["url"])
    embed.set_footer(text="This link will expire in 10 minutes.")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@discord.app_commands.command(description="Show the leaderboard")
async def leaderboard(interaction: discord.Interaction):
    top = heapq.nlargest(10, users_candies.items(), key=(lambda x:x[1]))

    description = []

    for i in range(len(top)):
        user, score = top[i]
        description.append(f"{i+1}. <@{user}> : {score}")

    embed = discord.Embed(color=4579838, title="Leaderboard", description="\n".join(description))

    await interaction.response.send_message(embed=embed)

@discord.app_commands.command(description="Show your rank")
async def rank(interaction: discord.Interaction):

    user_id = str(interaction.user.id)

    if not user_id in users_candies:
        return await interaction.response.send_message("You are not in the leaderboard")

    place = sorted(users_candies, key=(lambda x: users_candies[x]), reverse=True).index(user_id)

    embed = discord.Embed(color=4579838, title="Rank",
        description=f"You are rank {place+1} on the leaderboard with {users_candies[user_id]} candies.")
    embed.set_thumbnail(url=interaction.user.display_avatar.url)

    await interaction.response.send_message(embed=embed)
