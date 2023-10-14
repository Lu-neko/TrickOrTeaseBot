# Trick or Tease Discord Bot

![Project Image](trick_tease_pfp.png)

The Trick or Tease Bot was a project created for the Lovense Dev Halloween Event.

The Trick or Tease Bot is a Halloween Themed Discord Bot that posts monsters into a specified channel on Discord and allows users to react to the message to collect candy.

The Bot also is Lovense integrated allowing for Lovense toys to vibrate when users collect candies.

The Trick or Tease bot has 2 categories of monsters: common and rare.
- The common monsters allow all users who react to collect candy and each candy collection produces toy vibrations whereas the rare monsters allow for only one user to react.
- Once a user reacts to a rare monster they are redirected to a website that they can use to control all the connected Lovense toys for as long as it takes for the next monster to appear.

The bot allows users to use leaderboard related commands to check how they compare to others with how many candies they have collected, the use of these commands can be restricted to specific channels using Discord's own features. 

## Commands

Configuration Commands (Admin needed)

```
/config set_channel channel: - allows admins to select the channel the bot sends monster messages in
/config set_timing min: max: - allows admins to dictate the minimum and maximum amount of time between monster posts (in minutes)
/config set_chance chance: - allows admin to set the probability of rare monsters appearing using 0 and 1 and numbers in between to set the probability 
/config set_enable enabled: - allows admins to turn on and off the monster messages 
```

User Commands

```
/connect - allows the user to connect their toy with a simple qrcode to scan
/leaderboard - allows user to see the leaderboard for candies collected and where they place on it
/rank - allows the users to easily check their own rank 
```

## Installation

This repository contains the discord bot part, not the website part (which is private). The bot will not work properly if you can't connect it to any server.

First, you need to create a bot and add it to your server with at least the permission to send messages in the wanted channel and to create app-commands.

(Tested in python 3.10.1)

To install the bot code, you'll need to do:

```sh
# Clone repository
git clone https://github.com/Lu-neko/TrickOrTeaseBot
cd TrickOrTeaseBot

# Activate the env
py -m venv env

# On linux
. env/bin/activate

# On Windows
env\Scripts\activate

# Install the requirements
pip install -r requirements.txt
```

After this, you can fill up the .env :

```
TOKEN=YOUR_TOKEN_FOR_THE_API
DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN
GUILD=YOUR_GUILD
```

 and then start the bot with :

```sh
py -m trick_or_tease_bot
```

And after this step, the bot should be running correctly.

## Checklist :

* [x] Bot is working
* [x] You can connect your toys
* [x] Configuration for admins
* [x] Dropping monsters every x minutes
* [x] Leaderboard and Rank
* [x] Common monsters vibing everyone when claimed
* [x] Rare monsters give a link to the control page
* [ ] Put the api configuration in the .env file
* [ ] Custom emojis for the views