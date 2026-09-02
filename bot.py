import os
import random

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from config import (
    DEFAULT_CAP_RATE,
    USER_CAP_RATES,
    CAP_RESPONSES,
    NO_CAP_RESPONSES,
    RARE_CAP_RESPONSES,
    RARE_NO_CAP_RESPONSES,
    RARE_RESPONSE_RATE,
    APPEAL_SUCCESS_RATE,
)

from database import (
    setup_database,
    get_ruling,
    save_ruling,
    mark_appealed,
    update_verdict,
    get_user_stats,
    get_leaderboard,
)


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError(
        "DISCORD_TOKEN wasn't found. Check your .env file."
    )


# ============================================================
# DISCORD SETUP
# ============================================================

intents = discord.Intents.default()
intents.message_content = True


class CapBot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents,
        )

    async def setup_hook(self):

        setup_database()
        print("Database ready.")

        await self.tree.sync()
        print("Slash commands synced.")


bot = CapBot()


# ============================================================
# VERDICT FUNCTIONS
# ============================================================

def get_cap_probability(user_id):

    return USER_CAP_RATES.get(
        user_id,
        DEFAULT_CAP_RATE
    )


def determine_verdict(user_id):

    cap_probability = get_cap_probability(
        user_id
    )

    if random.random() < cap_probability:
        return "CAP"

    return "NO_CAP"


def choose_response(verdict, mention):

    rare = (
        random.random()
        < RARE_RESPONSE_RATE
    )

    if verdict == "CAP":

        if rare:
            pool = RARE_CAP_RESPONSES
        else:
            pool = CAP_RESPONSES

    else:

        if rare:
            pool = RARE_NO_CAP_RESPONSES
        else:
            pool = NO_CAP_RESPONSES

    response = random.choice(pool)

    return response.format(
        mention=mention
    )


# ============================================================
# FIND WHICH MESSAGE WE ARE JUDGING
# ============================================================

async def find_target_message(message):

    # --------------------------------------------------------
    # REPLY MODE
    #
    # Reply to a human message + mention CapBot
    # → judge that message
    # --------------------------------------------------------

    if (
        message.reference
        and message.reference.message_id
    ):

        try:

            target = await message.channel.fetch_message(
                message.reference.message_id
            )

            return target

        except (
            discord.NotFound,
            discord.Forbidden,
            discord.HTTPException,
        ):
            pass


    # --------------------------------------------------------
    # NORMAL MODE
    #
    # Otherwise judge the previous human message
    # --------------------------------------------------------

    async for previous_message in message.channel.history(
        limit=5,
        before=message,
    ):

        if previous_message.author.bot:
            continue

        return previous_message


    return None


# ============================================================
# FIND ORIGINAL MESSAGE FROM A CAPBOT VERDICT
# ============================================================

async def get_original_message_from_capbot_reply(message):

    # User must be replying to something
    if not (
        message.reference
        and message.reference.message_id
    ):
        return None

    try:

        replied_message = await message.channel.fetch_message(
            message.reference.message_id
        )

    except (
        discord.NotFound,
        discord.Forbidden,
        discord.HTTPException,
    ):
        return None


    # The replied-to message must be CapBot's message
    if replied_message.author.id != bot.user.id:
        return None


    # CapBot's verdict itself must be a reply
    # to the original human statement
    if not (
        replied_message.reference
        and replied_message.reference.message_id
    ):
        return None


    try:

        original_message = await message.channel.fetch_message(
            replied_message.reference.message_id
        )

        return original_message

    except (
        discord.NotFound,
        discord.Forbidden,
        discord.HTTPException,
    ):
        return None


# ============================================================
# STREAK ANNOUNCEMENTS
# ============================================================

def get_streak_message(stats, mention):

    streak = stats["current_streak"]
    verdict = stats["current_verdict"]


    # --------------------------------------------------------
    # CAP streaks
    # --------------------------------------------------------

    if verdict == "CAP":

        if streak == 3:
            return (
                f"{mention} hat trick 🧢🧢🧢"
            )

        if streak == 5:
            return (
                f"{mention} GENERATIONAL LIAR"
            )

        if streak == 10:
            return (
                f"{mention} statistically this is "
                "getting concerning"
            )


    # --------------------------------------------------------
    # NO-CAP streaks
    # --------------------------------------------------------

    if verdict == "NO_CAP":

        if streak == 3:
            return (
                f"{mention} is on a truth arc 💯"
            )

        if streak == 5:
            return (
                f"{mention} certified truth merchant"
            )

        if streak == 10:
            return (
                f"{mention} has apparently transcended "
                "dishonesty"
            )


    return None


