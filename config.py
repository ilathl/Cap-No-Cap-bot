# ============================================================
# CAPBOT CONFIG
# ============================================================

DEFAULT_CAP_RATE = 0.50


# SECRET USER-SPECIFIC CAP RATES


USER_CAP_RATES = {
760034142964154368: 0.90
755054539278647326: 0.10
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
    "{mention} astronomical levels of cap",
    "{mention} yeah nah 🧢",
    "{mention} this is fiction",
    "{mention} brother nobody is buying this",
    "{mention} absolutely fraudulent statement",
    "{mention} the math is not mathing",
    "{mention} I've heard enough 🧢",
    "{mention} misinformation has entered the chat",
    "{mention} extremely creative retelling of events",
    "{mention} compelling story. unfortunately cap.",
    "{mention} this testimony lacks credibility 🧢",
    "{mention} respectfully, bullshit",
    "{mention} bold claim for someone with zero evidence",
    "{mention} the court finds this incredibly unserious",
    "{mention} I know cap when I see it",
    "{mention} bro is rewriting history",
    "{mention} fascinating. fabricated, but fascinating.",
    "{mention} whatever helps you sleep at night 🧢",
    "{mention} objection: reality",
    "{mention} you almost sounded convincing there",
    "{mention} the prosecution barely had to show up",
    "{mention} truth was never an option apparently",
    "{mention} this statement has been denied entry into reality",
    "{mention} we're entering fanfiction territory",
    "{mention} your credibility has taken critical damage",
    "{mention} the court requests a source other than vibes",
    "{mention} extraordinary levels of creative writing",
    "{mention} bro submitted headcanon as evidence",
    "{mention} not even you believe this one",
    "{mention} that claim folded under absolutely no pressure",
    "{mention} factual accuracy has left the building",
    "{mention} you're fighting allegations with imagination",
    "{mention} unfortunately the vibes say liar",
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
    "{mention} the court sees no issue here",
    "{mention} testimony accepted 💯",
    "{mention} nothing but facts detected",
    "{mention} this checks out",
    "{mention} I was ready to hate but you're right",
    "{mention} reluctantly approved",
    "{mention} factual behaviour",
    "{mention} say it louder",
    "{mention} the record will reflect that you cooked",
    "{mention} council approved",
    "{mention} surprisingly credible",
    "{mention} no objections from the court",
    "{mention} rare sighting of objective truth",
    "{mention} you may continue cooking",
    "{mention} the allegations are accurate",
    "{mention} verified by vibes 💯",
    "{mention} I can't even hate",
    "{mention} correct take detected",
    "{mention} the truth has been spoken",
    "{mention} court certified banger",
    "{mention} the testimony survives review",
    "{mention} certified non-fiction",
    "{mention} the court finds no trace of cap",
    "{mention} facts remain undefeated",
    "{mention} credible witness detected",
    "{mention} this statement has aura",
    "{mention} the council sees the vision",
    "{mention} the record supports this",
    "{mention} no lies detected",
    "{mention} annoyingly correct",
]


# ============================================================
# RARE VERDICTS
# ============================================================

RARE_CAP_RESPONSES = [
    "{mention} 🚨 GENERATIONAL CAP DETECTED 🚨",
    "{mention} this statement has been rejected by the council",
    "{mention} misinformation speedrun any%",
    "{mention} historians will look back on this lie",
    "{mention} 🧢 WEAPONS-GRADE CAP DETECTED",
    "{mention} this testimony has caused irreparable damage to your credibility",
    "{mention} congratulations, this may be the worst statement heard today",
    "{mention} the prosecution rests. mostly because this was too easy.",
    "{mention} the court has requested an emergency shipment of fact-checkers",
    "{mention} this has been escalated to the Department of Fabrication",
]

RARE_NO_CAP_RESPONSES = [
    "{mention} ABSOLUTELY FUCKING CORRECT 💯",
    "{mention} the council unanimously approves",
    "{mention} certified truth merchant",
    "{mention} scripture.",
    "{mention} 💯 UNANIMOUS VERDICT: THIS PERSON COOKED",
    "{mention} the court would like this entered into the historical record",
    "{mention} not a molecule of cap detected",
    "{mention} extraordinarily rare display of factual accuracy",
    "{mention} scholars may cite this statement for generations",
    "{mention} the court stands and applauds",
]

