# ============================================================
# CAP OR NO-CAP BOT — CONFIG
# ============================================================

# Default chance of someone receiving CAP
# 0.50 = 50%
DEFAULT_CAP_RATE = 0.50


# ============================================================
# SECRET USER-SPECIFIC CAP RATES
# ============================================================

# Put Discord User IDs here to rig someone's odds.
#
# Example:
# 123456789012345678: 0.90
#
# Anyone NOT listed here automatically gets the normal 50/50.

USER_CAP_RATES = {
    760034142964154368: 0.60,
}


# ============================================================
# NORMAL CAP RESPONSES
# ============================================================

CAP_RESPONSES = [
    "{mention} stop capping 🧢",
    "{mention} that's straight cap 🧢",
    "{mention} dubious amounts of copium",
    "{mention} be serious rn",
    "{mention} we're just making shit up now",
    "{mention} source: trust me bro 🧢",
    "{mention} you don't even believe that",
    "{mention} astronomical levels of cap 🧢",
    "{mention} yeah nah 🧢",
    "{mention} this is fiction",
]


# ============================================================
# NORMAL NO-CAP RESPONSES
# ============================================================

NO_CAP_RESPONSES = [
    "{mention} no cap, straight gas",
    "{mention} I see no cap 💯",
    "{mention} FRFR you right",
    "{mention} let him cook",
    "{mention} unfortunately has a point",
    "{mention} real recognizes real",
    "{mention} the facts have been checked 💯",
    "{mention} valid.",
    "{mention} speaking nothing but truth",
    "{mention} certified factual",
]


# ============================================================
# RARE CAP RESPONSES
# ============================================================

RARE_CAP_RESPONSES = [
    "{mention} 🚨 GENERATIONAL CAP DETECTED 🚨",
    "{mention} this statement has been rejected by the council",
    "{mention} misinformation speedrun any%",
    "{mention} historians will look back on this lie",
]


# ============================================================
# RARE NO-CAP RESPONSES
# ============================================================

RARE_NO_CAP_RESPONSES = [
    "{mention} ABSOLUTELY FUCKING CORRECT 💯",
    "{mention} the council unanimously approves",
    "{mention} certified truth merchant",
    "{mention} scripture.",
]


# ============================================================
# RARE RESPONSE CHANCE
# ============================================================

# 0.02 = 2%
#
# This does NOT affect whether something is Cap or No-Cap.
# It only decides whether CapBot uses one of the rare responses.

RARE_RESPONSE_RATE = 0.02


# ============================================================
# APPEAL SYSTEM
# ============================================================

# 0.25 = 25% chance that an appeal succeeds.

APPEAL_SUCCESS_RATE = 0.25