# ============================================================
# BOT READY
# ============================================================

@bot.event
async def on_ready():

    print(
        f"Logged in as {bot.user}"
    )

    print(
        "Cap or No-Cap is online."
    )


# ============================================================
# MAIN @CAPBOT SYSTEM
# ============================================================

@bot.event
async def on_message(message):

    # --------------------------------------------------------
    # Ignore bot messages
    # --------------------------------------------------------

    if message.author.bot:
        return


    # --------------------------------------------------------
    # Only activate when CapBot is mentioned
    # --------------------------------------------------------

    if bot.user not in message.mentions:
        return


    # --------------------------------------------------------
    # Detect appeal request
    # --------------------------------------------------------

    content = message.content.lower()

    is_appeal = (
        "appeal" in content
    )


    # ========================================================
    # APPEAL MODE
    # ========================================================

    if is_appeal:

        original_message = (
            await get_original_message_from_capbot_reply(
                message
            )
        )


        if original_message is None:

            await message.reply(
                "Reply to one of my rulings "
                "if you want to appeal it."
            )

            return


        ruling = get_ruling(
            original_message.id
        )


        if ruling is None:

            await message.reply(
                "I have no ruling for that message."
            )

            return


        # ----------------------------------------------------
        # DATABASE COLUMN ORDER
        #
        # 0 id
        # 1 guild_id
        # 2 channel_id
        # 3 message_id
        # 4 target_user_id
        # 5 target_username
        # 6 invoker_user_id
        # 7 verdict
        # 8 appealed
        # 9 created_at
        # ----------------------------------------------------

        target_user_id = ruling[4]
        original_verdict = ruling[7]
        already_appealed = ruling[8]



        # ----------------------------------------------------
        # Only one appeal allowed
        # ----------------------------------------------------

        if already_appealed:

            await message.reply(
                "Appeal already used. "
                "The court is closed."
            )

            return


        # ----------------------------------------------------
        # Consume the appeal
        # ----------------------------------------------------

        mark_appealed(
            original_message.id
        )


        # ----------------------------------------------------
        # Determine whether appeal succeeds
        # ----------------------------------------------------

        appeal_success = (
            random.random()
            < APPEAL_SUCCESS_RATE
        )


        if appeal_success:

            if original_verdict == "CAP":

                new_verdict = "NO_CAP"

                response = (
                    "## APPEAL SUCCESSFUL\n\n"
                    "💯 **NO CAP**\n\n"
                    "Previous ruling overturned."
                )


            else:

                new_verdict = "CAP"

                response = (
                    "## APPEAL SUCCESSFUL\n\n"
                    "🧢 **CAP**\n\n"
                    "Previous ruling overturned."
                )


            update_verdict(
                original_message.id,
                new_verdict
            )


        else:

            response = (
                "## APPEAL DENIED\n\n"
                f"**{original_verdict.replace('_', ' ')}** "
                "stands.\n\n"
                "The court is unmoved."
            )


        await message.reply(
            response
        )

        return


    # ========================================================
    # NORMAL JUDGEMENT MODE
    # ========================================================

    # --------------------------------------------------------
    # If someone replies directly to a CapBot verdict
    # with just @CapBot, don't treat CapBot itself
    # as the target
    # --------------------------------------------------------

    if (
        message.reference
        and message.reference.message_id
    ):

        try:

            replied_message = await message.channel.fetch_message(
                message.reference.message_id
            )

        except (
            discord.NotFound,
            discord.Forbidden,
            discord.HTTPException,
        ):

            replied_message = None


        if (
            replied_message
            and replied_message.author.id == bot.user.id
        ):

            await message.reply(
                "the court has already spoken."
            )

            return


    # --------------------------------------------------------
    # Find which message we're judging
    # --------------------------------------------------------

    target_message = await find_target_message(
        message
    )


    if target_message is None:

        await message.reply(
            "I got nothing to judge."
        )

        return


    # --------------------------------------------------------
    # Don't judge bot messages
    # --------------------------------------------------------

    if target_message.author.bot:

        await message.reply(
            "the court has already spoken."
        )

        return


    # ========================================================
    # CHECK FOR EXISTING RULING
    # ========================================================

    existing_ruling = get_ruling(
        target_message.id
    )


    if existing_ruling:

        existing_verdict = (
            existing_ruling[7]
        )


        if existing_verdict == "CAP":

            repeat_responses = [
                "verdict stands. 🧢",
                "appeal to reality denied.",
                "asking again isn't changing the ruling.",
                "still cap.",
                "the court has already spoken.",
            ]


        else:

            repeat_responses = [
                "verdict stands. 💯",
                "already cleared.",
                "the facts remain factual.",
                "still no cap.",
                "the court has already spoken.",
            ]


        await target_message.reply(
            random.choice(
                repeat_responses
            )
        )

        return


    # ========================================================
    # NEW RULING
    # ========================================================

    target_user = (
        target_message.author
    )


    verdict = determine_verdict(
        target_user.id
    )


    response = choose_response(
        verdict,
        target_user.mention
    )


    # --------------------------------------------------------
    # Server-only protection
    # --------------------------------------------------------

    if message.guild is None:

        await message.reply(
            "The Cap Court only operates inside servers."
        )

        return


    # --------------------------------------------------------
    # Save ruling
    # --------------------------------------------------------

    save_ruling(

        guild_id=message.guild.id,

        channel_id=message.channel.id,

        message_id=target_message.id,

        target_user_id=target_user.id,

        target_username=target_user.display_name,

        invoker_user_id=message.author.id,

        verdict=verdict,
    )


    # ========================================================
    # DELIVER VERDICT
    # ========================================================

    await target_message.reply(
        response
    )


    # ========================================================
    # SELF-SUBMISSION JOKE
    # ========================================================

    if (
        message.author.id == target_user.id
        and random.random() < 0.25
    ):

        await message.channel.send(
            f"{target_user.mention} really called for "
            "a fact check on himself"
        )


    # ========================================================
    # STREAK CHECK
    # ========================================================

    stats = get_user_stats(
        message.guild.id,
        target_user.id
    )


    streak_message = get_streak_message(
        stats,
        target_user.mention
    )


    if streak_message:

        await message.channel.send(
            streak_message
        )


