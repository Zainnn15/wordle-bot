import os

from dotenv import load_dotenv

import nextcord
from nextcord.ext import commands

from utils import generate_puzzle_embed, is_game_over, is_valid_word, random_puzzle_id, update_embed

load_dotenv()

client = commands.Bot(command_prefix=[])


@client.slash_command(description="Play a game of wordle")
async def play(interaction: nextcord.Interaction):
    # generate a puzzle
    puzzle_id = random_puzzle_id()
    # create the puzzle to display
    embed = generate_puzzle_embed(interaction.user, puzzle_id)
    # send the puzzle as an interaction response
    await interaction.send(embed=embed)


@client.event
async def on_message(message: nextcord.Message):
     # get the message replied to
      ref = message.reference
      if not ref or not isinstance(ref.resolved, nextcord.Message):
        return
      parent = ref.resolved  
     # if the parent message is not the bot's message, ignore it
      if parent.author.id != client.user.id:
        return
     # check that the message has embeds
      if not parent.embeds:
        return  

      embed = parent.embeds[0]

     #check if the user is playing
      if embed.author.name != message.author.name:
        await message.reply("The game was started by {embed.author.name}", delete_after=5
        )
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return


      #check if the game is over
      if is_game_over(embed):
        await message.reply("The game is over. Start a new game with /play", delete_after=5
        )
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return


     # Check if a single word is valid
      if len(message.content.split()) > 1:
        await message.reply("That is not a valid word", delete_after=5)
        try:
          await message.delete(delay=5)
        except Exception:
          pass
        await message.delete(delay=5)
        return



     # check that the word is valid
      if not is_valid_word(message.content):
        await message.reply("That is not a valid word", delete_after=5)
        try:
          await message.delete(delay=5)
        except Exception:
          pass
        await message.delete(delay=5)
        return
     # update the embed
      embed = update_embed(embed, message.content)
      await parent.edit(embed=embed)

     # attempt to delete the message
      try:
        await message.delete()
      except Exception:
        pass
client.run("OTg4NDczNTU0Mjg0NzI4Mzkw.GkeQeA.tj5dT3fc4m4PC4f37XjQIdbq8tKsC2oFgaXCnE")