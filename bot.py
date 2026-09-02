import os
import random
import re

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

    SAME_INVOKER_REPEAT_RESPONSES,
    REPEAT_CASE_RESPONSES,
    SECOND_APPEAL_RESPONSES,

    BOT_ON_BOT_RESPONSES,

    BEEF_CATEGORIES,

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

        print(
            "Database ready."
        )

        await self.tree.sync()

        print(
            "Slash commands synced."
        )


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

    probability = get_cap_probability(
        user_id
    )

    if random.random() < probability:
        return "CAP"

    return "NO_CAP"


def choose_response(
    verdict,
    mention
):

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


    response = random.choice(
        pool
    )


    return response.format(
        mention=mention
    )


# ============================================================
# CLEAN MESSAGE TEXT
# ============================================================

def clean_message_content(message):

    content = message.content.lower()


    # Remove CapBot's Discord mention.
    #
    # Discord represents mentions internally as:
    #
    # <@123456789>
    #
    # or sometimes:
    #
    # <@!123456789>

    if bot.user:

        content = content.replace(
            f"<@{bot.user.id}>",
            ""
        )

        content = content.replace(
            f"<@!{bot.user.id}>",
            ""
        )


    # Replace punctuation with spaces

    cleaned = re.sub(
        r"[^\w\s']",
        " ",
        content
    )


    # Collapse repeated whitespace

    cleaned = re.sub(
        r"\s+",
        " ",
        cleaned
    ).strip()


    return cleaned


# ============================================================
# KEYWORD MATCHING
# ============================================================

def keyword_matches(
    cleaned_content,
    keyword
):

    keyword_clean = (
        keyword
        .lower()
        .strip()
    )


    # Multi-word phrase

    if " " in keyword_clean:

        return (
            keyword_clean
            in cleaned_content
        )


    # Single words need boundaries.
    #
    # This prevents:
    #
    # "cap"
    #
    # matching random words containing
    # those same characters.

    pattern = (
        r"\b"
        + re.escape(keyword_clean)
        + r"\b"
    )


    return bool(
        re.search(
            pattern,
            cleaned_content
        )
    )


# ============================================================
# BEEF CLASSIFIER
# ============================================================

def get_beef_category(message):

    cleaned = clean_message_content(
        message
    )


    if not cleaned:
        return None


    # --------------------------------------------------------
    # Iterate in config order.
    #
    # More specific categories should therefore appear
    # before generic categories inside config.py.
    # --------------------------------------------------------

    for category, data in BEEF_CATEGORIES.items():

        keywords = data[
            "keywords"
        ]


        for keyword in keywords:

            if keyword_matches(
                cleaned,
                keyword
            ):

                return category


    return None


def choose_beef_response(
    category,
    mention
):

    responses = (
        BEEF_CATEGORIES[
            category
        ]["responses"]
    )


    response = random.choice(
        responses
    )


    return response.format(
        mention=mention
    )


# ============================================================
# FIND TARGET MESSAGE
# ============================================================

