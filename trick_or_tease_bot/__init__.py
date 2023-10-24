import discord
from discord import app_commands
from discord.ext import tasks
import os
import websockets
import dotenv
import aiohttp
import random
import json

with open("candies.json") as file:
    users_candies = json.load(file)

with open("config.json") as file:
    config = json.load(file)

def add_user_candy(user_id):
    users_candies[str(user_id)] = users_candies.get(str(user_id), 0)+1

from .views import Vibrate, RemoteControl

dotenv.load_dotenv()

GUILD = discord.Object(id=os.getenv("GUILD"))
TOKEN = os.getenv("TOKEN")
SERVER = os.getenv("SERVER")

monsters = {"common":{}, "rare":{}}

for root, dirs, files in os.walk("monsters"):
    if files:
        _, category, monster = root.split("/")
        monsters[category][monster] = files

class TrickTeaseBot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.enabled = False
        self.channel = None
        self.min_timing = config.get("min_timing", 5)
        self.max_timing = config.get("max_timing", 10)
        self.rare_chance = config.get("rare_chance", 0.2)
        self.current = 0

        self.current_view = None
        self.current_message = None

    async def on_ready(self):
        if config.get("channel"):
            self.channel = client.get_channel(int(config.get("channel")))
        self.verify_time.start()
        self.save_candies.start()
        self.session = aiohttp.ClientSession()
        print(f"Logged in as {client.user}")

    async def cancel_previous(self):
        if self.current_view:
            await self.current_view.cancel()
            self.current_view = None

        if self.current_message:
            await self.current_message.edit(view=None)

    async def send_monster(self):
        async with client.session.post(f"https://{SERVER}/api/genToken", json={"token": TOKEN}) as r:
            result = await r.json()
        
        generated_token = result["token"]

        if random.random() >= self.rare_chance:
            start_path = "common"
            socket = await websockets.connect(f"wss://{SERVER}/vibe/{generated_token}")

            self.current_view = view = Vibrate(socket)

            embed = discord.Embed(color=4579838, title="A monster appeared!", description="A new monster appeared "+
                "in the channel, click the button under to steal a candy from the monster and vibrate everyone!")
        else:
            start_path = "rare"

            view = RemoteControl(f"https://{SERVER}/control/{generated_token}")

            embed = discord.Embed(color=4579838, title="A *Rare* monster appeared!", description="A rare monster appeared! "+
                "They have the remote of everyone connected on them, be the first one to steal them to be able to control everyone!")

        monster_type = random.choice([*monsters[start_path]])

        monster = random.choice(monsters[start_path][monster_type])

        file = discord.File(f"monsters/{start_path}/{monster_type}/{monster}", filename="monster.png")

        embed.set_image(url="attachment://monster.png")

        self.current_message = await self.channel.send(embed=embed, view=view, file=file)

    @tasks.loop(seconds=5.0)
    async def verify_time(self):
        if not self.enabled:
            return

        self.current -= 5
        if self.current < 0:
            self.current = random.randint(self.min_timing*60, self.max_timing*60)

            await self.cancel_previous()
            await self.send_monster()

    @tasks.loop(minutes=10)
    async def save_candies(self):
        with open("candies.json", "w") as file:
            json.dump(users_candies, file)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)

    async def close(self):

        with open("candies.json", "w") as file:
            json.dump(users_candies, file)

        await client.session.post(f"https://{SERVER}/api/genToken", json={"token": TOKEN})

        await self.cancel_previous()

        await self.session.close()
        await super().close()

intents = discord.Intents.default()
client = TrickTeaseBot(intents=intents)