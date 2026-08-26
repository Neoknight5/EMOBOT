from io import BytesIO
import sqlite3
from datetime import datetime, timedelta

import requests
from PIL import Image  

conn = sqlite3.connect("data.db")
conn.row_factory = sqlite3.Row  
cursor = conn.cursor()


# --------------------------------------------------------------------------
# table creation

def user_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        coins INTEGER DEFAULT 0,
        xp INTEGER DEFAULT 0,
        str_id INTEGER DEFAULT 0,
        str_id2 INTEGER DEFAULT 0,
        str_id3 INTEGER DEFAULT 0,
        wp_id INTEGER DEFAULT 0,
        lt_work TEXT DEFAULT "",
        last_daily TEXT DEFAULT "",
        last_cf TEXT DEFAULT ""
    )
    """)
    conn.commit()


def wp_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wallpaper(
        wp_id INTEGER PRIMARY KEY,
        name TEXT,
        price INTEGER,
        url TEXT
    )
    """)
    conn.commit()


def str_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS str(
        str_id INTEGER PRIMARY KEY,
        name TEXT,
        price INTEGER,
        url TEXT
    )
    """)
    conn.commit()


def inv_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory(
        user_id INTEGER,
        item_type TEXT,
        item_id INTEGER,
        quantity INTEGER DEFAULT 1,
        PRIMARY KEY(user_id, item_type, item_id)
    )
    """)
    conn.commit()


def migrate_users_table():
    """Defensive migration: adds any columns missing from an ALREADY-EXISTING
    users table. CREATE TABLE IF NOT EXISTS only creates the table the first
    time — it silently does nothing if the table is already there with an
    older/different schema. This is almost certainly why str_id wasn't
    showing up: something created `users` before this schema could, and
    IF NOT EXISTS let that older version win. Run this every startup and
    you never have to manually delete data.db again to pick up a new column.
    """
    cursor.execute("PRAGMA table_info(users)")
    existing_cols = {row[1] for row in cursor.fetchall()}

    expected_cols = {
        "coins": "INTEGER DEFAULT 0",
        "xp": "INTEGER DEFAULT 0",
        "str_id": "INTEGER DEFAULT 0",
        "str_id2": "INTEGER DEFAULT 0",
        "str_id3": "INTEGER DEFAULT 0",
        "wp_id": "INTEGER DEFAULT 0",
        "lt_work": 'TEXT DEFAULT ""',
        "last_daily": 'TEXT DEFAULT ""',
        "last_cf": 'TEXT DEFAULT ""',
    }

    for col, definition in expected_cols.items():
        if col not in existing_cols:
            cursor.execute(f"ALTER TABLE users ADD COLUMN {col} {definition}")

    conn.commit()


# --------------------------------------------------------------------------
# main helper class
# --------------------------------------------------------------------------