async def find_target_message(message):

    # --------------------------------------------------------
    # REPLY MODE
    #
    # Reply to a human message + @CapBot
    # → judge that exact message
    # --------------------------------------------------------

    if (
        message.reference
        and message.reference.message_id
    ):

        try:

            target = (
                await message.channel.fetch_message(
                    message.reference.message_id
                )
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
    # Otherwise find the previous human message.
    # --------------------------------------------------------

    async for previous_message in message.channel.history(
        limit=10,
        before=message,
    ):

        if previous_message.author.bot:
            continue

        return previous_message


    return None


# ============================================================
# FIND ORIGINAL STATEMENT FROM CAPBOT VERDICT
# ============================================================

async def get_original_message_from_capbot_reply(
    message
):

    # The user must be replying to something.

    if not (
        message.reference
        and message.reference.message_id
    ):

        return None


    try:

        replied_message = (
            await message.channel.fetch_message(
                message.reference.message_id
            )
        )


    except (
        discord.NotFound,
        discord.Forbidden,
        discord.HTTPException,
    ):

        return None


    # Must be replying to CapBot.

    if (
        replied_message.author.id
        != bot.user.id
    ):

        return None


    # CapBot's verdict itself must be
    # a reply to the original statement.

    if not (
        replied_message.reference
        and replied_message.reference.message_id
    ):

        return None


    try:

        original_message = (
            await message.channel.fetch_message(
                replied_message.reference.message_id
            )
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

def get_streak_message(
    stats,
    mention
):

    streak = stats[
        "current_streak"
    ]

    verdict = stats[
        "current_verdict"
    ]


    # --------------------------------------------------------
    # CAP STREAKS
    # --------------------------------------------------------

    if verdict == "CAP":

        if streak == 3:

            return (
                f"{mention} "
                "hat trick 🧢🧢🧢"
            )


        if streak == 5:

            return (
                f"{mention} "
                "GENERATIONAL LIAR"
            )


        if streak == 10:

            return (
                f"{mention} statistically "
                "this is getting concerning"
            )


    # --------------------------------------------------------
    # NO-CAP STREAKS
    # --------------------------------------------------------

    if verdict == "NO_CAP":

        if streak == 3:

            return (
                f"{mention} "
                "is on a truth arc 💯"
            )


        if streak == 5:

            return (
                f"{mention} "
                "certified truth merchant"
            )


        if streak == 10:

            return (
                f"{mention} has apparently "
                "transcended dishonesty"
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
# MAIN MESSAGE HANDLER
# ============================================================

@bot.event
async def on_message(message):

    # --------------------------------------------------------
    # Ignore bot messages
    # --------------------------------------------------------

    if message.author.bot:
        return


    # --------------------------------------------------------
    # CapBot must actually be mentioned
    # --------------------------------------------------------

    if (
        bot.user
        not in message.mentions
    ):

        return


    # ========================================================
    # BEEF DETECTION
    # ========================================================

    beef_category = (
        get_beef_category(
            message
        )
    )


    if beef_category:

        response = (
            choose_beef_response(
                beef_category,
                message.author.mention
            )
        )


        await message.reply(
            response
        )

        return


    # ========================================================
    # APPEAL DETECTION
    # ========================================================

    cleaned_content = (
        clean_message_content(
            message
        )
    )


    is_appeal = (
        keyword_matches(
            cleaned_content,
            "appeal"
        )
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

        original_verdict = ruling[7]

        already_appealed = ruling[8]


        # ----------------------------------------------------
        # SECOND APPEAL
        # ----------------------------------------------------

        if already_appealed:

            response = random.choice(
                SECOND_APPEAL_RESPONSES
            )


            await message.reply(
                response.format(
                    mention=message.author.mention
                )
            )

            return


        # ----------------------------------------------------
        # Anyone can appeal.
        #
        # Every ruling still receives only ONE appeal.
        # ----------------------------------------------------

        mark_appealed(
            original_message.id
        )


        appeal_success = (
            random.random()
            < APPEAL_SUCCESS_RATE
        )


        # ----------------------------------------------------
        # SUCCESSFUL APPEAL
        # ----------------------------------------------------

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


        # ----------------------------------------------------
        # FAILED APPEAL
        # ----------------------------------------------------

        else:

            readable_verdict = (
                original_verdict.replace(
                    "_",
                    " "
                )
            )


            response = (
                "## APPEAL DENIED\n\n"
                f"**{readable_verdict}** stands.\n\n"
                "The court is unmoved."
            )


        await message.reply(
            response
        )

        return


    # ========================================================
    # REPLYING DIRECTLY TO CAPBOT
    # WITHOUT APPEALING
    # ========================================================

    if (
        message.reference
        and message.reference.message_id
    ):

        try:

            replied_message = (
                await message.channel.fetch_message(
                    message.reference.message_id
                )
            )


        except (
            discord.NotFound,
            discord.Forbidden,
            discord.HTTPException,
        ):

            replied_message = None


        if (
            replied_message
            and replied_message.author.id
            == bot.user.id
        ):

            responses = [

                "the court has already spoken.",

                "if you want to challenge the ruling, appeal.",

                "why are you asking me to judge myself?",

                "I issued the verdict. keep up.",

                "you're replying to the judge.",

                "please direct complaints through the completely legitimate appeals process.",

                "the judiciary does not fact-check itself.",

                "this conversation is becoming procedurally confusing.",
            ]


            await message.reply(
                random.choice(
                    responses
                )
            )

            return


    # ========================================================
    # FIND TARGET MESSAGE
    # ========================================================

    target_message = (
        await find_target_message(
            message
        )
    )


    if target_message is None:

        await message.reply(
            "I got nothing to judge."
        )

        return


    # ========================================================
    # BOT-ON-BOT VIOLENCE
    # ========================================================

    if target_message.author.bot:

        await message.reply(
            random.choice(
                BOT_ON_BOT_RESPONSES
            )
        )

        return


    # ========================================================
    # EXISTING RULING
    # ========================================================

    existing_ruling = get_ruling(
        target_message.id
    )


    if existing_ruling:

        original_invoker_id = (
            existing_ruling[6]
        )


        # ----------------------------------------------------
        # SAME PERSON CALLING CAPBOT AGAIN
        # ----------------------------------------------------

        if (
            message.author.id
            == original_invoker_id
        ):

            response = random.choice(
                SAME_INVOKER_REPEAT_RESPONSES
            )


            await message.reply(
                response.format(
                    mention=message.author.mention
                )
            )

            return


        # ----------------------------------------------------
        # DIFFERENT PERSON TRYING SAME CASE
        # ----------------------------------------------------

        response = random.choice(
            REPEAT_CASE_RESPONSES
        )


        await message.reply(
            response
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
    # Server only
    # --------------------------------------------------------

    if message.guild is None:

        await message.reply(
            "The Cap Court only operates inside servers."
        )

        return


    # --------------------------------------------------------
    # Store ruling
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
    # SELF-SUBMISSION
    # ========================================================

    if (
        message.author.id
        == target_user.id

        and random.random()
        < 0.25
    ):

        self_submission_responses = [

            (
                f"{target_user.mention} "
                "really called for a fact check on himself"
            ),

            (
                f"{target_user.mention} "
                "voluntarily submitted himself to the court"
            ),

            (
                f"{target_user.mention} "
                "requested an audit of his own statement"
            ),

            (
                f"{target_user.mention} "
                "self-reported to the authorities"
            ),

            (
                f"{target_user.mention} "
                "has chosen to testify against himself"
            ),

            (
                f"{target_user.mention} "
                "has waived the right to remain silent"
            ),

            (
                f"{target_user.mention} "
                "apparently wanted judicial consequences"
            ),
        ]


        await message.channel.send(
            random.choice(
                self_submission_responses
            )
        )


    # ========================================================
    # STREAK CHECK
    # ========================================================

    stats = get_user_stats(
        message.guild.id,
        target_user.id
    )


    streak_message = (
        get_streak_message(
            stats,
            target_user.mention
        )
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


    current_verdict = (
        data["current_verdict"]
        .replace(
            "_",
            " "
        )
    )


    current_streak = (
        f"{data['current_streak']} "
        f"{current_verdict}"
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

        username = row[1]

        total = row[2]

        cap_count = row[3]


        cap_rate = (
            cap_count
            / total
        ) * 100


        lines.append(

            f"**{position}. {username}** — "
            f"{cap_rate:.1f}% 🧢 "
            f"({cap_count}/{total})"
        )


    text = (
        "## 🏆 CERTIFIED CAPPERS\n\n"
        + "\n".join(
            lines
        )
    )


    await interaction.response.send_message(
        text
    )


# ============================================================
# START CAPBOT
# ============================================================

bot.run(
    TOKEN
)