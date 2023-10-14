import discord
import json

from . import add_user_candy

class Vibrate(discord.ui.View):

    def __init__(self, websocket):
        super().__init__()

        self.user_list = []
        self.websocket = websocket

    @discord.ui.button(label="Steal a candy", style=discord.ButtonStyle.green,
        emoji=discord.PartialEmoji.from_str("<:candy:1162847068864401418>"))
    async def claim_vibrate(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user.id in self.user_list:
            return await interaction.response.send_message("You already claimed this candy", ephemeral=True)

        self.user_list.append(interaction.user.id)

        add_user_candy(interaction.user.id)

        await interaction.response.send_message("Candy claimed!", ephemeral=True)

        await self.websocket.send(json.dumps({"type":"vibe", "value":15}))

    async def cancel(self):
        if self.websocket:
            await self.websocket.close()
            self.websocket = None

class RemoteControl(discord.ui.View):

    def __init__(self, link):
        super().__init__()

        self.link = link

        self.activated = True

    @discord.ui.button(label="Steal the remote", style=discord.ButtonStyle.red,
        emoji=discord.PartialEmoji.from_str("<:smug:1162855875908730910>"))
    async def claim_vibrate(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.activated:
            return await interaction.response.send_message("Sadly, the remote was already stolen by someone else", ephemeral=True)

        self.activated = False

        add_user_candy(interaction.user.id)

        embed = discord.Embed(title="You managed to get the remote!",
            description="You managed to steal the remote from the monster! Quick, go on this link to being able to control everyone!")

        view = discord.ui.View()

        view.add_item(discord.ui.Button(style=discord.ButtonStyle.url, label="Control the remote", url=self.link))

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        await interaction.message.edit(view=None)