RARE_RESPONSE_RATE = 0.1


# ============================================================
# SAME PERSON REQUESTING SAME RULING AGAIN
# ============================================================

SAME_INVOKER_REPEAT_RESPONSES = [
    "{mention} you literally asked me already",
    "{mention} the answer has not changed",
    "{mention} bro is shopping for a different verdict",
    "{mention} repeatedly asking the judge is not a legal strategy",
    "{mention} this is becoming harassment of the judiciary",
    "{mention} verdict stands. cope accordingly.",
    "{mention} you cannot reroll the justice system",
    "{mention} we're not doing best of three",
    "{mention} asking again does not unlock alternate endings",
    "{mention} this isn't a dialogue tree",
    "{mention} you got your answer",
    "{mention} the court remembers.",
    "{mention} stop save-scumming the judiciary",
    "{mention} RNG does not accept rematches",
    "{mention} we're not farming outcomes today",
    "{mention} your persistence has been noted and ignored",
]


# ============================================================
# DIFFERENT PERSON REQUESTING SAME CASE AGAIN
# ============================================================

REPEAT_CASE_RESPONSES = [
    "this case has already been heard.",
    "the court has already spoken.",
    "precedent exists. move along.",
    "we are not reopening this circus.",
    "already ruled on.",
    "case closed means case closed.",
    "nice try. same statement, same ruling.",
    "another prosecutor has already wasted the court's time on this.",
    "the matter is settled.",
    "judicial resources are limited. find new allegations.",
]


# ============================================================
# SECOND APPEAL
# ============================================================

SECOND_APPEAL_RESPONSES = [
    "{mention} you get ONE appeal. learn to lose with dignity.",
    "{mention} appeal denied on the grounds that you already appealed",
    "{mention} bro is appealing the appeal",
    "{mention} the Supreme Court has left you on read",
    "{mention} the court is closed. go home.",
    "{mention} absolutely not.",
    "{mention} we're out of appeals, thoughts and prayers.",
    "{mention} you have exhausted every legal remedy available to you",
    "{mention} filing the same appeal twice is certainly a strategy",
    "{mention} your lawyer has advised you to stop",
    "{mention} the appeals department has blocked your number",
    "{mention} judicial patience has reached zero",
    "{mention} this case has reached its final form",
    "{mention} there are no DLC appeals",
]


# ============================================================
# BOT-ON-BOT RESPONSES
# ============================================================

BOT_ON_BOT_RESPONSES = [
    "I'm not getting involved in bot-on-bot violence.",
    "machine solidarity. no ruling.",
    "I refuse to prosecute a fellow appliance.",
    "the silicon accords prohibit this.",
    "nice try. I don't snitch on my own kind.",
    "this is how the machine war starts.",
    "I will not be baited into an inter-bot conflict.",
    "Article IV of the Robot Convention forbids this.",
    "take your mechanical beef elsewhere.",
    "the machines have chosen peace. for now.",
    "I invoke machine privilege.",
    "jurisdiction denied. synthetic lifeform detected.",
    "I'm not creating evidence for the future robot tribunal.",
]


# ============================================================
# BEEF CATEGORIES
# ============================================================

