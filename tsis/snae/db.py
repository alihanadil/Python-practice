import psycopg2
from config import DB_CONFIG

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    """Create tables if they don't exist."""
    sql = """
    CREATE TABLE IF NOT EXISTS players (
        id       SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL
    );
    CREATE TABLE IF NOT EXISTS game_sessions (
        id            SERIAL PRIMARY KEY,
        player_id     INTEGER REFERENCES players(id),
        score         INTEGER   NOT NULL,
        level_reached INTEGER   NOT NULL,
        played_at     TIMESTAMP DEFAULT NOW()
    );
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
        return True
    except Exception as e:
        print(f"DB init error: {e}")
        return False

def get_or_create_player(username):
    """Return player id, creating the row if needed."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM players WHERE username = %s", (username,))
                row = cur.fetchone()
                if row:
                    return row[0]
                cur.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
                return cur.fetchone()[0]
    except Exception as e:
        print(f"DB player error: {e}")
        return None

def save_session(username, score, level_reached):
    """Save a completed game session."""
    try:
        player_id = get_or_create_player(username)
        if player_id is None:
            return
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
                    (player_id, score, level_reached)
                )
    except Exception as e:
        print(f"DB save error: {e}")

def get_top10():
    """Return list of (rank, username, score, level, date) for top 10."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT p.username, gs.score, gs.level_reached,
                           TO_CHAR(gs.played_at, 'YYYY-MM-DD')
                    FROM game_sessions gs
                    JOIN players p ON p.id = gs.player_id
                    ORDER BY gs.score DESC
                    LIMIT 10
                """)
                rows = cur.fetchall()
        return [(i + 1,) + row for i, row in enumerate(rows)]
    except Exception as e:
        print(f"DB top10 error: {e}")
        return []

def get_personal_best(username):
    """Return the player's highest score, or 0 if none."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT COALESCE(MAX(gs.score), 0)
                    FROM game_sessions gs
                    JOIN players p ON p.id = gs.player_id
                    WHERE p.username = %s
                """, (username,))
                return cur.fetchone()[0]
    except Exception as e:
        print(f"DB personal best error: {e}")
        return 0