class coins:
    """Helper class providing common coin/xp/user operations using the
    module-level sqlite3 connection and cursor.

    Also doubles as a small cooldown-tracking object: coins(iso_string)
    wraps a stored ISO timestamp and answers can_work/can_daily checks.
    """

    # ---------------- setup ----------------

    @staticmethod
    def ensure_tables():
        user_table()
        str_table()
        wp_table()
        inv_table()
        migrate_users_table()

    # ---------------- users ----------------

    @staticmethod
    def add_user(
        user_id: int,
        coins_val: int = 0,
        xp: int = 0,
        str_id: int = 0,
        wp_id: int = 0,
        lt_work: str = "",
        last_daily: str = "",
        last_cf: str = "",
    ):
        cursor.execute(
            """
            INSERT INTO users(id, coins, xp, str_id, wp_id, lt_work, last_daily, last_cf)
            VALUES(?,?,?,?,?,?,?,?)
            """,
            (user_id, coins_val, xp, str_id, wp_id, lt_work, last_daily, last_cf),
        )
        conn.commit()

    @staticmethod
    def get_user(user_id: int):
        cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
        return cursor.fetchone()

    @staticmethod
    def user_exists(user_id: int):
        cursor.execute("SELECT 1 FROM users WHERE id=?", (user_id,))
        return cursor.fetchone() is not None

    @staticmethod
    def delete_user(user_id: int):
        cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()

    @staticmethod
    def update_coins(user_id: int, coins_val: int):
        cursor.execute("UPDATE users SET coins=? WHERE id=?", (coins_val, user_id))
        conn.commit()

    @staticmethod
    def update_xp(user_id: int, xp_val: int):
        cursor.execute("UPDATE users SET xp=? WHERE id=?", (xp_val, user_id))
        conn.commit()

    @staticmethod
    def add_xp(user_id: int, amount: int = 2):
        cursor.execute("UPDATE users SET xp = xp + ? WHERE id = ?", (amount, user_id))
        conn.commit()

    @staticmethod
    def update_str(user_id: int, str_id: int):
        cursor.execute("UPDATE users SET str_id=? WHERE id=?", (str_id, user_id))
        conn.commit()

    # slot-based equip: slot 1/2/3 map to the str_id/str_id2/str_id3 columns.
    # Whitelisted on purpose — never build a column name from user input
    # directly, even though slot is already type-checked as an int.
    _STR_SLOT_COLUMNS = {1: "str_id", 2: "str_id2", 3: "str_id3"}

    @staticmethod
    def update_str_slot(user_id: int, slot: int, str_id: int):
        column = coins._STR_SLOT_COLUMNS.get(slot)
        if column is None:
            raise ValueError(f"slot must be 1, 2, or 3 (got {slot})")
        cursor.execute(f"UPDATE users SET {column}=? WHERE id=?", (str_id, user_id))
        conn.commit()

    @staticmethod
    def get_equipped_stickers(user_id: int):
        """Returns the up-to-3 equipped sticker ids for a user, in slot
        order, skipping empty slots (stored as 0)."""
        data = coins.get_user(user_id)
        if data is None:
            return []
        slot_ids = [data["str_id"], data["str_id2"], data["str_id3"]]
        return [sid for sid in slot_ids if sid]

    @staticmethod
    def update_wp(user_id: int, wp_id: int):
        cursor.execute("UPDATE users SET wp_id=? WHERE id=?", (wp_id, user_id))
        conn.commit()

    @staticmethod
    def update_last_work(user_id: int, value: str):
        cursor.execute("UPDATE users SET lt_work=? WHERE id=?", (value, user_id))
        conn.commit()

    @staticmethod
    def update_last_daily(user_id: int, value: str):
        cursor.execute("UPDATE users SET last_daily=? WHERE id=?", (value, user_id))
        conn.commit()

    @staticmethod
    def all_users():
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()

    @staticmethod
    def leaderboard():
        cursor.execute("SELECT * FROM users ORDER BY coins DESC LIMIT 10")
        return cursor.fetchall()

    # ---------------- stickers ----------------

    @staticmethod
    def add_str(str_id: int, name: str, price: int, url: str):
        cursor.execute(
            "INSERT OR REPLACE INTO str(str_id, name, price, url) VALUES(?,?,?,?)",
            (str_id, name, price, url),
        )
        conn.commit()

    @staticmethod
    def get_str(str_id: int):
        cursor.execute("SELECT * FROM str WHERE str_id=?", (str_id,))
        return cursor.fetchone()

    @staticmethod
    def delete_str(str_id: int):
        cursor.execute("DELETE FROM str WHERE str_id=?", (str_id,))
        conn.commit()

    @staticmethod
    def all_str():
        cursor.execute("SELECT * FROM str")
        return cursor.fetchall()

    @staticmethod
    def update_str_price(str_id: int, new_price: int):
        cursor.execute("UPDATE str SET price=? WHERE str_id=?", (new_price, str_id))
        conn.commit()

    @staticmethod
    def update_str_name(str_id: int, new_name: str):
        cursor.execute("UPDATE str SET name=? WHERE str_id=?", (new_name, str_id))
        conn.commit()

    @staticmethod
    def update_str_url(str_id: int, new_url: str):
        cursor.execute("UPDATE str SET url=? WHERE str_id=?", (new_url, str_id))
        conn.commit()

    # ---------------- wallpaper ----------------

    @staticmethod
    def add_wp(wp_id: int, name: str, price: int, url: str):
        cursor.execute(
            "INSERT OR REPLACE INTO wallpaper(wp_id, name, price, url) VALUES(?,?,?,?)",
            (wp_id, name, price, url),
        )
        conn.commit()

    @staticmethod
    def get_wp(wp_id: int):
        cursor.execute("SELECT * FROM wallpaper WHERE wp_id=?", (wp_id,))
        return cursor.fetchone()

    @staticmethod
    def delete_wp(wp_id: int):
        cursor.execute("DELETE FROM wallpaper WHERE wp_id=?", (wp_id,))
        conn.commit()

    @staticmethod
    def all_wp():
        cursor.execute("SELECT * FROM wallpaper")
        return cursor.fetchall()

    @staticmethod
    def update_wp_price(wp_id: int, new_price: int):
        cursor.execute("UPDATE wallpaper SET price=? WHERE wp_id=?", (new_price, wp_id))
        conn.commit()

    @staticmethod
    def update_wp_url(wp_id: int, new_url: str):
        cursor.execute("UPDATE wallpaper SET url=? WHERE wp_id=?", (new_url, wp_id))
        conn.commit()

    @staticmethod
    def load_wallpaper(url: str):
        response = requests.get(url)
        wallpaper = Image.open(BytesIO(response.content)).convert("RGBA")
        return wallpaper

    # ---------------- inventory ----------------

    @staticmethod
    def add_inventory(user_id: int, item_type: str, item_id: int, quantity: int = 1):
        cursor.execute(
            "SELECT quantity FROM inventory WHERE user_id=? AND item_type=? AND item_id=?",
            (user_id, item_type, item_id),
        )
        data = cursor.fetchone()

        if data:
            cursor.execute(
                "UPDATE inventory SET quantity = quantity + ? WHERE user_id=? AND item_type=? AND item_id=?",
                (quantity, user_id, item_type, item_id),
            )
        else:
            cursor.execute(
                "INSERT INTO inventory(user_id, item_type, item_id, quantity) VALUES(?,?,?,?)",
                (user_id, item_type, item_id, quantity),
            )

        conn.commit()

    @staticmethod
    def remove_inventory(user_id: int, item_type: str, item_id: int, quantity: int = 1):
        cursor.execute(
            "SELECT quantity FROM inventory WHERE user_id=? AND item_type=? AND item_id=?",
            (user_id, item_type, item_id),
        )
        data = cursor.fetchone()
        if not data:
            return

        if data[0] > quantity:
            cursor.execute(
                "UPDATE inventory SET quantity = quantity - ? WHERE user_id=? AND item_type=? AND item_id=?",
                (quantity, user_id, item_type, item_id),
            )
        else:
            cursor.execute(
                "DELETE FROM inventory WHERE user_id=? AND item_type=? AND item_id=?",
                (user_id, item_type, item_id),
            )

        conn.commit()

    @staticmethod
    def get_inventory(user_id: int):
        cursor.execute("SELECT * FROM inventory WHERE user_id=?", (user_id,))
        return cursor.fetchall()

    @staticmethod
    def owns_item(user_id: int, item_type: str, item_id: int):
        cursor.execute(
            "SELECT 1 FROM inventory WHERE user_id=? AND item_type=? AND item_id=?",
            (user_id, item_type, item_id),
        )
        return cursor.fetchone() is not None

    @staticmethod
    def owns_sticker(user_id: int, str_id: int):
        return coins.owns_item(user_id, "str", str_id)

    @staticmethod
    def owns_wallpaper(user_id: int, wp_id: int):
        return coins.owns_item(user_id, "wp", wp_id)

    @staticmethod
    def get_user_stickers(user_id: int):
        cursor.execute(
            "SELECT item_id FROM inventory WHERE user_id=? AND item_type='str'",
            (user_id,),
        )
        return [row[0] for row in cursor.fetchall()]

    @staticmethod
    def get_user_wallpapers(user_id: int):
        cursor.execute(
            "SELECT item_id FROM inventory WHERE user_id=? AND item_type='wp'",
            (user_id,),
        )
        return [row[0] for row in cursor.fetchall()]

    # ---------------- cooldown tracking (instance side) ----------------
    # Usage: coins(user_row_lt_work_value).can_work()

    def __init__(self, time_iso: str = ""):
        self.time_iso = time_iso

    def get_time(self):
        if not self.time_iso:
            return None
        try:
            return datetime.fromisoformat(self.time_iso)
        except ValueError:
            return None

    def set_time(self, value=None):
        if value is None:
            value = datetime.now()
        elif isinstance(value, str):
            value = datetime.fromisoformat(value)
        self.time_iso = value.isoformat()
        return self

    def can_work(self, cooldown: timedelta = timedelta(minutes=15)) -> bool:
        # was calling self.get_last_work(), which didn't exist -> AttributeError
        last = self.get_time()
        if last is None:
            return True
        return datetime.now() - last >= cooldown

    def remaining_work(self, cooldown: timedelta = timedelta(minutes=15)):
        last = self.get_time()
        if last is None:
            return 0
        remain = cooldown - (datetime.now() - last)
        return max(0, int(remain.total_seconds()))

    def can_daily(self, cooldown: timedelta = timedelta(hours=12)):
        last = self.get_time()
        if last is None:
            return True
        return datetime.now() - last >= cooldown

    def remaining_daily(self, cooldown: timedelta = timedelta(hours=12)):
        last = self.get_time()
        if last is None:
            return 0
        remain = cooldown - (datetime.now() - last)
        return max(0, remain.total_seconds() / 3600)
    # =========================
    # TABLES
    # =========================

    @staticmethod
    def td_players_table():

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS td_players(

            guild_id INTEGER,

            user_id INTEGER,

            position INTEGER,

            PRIMARY KEY(guild_id, user_id)

        )
        """)

        conn.commit()

    @staticmethod
    def td_server_table():

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS td_server(

            guild_id INTEGER PRIMARY KEY,

            current_turn INTEGER DEFAULT 1

        )
        """)

        conn.commit()

    # =========================
    # SERVER
    # =========================

    @staticmethod
    def create_td_server(guild_id: int):

        cursor.execute(
        """
        INSERT OR IGNORE INTO td_server(
            guild_id
        )
        VALUES(?)
        """,
        (guild_id,)
        )

        conn.commit()

    @staticmethod
    def get_current_turn(guild_id: int):

        cursor.execute(
        """
        SELECT current_turn
        FROM td_server
        WHERE guild_id=?
        """,
        (guild_id,)
        )

        row = cursor.fetchone()

        if row:
            return row[0]

        return 1

    @staticmethod
    def update_current_turn(
        guild_id: int,
        turn: int
    ):

        cursor.execute(
        """
        UPDATE td_server
        SET current_turn=?
        WHERE guild_id=?
        """,
        (
            turn,
            guild_id
        )
        )

        conn.commit()

    # =========================
    # PLAYERS
    # =========================

    @staticmethod
    def add_td_player(
        guild_id: int,
        user_id: int,
        position: int
    ):

        cursor.execute(
        """
        INSERT OR IGNORE INTO td_players(
            guild_id,
            user_id,
            position
        )
        VALUES(?,?,?)
        """,
        (
            guild_id,
            user_id,
            position
        )
        )

        conn.commit()

    @staticmethod
    def remove_td_player(
        guild_id: int,
        user_id: int
    ):

        cursor.execute(
        """
        DELETE FROM td_players
        WHERE guild_id=? AND user_id=?
        """,
        (
            guild_id,
            user_id
        )
        )

        conn.commit()

    @staticmethod
    def get_td_players(guild_id: int):

        cursor.execute(
        """
        SELECT *
        FROM td_players
        WHERE guild_id=?
        ORDER BY position
        """,
        (guild_id,)
        )

        return cursor.fetchall()

    @staticmethod
    def td_player_count(guild_id: int):

        cursor.execute(
        """
        SELECT COUNT(*)
        FROM td_players
        WHERE guild_id=?
        """,
        (guild_id,)
        )

        return cursor.fetchone()[0]

    @staticmethod
    def td_player_exists(
        guild_id: int,
        user_id: int
    ):

        cursor.execute(
        """
        SELECT 1
        FROM td_players
        WHERE guild_id=? AND user_id=?
        """,
        (
            guild_id,
            user_id
        )
        )

        return cursor.fetchone() is not None

    @staticmethod
    def get_player_by_position(
        guild_id: int,
        position: int
    ):

        cursor.execute(
        """
        SELECT *
        FROM td_players
        WHERE guild_id=? AND position=?
        """,
        (
            guild_id,
            position
        )
        )

        return cursor.fetchone()

    
    
