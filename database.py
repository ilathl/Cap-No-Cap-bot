import sqlite3
from datetime import datetime, timezone


DATABASE_NAME = "capbot.db"


# ============================================================
# CONNECTION
# ============================================================

def connect():
    return sqlite3.connect(DATABASE_NAME)


# ============================================================
# CREATE DATABASE
# ============================================================

def setup_database():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rulings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            guild_id INTEGER NOT NULL,
            channel_id INTEGER NOT NULL,
            message_id INTEGER NOT NULL UNIQUE,

            target_user_id INTEGER NOT NULL,
            target_username TEXT NOT NULL,

            invoker_user_id INTEGER NOT NULL,

            verdict TEXT NOT NULL,

            appealed INTEGER DEFAULT 0,

            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ============================================================
# GET AN EXISTING RULING
# ============================================================

def get_ruling(message_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM rulings
        WHERE message_id = ?
    """, (message_id,))

    ruling = cursor.fetchone()

    conn.close()

    return ruling


# ============================================================
# SAVE NEW RULING
# ============================================================

def save_ruling(
    guild_id,
    channel_id,
    message_id,
    target_user_id,
    target_username,
    invoker_user_id,
    verdict,
):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO rulings (
            guild_id,
            channel_id,
            message_id,
            target_user_id,
            target_username,
            invoker_user_id,
            verdict,
            appealed,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?)
    """, (
        guild_id,
        channel_id,
        message_id,
        target_user_id,
        target_username,
        invoker_user_id,
        verdict,
        datetime.now(timezone.utc).isoformat(),
    ))

    conn.commit()
    conn.close()


# ============================================================
# MARK A RULING AS APPEALED
# ============================================================

def mark_appealed(message_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE rulings
        SET appealed = 1
        WHERE message_id = ?
    """, (message_id,))

    conn.commit()
    conn.close()


# ============================================================
# CHANGE VERDICT AFTER SUCCESSFUL APPEAL
# ============================================================

def update_verdict(message_id, verdict):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE rulings
        SET verdict = ?
        WHERE message_id = ?
    """, (
        verdict,
        message_id,
    ))

    conn.commit()
    conn.close()


# ============================================================
# USER STATISTICS
# ============================================================

def get_user_stats(guild_id, user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT verdict
        FROM rulings
        WHERE guild_id = ?
        AND target_user_id = ?
        ORDER BY id ASC
    """, (
        guild_id,
        user_id,
    ))

    rows = cursor.fetchall()

    conn.close()

    verdicts = [row[0] for row in rows]

    total = len(verdicts)

    cap_count = verdicts.count("CAP")
    no_cap_count = verdicts.count("NO_CAP")

    if total > 0:
        cap_rate = (cap_count / total) * 100
    else:
        cap_rate = 0


    # --------------------------------------------------------
    # Current streak
    # --------------------------------------------------------

    current_streak = 0
    current_verdict = None

    if verdicts:

        current_verdict = verdicts[-1]

        for verdict in reversed(verdicts):

            if verdict == current_verdict:
                current_streak += 1

            else:
                break


    # --------------------------------------------------------
    # Longest streaks
    # --------------------------------------------------------

    longest_cap_streak = 0
    longest_no_cap_streak = 0

    cap_streak = 0
    no_cap_streak = 0


    for verdict in verdicts:

        if verdict == "CAP":

            cap_streak += 1
            no_cap_streak = 0

            longest_cap_streak = max(
                longest_cap_streak,
                cap_streak
            )

        else:

            no_cap_streak += 1
            cap_streak = 0

            longest_no_cap_streak = max(
                longest_no_cap_streak,
                no_cap_streak
            )


    return {
        "total": total,

        "cap": cap_count,

        "no_cap": no_cap_count,

        "cap_rate": cap_rate,

        "current_streak": current_streak,

        "current_verdict": current_verdict,

        "longest_cap_streak": longest_cap_streak,

        "longest_no_cap_streak": longest_no_cap_streak,
    }


# ============================================================
# SERVER LEADERBOARD
# ============================================================

def get_leaderboard(guild_id, minimum_rulings=5):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            target_user_id,
            target_username,

            COUNT(*) AS total,

            SUM(
                CASE
                    WHEN verdict = 'CAP'
                    THEN 1
                    ELSE 0
                END
            ) AS cap_count

        FROM rulings

        WHERE guild_id = ?

        GROUP BY
            target_user_id,
            target_username

        HAVING COUNT(*) >= ?

        ORDER BY
            CAST(cap_count AS REAL) / COUNT(*) DESC,
            COUNT(*) DESC
    """, (
        guild_id,
        minimum_rulings,
    ))

    rows = cursor.fetchall()

    conn.close()

    return rows