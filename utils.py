import random
import nextcord

words = open("sgb-words.txt").read().splitlines()


EMOJI_CODES = {
    "green": {
       "a": "<:1f1e6:988519604248793119>",
       "b": "<:1f1e7:988519605066682458>" ,
       "c": "<:1f1e8:988519606132023306>" ,
       "d": "<:1f1e9:988519607130275940>" ,
       "e": "<:1f1ea:988519607960752168>" ,
       "f": "<:1f1eb:988519608690569276>" ,
       "g": "<:1f1ec:988519609705562132>" ,
       "h": "<:1f1ed:988519610913546340>" ,
       "i": "<:1f1ee:988519612498972682>",
       "j": "<:1f1ef:988519613606293534>" ,
       "k": "<:1f1f0:988519614407405608>" ,
       "l": "<:1f1f1:988519614902321183>" ,
       "m": "<:1f1f2:988519615787335821>" ,
       "n": "<:1f1f3:988519616999460904>" ,
       "o": "<:1f1f4:988519618110976070>" ,
       "p": "<:1f1f5:988519619134390282>" ,
       "q": "<:1f1f6:988519620069711972>" ,
       "r": "<:1f1f7:988519620820488232>" ,
       "s": "<:1f1f8:988519621575446548>" ,
       "t": "<:1f1f9:988519622418497616>" ,
       "u": "<:1f1fa:988519623261585428>" ,
       "v": "<:1f1fb:988519624050089984>" ,
       "w": "<:1f1fc:988519624712802394>" ,
       "x": "<:1f1fd:988519625090289697>" ,
       "y": "<:1f1fe:988519626214355024>" ,
       "z": "<:1f1ff:988519626965127309>" ,
    },

     "yellow": {
       "a": "<:1f1e6:988520028133548052>",
       "b": "<:1f1e7:988520029257597040>" ,
       "c": "<:1f1e8:988520031224725585>" ,
       "d": "<:1f1e9:988520031954559017>" ,
       "e": "<:1f1ea:988520032864706570>" ,
       "f": "<:1f1eb:988520033644871790>" ,
       "g": "<:1f1ec:988520034471116891>" ,
       "h": "<:1f1ed:988520035209334825>" ,
       "i": "<:1f1ee:988520036622807120>",
       "j": "<:1f1ef:988520037658796032>" ,
       "k": "<:1f1f0:988520038443139182>" ,
       "l": "<:1f1f1:988520039315558453>" ,
       "m": "<:1f1f2:988520040078925864>" ,
       "n": "<:1f1f3:988520041089728582>" ,
       "o": "<:1f1f4:988520041903439912>" ,
       "p": "<:1f1f5:988520042708754432>" ,
       "q": "<:1f1f6:988520043425959966>" ,
       "r": "<:1f1f7:988520044390678538>" ,
       "s": "<:1f1f8:988520045124665484>" ,
       "t": "<:1f1f9:988520046034845806>" ,
       "u": "<:1f1fa:988520046752055326>" ,
       "v": "<:1f1fb:988520047368626189>" ,
       "w": "<:1f1fc:988520048207470626>" ,
       "x": "<:1f1fd:988520049381896232>" ,
       "y": "<:1f1fe:988520592468762714>" ,
       "z": "<:1f1ff:988520593567670272>" ,
    },

    "blue": {
       "a": ":regional_indicator_a:",
       "b": ":regional_indicator_b:",
       "c": ":regional_indicator_c:",
       "d": ":regional_indicator_d:",
       "e": ":regional_indicator_e:",
       "f": ":regional_indicator_f:",
       "g": ":regional_indicator_g:",
       "h": ":regional_indicator_h:",
       "i": ":regional_indicator_i:",
       "j": ":regional_indicator_j:",
       "k": ":regional_indicator_k:",
       "l": ":regional_indicator_l:",
       "m": ":regional_indicator_m:",
       "n": ":regional_indicator_n:",
       "o": ":regional_indicator_o:",
       "p": ":regional_indicator_p:",
       "q": ":regional_indicator_q:",
       "r": ":regional_indicator_r:",
       "s": ":regional_indicator_s:",
       "t": ":regional_indicator_t:",
       "u": ":regional_indicator_u:",
       "v": ":regional_indicator_v:",
       "w": ":regional_indicator_w:",
       "x": ":regional_indicator_x:",
       "y": ":regional_indicator_y:",
       "z": ":regional_indicator_z:",
    }
}
def generate_colored_word(guess: str, answer: str) -> str:
    """Return a string of emojis with the letters colored """

    colored_word = [EMOJI_CODES["blue"][letter] for letter in guess]
    guess_letters = list(guess)
    answer_letters = list(answer)
    #change colors to green if correct
    for i in range(len(guess_letters)):
        if guess_letters[i] == answer_letters[i]:
            colored_word[i] = EMOJI_CODES["green"][guess_letters[i]]
            answer_letters[i] = None
            guess_letters[i] = None
    #change colors to yellow if correct but not in right place
    for i in range(len(guess_letters)):
        if guess_letters[i] is not None and guess_letters[i] in answer_letters:
            colored_word[i] = EMOJI_CODES["yellow"][guess_letters[i]]
            answer_letters[answer_letters.index(guess_letters[i])] = None
    return "".join(colored_word)

def generate_blanks():
    """Return a string of 5 blank emoji characters"""
    return "\N{WHITE MEDIUM SQUARE}" * 5

def generate_puzzle_embed(user: nextcord.User, puzzle_id: int) -> nextcord.Embed:
    embed = nextcord.Embed(title="Wordle Clone")
    embed.description = "\n".join([generate_blanks()] * 6)
    embed.set_author(name=user.name, icon_url=user.display_avatar.url)
    embed.set_footer(
        text=f"ID: {puzzle_id} | To play use the command w.play\n"
        "To guess, reply to this message with the word."
    )
    return embed


def is_valid_word(word: str) -> bool:
    """check if this is valid"""
    return word.lower() in words

def random_puzzle_id() -> int:
    return random.randint(0, len(words) - 1)

def update_embed(embed: nextcord.Embed, guess: str) -> nextcord.Embed:
    puzzle_id = int(embed.footer.text.split()[1])
    answer = words[puzzle_id]
    colored_word = generate_colored_word(guess, answer)
    empty_slot = generate_blanks()
    # replace the first blank with the colored letters
    embed.description = embed.description.replace(empty_slot, colored_word, 1)
    # game over
    nun_empty_slots = embed.description.count(empty_slot)
    if guess == answer:
        if nun_empty_slots == 0:
            embed.description += "\n\nPhew"
        if nun_empty_slots == 1:
            embed.description += "\n\nOk Ok!"
        if nun_empty_slots == 2:
            embed.description += "\n\nJhezz!"
        if nun_empty_slots == 3:
            embed.description += "\n\nWE OUT HERE!"
        if nun_empty_slots == 4:
            embed.description += "\n\nYOOOOOOOO!"
        if nun_empty_slots == 5:
            embed.description += "\n\nNah your just cheating"
    elif nun_empty_slots == 0:
        embed.description += f"\n\n Dam you suck. The word was {answer}"
    return embed

def is_game_over(embed: nextcord.Embed) -> bool:
    return "\n\n" in embed.description