user_table()
wp_table()
str_table()
inv_table()
migrate_users_table()
coins.td_server_table()
coins.td_players_table()



# coins.add_str(1,"str1",50000,"https://media.discordapp.net/attachments/1524050865374105631/1530549415167922246/140806234859369.jpg?ex=6a786fb8&is=6a771e38&hm=53a7d6748efdbf57e5ed68b8c83069360abfaaf568d15a0f87dc4e3bfc182449&=&format=webp")
# coins.add_str(2,"str2",50000,"https://media.discordapp.net/attachments/1524050865374105631/1530553064925167786/Stickers_for_Sale.jpg?ex=6a78731e&is=6a77219e&hm=b2434671b9f9c0996b20dfdce97d78b1dda785556a44f7585d36054f786a98a9&=&format=webp")
# coins.add_str(3,"str3",70000,"https://media.discordapp.net/attachments/1524050865374105631/1530553317569200159/Halloween_stickers_for_car___Bat_Sticker.jpg?ex=6a78735b&is=6a7721db&hm=9ec060b767ae5539624dce74200efe7605ab3573cb13d007b904109c378ee8ab&=&format=webp&width=384&height=384")
# coins.add_str(4,"str4",70000,"https://media.discordapp.net/attachments/1524050865374105631/1530553569659453601/19069998418824418.jpg?ex=6a787397&is=6a772217&hm=070e6648ce519cace2997dc890da5b02b0c956362d621f3f0f14cb7e611ac080&=&format=webp&width=384&height=384")
# coins.add_str(5,"str5",90000,"https://media.discordapp.net/attachments/1524050865374105631/1530553801109667960/339881103150503412.jpg?ex=6a7873ce&is=6a77224e&hm=018681a5d3e0d355c1dd2f5e392c4ec17ac890fa2ea7341fa3564f27e2784d2f&=&format=webp&width=384&height=382")
# coins.add_str(6,"str6",50000,"https://media.discordapp.net/attachments/1524050865374105631/1530553933800538133/Ref__Logo.jpg?ex=6a7873ee&is=6a77226e&hm=36c85391b2d818af82146947317a7ca76930bdd7e64b84644ae3d0d81c9ed0b2&=&format=webp&width=384&height=384")
# coins.add_str(7,"str7",90000,"https://media.discordapp.net/attachments/1524050865374105631/1530554334599839845/Pixel_Style_Cartoon_Doctor_Hat_Graduation_Season_PNG_Free_Deduction_Picture_PNG_Images___PSD_Free_Download_-_Pikbest.jpg?ex=6a78744d&is=6a7722cd&hm=0b22cf1bb4c91c07e58cbdc94e76f9f3ba37f113af57688cf810557710a32ec1&=&format=webp")
# coins.add_str(8,"str8" ,120000,"https://media.discordapp.net/attachments/1524050865374105631/1530858204781740143/golden_trophy_cup_in_pixel_art_style.jpg?ex=6a783dcd&is=6a76ec4d&hm=e9dd8b249aa7238865e26b0d45fcc23c67cbe8f12d452a8cba788bd8aba981de&=&format=webp")
# coins.add_str(9,"str9",150000,"https://media.discordapp.net/attachments/1524050865374105631/1530860580695703592/11751649021958189.jpg?ex=6a784004&is=6a76ee84&hm=3381b14ac24a4012453b2e978e6f23258923123a3a3daa5ec0547888a07dbf3b&=&format=webp&width=360&height=640")
# coins.add_str(10,"str1",200000,"https://media.discordapp.net/attachments/1524050865374105631/1530860581324722207/88312842691864211.jpg?ex=6a784004&is=6a76ee84&hm=2b81c84bee392b084d76c0ffce3ec1158125b06f819c4a028bcb3897e05d64ed&=&format=webp")
# coins.add_str(11,"str1",230000,"https://media.discordapp.net/attachments/1524050865374105631/1530876430781780099/6e8c4e0cdbab9c8c547dbd3922bc9762.jpg?ex=6a784ec7&is=6a76fd47&hm=d710f11fb03e200a88fda50c74d89869649d4c9fd5b3432768789d54ae9f4eee&=&format=webp&width=384&height=384")
# coins.add_str(12,"str1",270000,"https://images-ext-1.discordapp.net/external/6vbffcdn6kBPbYBSuWuwqX04JwP-KyztZSHgoGIc5x4/https/i.pinimg.com/736x/1e/83/1b/1e831b5e193ff13410668fd503e1f34a.jpg?format=webp")
# coins.add_str(13,"str1",350000,"https://media.discordapp.net/attachments/1524050865374105631/1531583757948293130/d22f0d29f2b1fc11f23df242d712bcf1.png?ex=6a783e87&is=6a76ed07&hm=e103f83153adaf47993c47014627070065a3c53263570d233f4d88c5d58b5984&=&format=webp&quality=lossless&width=640&height=640")
# coins.add_str(14,"str1",350000,"https://images-ext-1.discordapp.net/external/gGjZak8o5Z5Dx32M1vu5UNYqKm1T5nOvCCt9X-p5Sfw/https/i.pinimg.com/736x/17/fc/c1/17fcc142d217aeaff52a47910f0e8f7e.jpg?format=webp")
# coins.add_str(15,"str15",300000,"https://media.discordapp.net/attachments/1524050865374105631/1531629219719807047/Aaa.jpg?ex=6a7868de&is=6a77175e&hm=8990cd04ba6b8bc1be7de9b4a72a592aa6aef428e5f2e3a531a29a30286dea48&=&format=webp")