# ============================================================
# /STATS
# ============================================================

@bot.tree.command(
    name="stats",
    description="View someone's official CapBot record"
)

@app_commands.describe(
    user="Whose criminal record do you want to see?"
)

async def stats(
    interaction: discord.Interaction,
    user: discord.Member,
):

    if interaction.guild is None:

        await interaction.response.send_message(
            "Server only.",
            ephemeral=True
        )

        return


    data = get_user_stats(
        interaction.guild.id,
        user.id
    )


    if data["total"] == 0:

        await interaction.response.send_message(
            f"{user.mention} has not been judged yet."
        )

        return


    current_streak = (
        f"{data['current_streak']} "
        f"{data['current_verdict']}"
    )


    text = (
        f"## {user.display_name.upper()}'S OFFICIAL RECORD\n\n"

        f"Judged: **{data['total']}** times\n\n"

        f"🧢 CAP: **{data['cap']}**\n"
        f"💯 NO CAP: **{data['no_cap']}**\n\n"

        f"Cap Rate: **{data['cap_rate']:.1f}%**\n\n"

        f"Current streak: **{current_streak}**\n"

        f"Longest Cap streak: "
        f"**{data['longest_cap_streak']}**\n"

        f"Longest No-Cap streak: "
        f"**{data['longest_no_cap_streak']}**"
    )


    await interaction.response.send_message(
        text
    )


# ============================================================
# /LEADERBOARD
# ============================================================

@bot.tree.command(
    name="leaderboard",
    description="See the server's biggest cappers"
)

async def leaderboard(
    interaction: discord.Interaction
):

    if interaction.guild is None:

        await interaction.response.send_message(
            "Server only.",
            ephemeral=True
        )

        return


    rows = get_leaderboard(
        interaction.guild.id,
        minimum_rulings=5
    )


    if not rows:

        await interaction.response.send_message(
            "Not enough evidence yet.\n"
            "Users need at least 5 rulings to qualify."
        )

        return


    lines = []


    for position, row in enumerate(
        rows[:10],
        start=1
    ):

        user_id = row[0]
        username = row[1]
        total = row[2]
        cap_count = row[3]

        cap_rate = (
            cap_count / total
        ) * 100


        lines.append(
            f"**{position}. {username}** — "
            f"{cap_rate:.1f}% 🧢 "
            f"({cap_count}/{total})"
        )


    text = (
        "## 🏆 CERTIFIED CAPPERS\n\n"
        + "\n".join(lines)
    )


    await interaction.response.send_message(
        text
    )


# ============================================================
# START CAPBOT
# ============================================================

bot.run(TOKEN)