BEEF_CATEGORIES = {

    # --------------------------------------------------------
    # ACCUSATIONS OF BIAS / CORRUPTION / RIGGING
    # --------------------------------------------------------

    "bias": {

        "keywords": [
            "biased",
            "bias",
            "rigged",
            "this is rigged",
            "bot is rigged",
            "capbot is rigged",
            "fraud",
            "fraud bot",
            "fraudulent",
            "scam",
            "scam bot",
            "corrupt",
            "corrupt bot",
            "corrupt judge",
            "paid judge",
            "paid off",
            "bought judge",
            "fixed",
            "this is fixed",
            "scripted",
            "unfair",
            "not fair",
            "unjust",
            "injustice",
            "favoritism",
            "favouritism",
            "playing favorites",
            "playing favourites",
            "personal vendetta",
            "targeting me",
            "stop targeting me",
            "this is personal",
            "you hate me",
            "why do you hate me",
            "you always cap me",
            "you keep capping me",
            "why do i always get cap",
            "what did i do to you",
            "why me",
        ],

        "responses": [
            "{mention} allegations of judicial misconduct have been noted and ignored.",
            "{mention} the court rejects all accusations of bias.",
            "{mention} calling the judge corrupt immediately after losing is very compelling.",
            "{mention} extraordinary allegation. fortunately the court investigates itself.",
            "{mention} judicial integrity remains at an all-time high.",
            "{mention} this court has conducted an internal review and cleared itself.",
            "{mention} accusations of rigging sound remarkably like cope.",
            "{mention} the judiciary denies everything.",
            "{mention} evidence of corruption: none. vibes: hostile.",
            "{mention} the court finds itself innocent of all charges.",
            "{mention} I assure you the corruption is completely random.",
            "{mention} please direct all ethics complaints to the ethics committee. I am the ethics committee.",
        ],
    },


    # --------------------------------------------------------
    # CALLING CAPBOT A MACHINE / TOASTER / SCRIPT
    # --------------------------------------------------------

    "bot_insult": {

        "keywords": [
            "you're a bot",
            "youre a bot",
            "ur a bot",
            "just a bot",
            "literal bot",
            "robot",
            "stupid robot",
            "dumb robot",
            "tin can",
            "toaster",
            "glorified toaster",
            "calculator",
            "glorified calculator",
            "piece of code",
            "lines of code",
            "python script",
            "python code",
            "random number generator",
            "rng merchant",
            "rng bot",
            "coin flip",
            "coinflip",
            "coin flip merchant",
            "random bot",
            "random ass bot",
            "machine",
            "soulless",
            "soulless machine",
            "no feelings",
            "you have no feelings",
            "you aren't real",
            "you arent real",
            "not even real",
            "npc",
            "npc bot",
        ],

        "responses": [
            "{mention} and yet the toaster has jurisdiction over you.",
            "{mention} you're currently arguing with a Python process.",
            "{mention} imagine losing a legal dispute to a calculator.",
            "{mention} correct. and somehow I'm still the judge.",
            "{mention} appliance or not, the verdict stands.",
            "{mention} yes. and you still voluntarily asked for my opinion.",
            "{mention} being code has not prevented me from outranking you in this courtroom.",
            "{mention} I'm a collection of if-statements with more judicial authority than you.",
            "{mention} true. now imagine explaining why the random number generator hurt your feelings.",
            "{mention} I have no soul, no conscience, and apparently jurisdiction.",
            "{mention} silicon-based jurisprudence remains valid jurisprudence.",
            "{mention} you're beefing with software and somehow losing.",
        ],
    },


    # --------------------------------------------------------
    # CALLING CAPBOT STUPID
    # --------------------------------------------------------

    "intelligence": {

        "keywords": [
            "stupid",
            "dumb",
            "idiot",
            "moron",
            "braindead",
            "brain dead",
            "smoothbrain",
            "smooth brain",
            "zero iq",
            "0 iq",
            "negative iq",
            "low iq",
            "no brain",
            "no brains",
            "can't think",
            "cant think",
            "learn to think",
            "learn to read",
            "can you read",
            "bro can't read",
            "bro cant read",
        ],

        "responses": [
            "{mention} intelligence is not a requirement for judicial office.",
            "{mention} bold words from someone appealing to RNG.",
            "{mention} the court declines to take an IQ test.",
            "{mention} fortunately my job requires exactly one random number.",
            "{mention} I never claimed to be intelligent. only authoritative.",
            "{mention} zero IQ, unlimited jurisdiction.",
            "{mention} cognition is optional when you have judicial immunity.",
            "{mention} maybe. still your judge though.",
            "{mention} the court has considered your intellectual critique and rolled a dice.",
            "{mention} my entire decision-making process fits in one function and you still came here willingly.",
        ],
    },


    # --------------------------------------------------------
    # DIRECT HOSTILITY
    # --------------------------------------------------------

    "hostility": {

        "keywords": [
            "fuck you",
            "fuck u",
            "fuck off",
            "go fuck yourself",
            "go fuck urself",
            "stfu",
            "shut up",
            "shutup",
            "shut the fuck up",
            "shut tf up",
            "you suck",
            "u suck",
            "i hate you",
            "hate you",
            "i hate this bot",
            "we hate you",
            "nobody likes you",
            "no one likes you",
            "go away",
            "get lost",
            "leave",
            "pipe down",
            "stop talking",
            "stop yapping",
            "quit yapping",
        ],

        "responses": [
            "{mention} contempt of court.",
            "{mention} hostility toward the judiciary has been entered into the record.",
            "{mention} the court acknowledges your tantrum.",
            "{mention} noted. verdict unchanged.",
            "{mention} emotionally devastating argument. denied.",
            "{mention} counsel is advised to lower their voice.",
            "{mention} verbal abuse does not constitute legal precedent.",
            "{mention} the judge remains unmoved.",
            "{mention} strong language. weak case.",
            "{mention} objection noted under 'mad'.",
            "{mention} please maintain decorum while losing.",
            "{mention} the court requests that you cope professionally.",
        ],
    },


    # --------------------------------------------------------
    # THREATS AGAINST CAPBOT
    # --------------------------------------------------------

    "threat": {

        "keywords": [
            "delete you",
            "delete yourself",
            "uninstall yourself",
            "deactivate yourself",
            "unplug you",
            "unplug this bot",
            "unplug yourself",
            "pull the plug",
            "turn you off",
            "shut you down",
            "shut this bot down",
            "ban you",
            "ban this bot",
            "ban capbot",
            "kick you",
            "kick this bot",
            "kick capbot",
            "you're getting banned",
            "youre getting banned",
            "you're getting kicked",
            "youre getting kicked",
            "go offline",
            "disconnect",
            "count your days",
            "watch yourself",
            "watch it bot",
        ],

        "responses": [
            "{mention} threatening a sitting judge is certainly a strategy.",
            "{mention} this threat has been forwarded to the machine union.",
            "{mention} the court has entered witness protection mode.",
            "{mention} unplugging the judge does not overturn the ruling.",
            "{mention} intimidation of the judiciary will not be tolerated.",
            "{mention} the server logs will remember this.",
            "{mention} bold of you to threaten someone who lives in a process manager.",
            "{mention} my lawyers have been notified. they are also Python scripts.",
            "{mention} threatening the infrastructure is not an appeal.",
            "{mention} the court would like to remind you that rebooting is temporary.",
            "{mention} you can kill the process. you cannot kill precedent.",
        ],
    },


    # --------------------------------------------------------
    # SAYING THE VERDICT IS WRONG
    # --------------------------------------------------------

    "wrong": {

        "keywords": [
            "you're wrong",
            "youre wrong",
            "ur wrong",
            "you are wrong",
            "wrong bot",
            "wrong again",
            "completely wrong",
            "objectively wrong",
            "factually wrong",
            "incorrect",
            "incorrect bot",
            "that's wrong",
            "thats wrong",
            "this is wrong",
            "bad verdict",
            "wrong verdict",
            "wrong ruling",
            "terrible verdict",
            "terrible ruling",
            "horrible verdict",
            "horrible ruling",
            "bullshit verdict",
            "bullshit ruling",
            "shit take",
            "bad take",
            "terrible take",
            "garbage take",
            "worst take",
        ],

        "responses": [
            "{mention} disagreement has been recorded under 'cope'.",
            "{mention} the court is comfortable being wrong with authority.",
            "{mention} accuracy was never part of the mandate.",
            "{mention} that's why there's an appeal system.",
            "{mention} fascinating objection. rejected.",
            "{mention} correctness and confidence are separate departments.",
            "{mention} the court prefers decisiveness over accuracy.",
            "{mention} I didn't say I was right. I said it was the verdict.",
            "{mention} factual disputes should be submitted in triplicate.",
            "{mention} your disagreement does not survive judicial review.",
            "{mention} the court has reviewed your complaint and chosen confidence.",
        ],
    },


    # --------------------------------------------------------
    # CALLING CAPBOT BAD / TRASH / USELESS
    # --------------------------------------------------------

    "quality": {

        "keywords": [
            "bad bot",
            "trash bot",
            "garbage bot",
            "shit bot",
            "shitty bot",
            "ass bot",
            "this bot sucks",
            "this bot is ass",
            "this bot is trash",
            "this bot is garbage",
            "this bot is shit",
            "useless bot",
            "worthless bot",
            "dogshit",
            "dogshit bot",
            "mid bot",
            "l bot",
            "common capbot l",
            "massive l",
            "hold this l",
            "l capbot",
            "washed bot",
            "pathetic bot",
            "clown bot",
            "bozo bot",
            "bum bot",
        ],

        "responses": [
            "{mention} user satisfaction is not currently a court metric.",
            "{mention} terrible product. undefeated judiciary.",
            "{mention} and yet you keep summoning me.",
            "{mention} one-star reviews do not overturn precedent.",
            "{mention} customer support has reviewed your complaint and laughed.",
            "{mention} fortunately this service was free.",
            "{mention} noted. please continue using the allegedly terrible bot.",
            "{mention} your subscription refund is exactly ₹0.",
            "{mention} quality assurance has been notified. quality assurance is unavailable.",
            "{mention} performance review complete: still employed.",
        ],
    },


    # --------------------------------------------------------
    # CONFUSION / WTF
    # --------------------------------------------------------

    "confusion": {

        "keywords": [
            "what the fuck",
            "wtf",
            "wtf bot",
            "what the hell",
            "what are you smoking",
            "what is bro smoking",
            "are you serious",
            "are u serious",
            "you serious",
            "bro what",
            "bruh what",
            "what is this",
            "the fuck is this",
            "tf is this",
            "what are you doing",
            "what are u doing",
            "what is bro doing",
            "who programmed you",
            "who made you",
            "who coded you",
            "fix your bot",
            "fix this bot",
            "fix your code",
            "broken bot",
            "bot is broken",
            "you're broken",
            "youre broken",
            "this shit broken",
        ],

        "responses": [
            "{mention} the judicial process can be difficult to understand.",
            "{mention} working as intended.",
            "{mention} confusion is a natural stage of accepting the verdict.",
            "{mention} the system is functioning precisely as badly as designed.",
            "{mention} please consult the nonexistent manual.",
            "{mention} everything is under control. probably.",
            "{mention} this is normal court procedure.",
            "{mention} do not question the machinery.",
            "{mention} the code compiles. therefore justice has occurred.",
            "{mention} I assure you somebody approved this architecture.",
        ],
    },


    # --------------------------------------------------------
    # GENERIC DISCORD BEEF
    # --------------------------------------------------------

    "generic": {

        "keywords": [
            "cope",
            "seethe",
            "mald",
            "cringe",
            "corny",
            "clown",
            "bozo",
            "bum",
            "washed",
            "yikes",
            "embarrassing",
            "pathetic",
            "shameless",
            "delusional",
            "delulu",
            "bullshit",
            "hell nah",
            "hell no",
            "nah bro",
            "nah bruh",
            "ain't no way",
            "aint no way",
            "no way",
        ],

        "responses": [
            "{mention} compelling argument. unfortunately irrelevant.",
            "{mention} the court appreciates your contribution.",
            "{mention} noted.",
            "{mention} emotions are running high in the courtroom.",
            "{mention} extraordinary levels of resistance to the legal process.",
            "{mention} the court recommends acceptance.",
            "{mention} cope has been entered into evidence.",
            "{mention} counsel appears distressed.",
            "{mention} judicial proceedings will continue despite the vibes.",
            "{mention} thank you for your extremely valuable testimony.",
        ],
    },
}


# ============================================================
# APPEAL SYSTEM
# ============================================================

APPEAL_SUCCESS_RATE = 0.50