# coins.add_wp(1,"wp1",100000,"https://media.discordapp.net/attachments/1487389986960707698/1531643411206242465/image.png?ex=6a791ed5&is=6a77cd55&hm=47538aef0098bd47a195d23340f67ff672934bfaf87ff06bc55c6f5f4508caf7&=&format=webp&quality=lossless")
# coins.add_wp(2,"wp2",270000,"https://images-ext-1.discordapp.net/external/GQRbkcOLgXWCaMLvonQTAqHGBWPITUkCje70zv4DoSU/%3Fformat%3Dwebp%26width%3D892%26height%3D615/https/images-ext-1.discordapp.net/external/1c1Y3vfTehzyRcinDcDX1gpmd0NSRbEBOGVxGs2oZd4/https/i.pinimg.com/1200x/af/bf/94/afbf94d44d85219a24bf99dcfc712e1c.jpg?format=webp&width=512&height=352")
# coins.add_wp(3,"wp3",290000,"https://cdn.discordapp.com/attachments/1487389986960707698/1531644179661328574/image.png?ex=6a791f8d&is=6a77ce0d&hm=4f46873aad9cfe011e4b015996be4ea34c8e265ed1aacd7b6123e3877a8c4e76")
# coins.add_wp(4,"wp4",300000,"https://media.discordapp.net/attachments/1487389986960707698/1531644354974978088/image.png?ex=6a791fb6&is=6a77ce36&hm=18594c1996ed60f472558a3a03faadbcca981f9e6337466bcfc8faf038464112&=&format=webp&quality=lossless")
# coins.add_wp(5,"wp5",320000,"https://media.discordapp.net/attachments/1486407954193322117/1531976354956836966/9e23f0e8bacb5f03ad6418a3bdd1727b.jpg?ex=6a790369&is=6a77b1e9&hm=20c1b87c86186cdd944cdb70eaa4262d80a6ee7715cea4a6b50568fee804f44c&=&format=webp")
# coins.add_wp(6,"wp6",350000,"https://cdn.discordapp.com/attachments/1487389986960707698/1531644471865770165/image.png?ex=6a791fd2&is=6a77ce52&hm=b3e0dd09c2222c9b79f009042c124520256bceadc405568b07bee2227abb6b7a")
# coins.add_wp(7,"wp7",380000,"https://media.discordapp.net/attachments/1487389986960707698/1531644829941891102/image.png?ex=6a792028&is=6a77cea8&hm=3a10acadb58904802d59015d272b7f81784000b4747628d2ed3fd84940b31d55&=&format=webp&quality=lossless")
# coins.add_wp(8,"wp8",400000,"https://images-ext-1.discordapp.net/external/xP1lT_LiwX4Dm0CHUtYHLrroRgU7lJaKfB3injkJr8Y/https/i.pinimg.com/736x/53/00/2d/53002d9b5528fd7222559fabc3ec6df2.jpg?format=webp")
# coins.add_wp(9,"wp9",500000,'https://images-ext-1.discordapp.net/external/FVqDK21D-BY0HXSHc6K18zqaYZpNZA-XY-QW77O1Cts/%3Fformat%3Dwebp%26width%3D670%26height%3D670/https/images-ext-1.discordapp.net/external/HxQ4lpc8T4dDL3IPgXUAbdYBGtoSHIaSpFTh-0msGb8/https/i.pinimg.com/1200x/e6/69/f0/e669f00b00074f018aba135e80e0ab26.jpg?format=webp')
# coins.add_wp(10,"wp10",500000,"https://images-ext-1.discordapp.net/external/VEhJeGwc81mNKteuQJo0USjsGV73f7633RAiURCser0/https/i.pinimg.com/736x/ec/af/19/ecaf19707ef5b6cdb25427eb6e8fdb7a.jpg?format=webp")


# rows = coins.all_str()
# val2 = coins.all_wp()

# coins.update_coins(1486400095317659880,20000000)
# coins.update_coins(1463873853892857856,50000000)

# print(val2)
# print([dict(row) for row in rows])
# print([dict(row) for row in val2])
print("✅✅")
# val = coins.get_user(1463873853892857856)
# print("__",val[5])

data = coins.get_user(1463873853892857856)
if data[1] >= 5000000 :
    val = 0
    coins.update_coins(1463873853892857856,val)
    print("🟩🟩🟩")
if not coins.user_exists(1486400095317659880):
    coins.add_user(1486400095317659880,55000,0,0,0,"","","")

print("🟦🟦 CODE SAVED 🟦🟦")
    

