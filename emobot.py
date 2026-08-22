import discord
from discord.ext import commands
from discord import ui 
import datetime
from datetime import datetime,timedelta
import random
import database
from database import coins
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
import time
import asyncio


class embed(discord.Embed):
    def __init__(self, title: str = "", description: str = "", color=None, url: str = None, timestamp: datetime = None):
        super().__init__(
            title=title,
            description=description,
            color=color or discord.Color.blurple(),
            url=url,
            timestamp=timestamp or datetime.utcnow(),
        )

    @classmethod
    def from_data(cls, data: dict):
        instance = cls(
            title=data.get("title", ""),
            description=data.get("description", ""),
            color=data.get("color", discord.Color.blurple()),
            url=data.get("url"),
            timestamp=data.get("timestamp", datetime.utcnow()),
        )

        for field in data.get("fields", []):
            instance.add_field(
                name=field.get("name", "\u200b"),
                value=field.get("value", "\u200b"),
                inline=field.get("inline", False),
            )

        author = data.get("author")
        if author:
            instance.set_author(
                name=author.get("name"),
                url=author.get("url"),
                icon_url=author.get("icon_url"),
            )

        footer = data.get("footer")
        if footer:
            instance.set_footer(
                text=footer.get("text"),
                icon_url=footer.get("icon_url"),
            )

        if data.get("thumbnail"):
            instance.set_thumbnail(url=data["thumbnail"])

        if data.get("image"):
            instance.set_image(url=data["image"])

        return instance

    def to_dict(self):
        return super().to_dict()

    def add_field_safe(self, name: str, value: str, inline: bool = False):
        return super().add_field(
            name=name or "\u200b",
            value=value or "\u200b",
            inline=inline,
        )

    def set_thumbnail_url(self, url: str):
        return self.set_thumbnail(url=url)

    def set_image_url(self, url: str):
        return self.set_image(url=url)

    def with_random_color(self):
        self.color = discord.Color.from_rgb(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
        return self
         
from io import BytesIO
import sqlite3
from datetime import datetime, timedelta

import requests
from PIL import Image  


conn = sqlite3.connect("data.db")
conn.row_factory = sqlite3.Row  
cursor = conn.cursor()


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix = "e ",intents = intents,    help_command=None, allowed_mentions=discord.AllowedMentions(
        users=True
    ))
@bot.event
async def on_ready():


    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name="🥰hello i am EMO🌹 \njoin server \nttps://discord.gg/wGxVswvEK "
    )

    await bot.change_presence(
        activity=activity
    )

    print("Emobot is ready!")



#_________start_______________
@bot.command()
async def start(ctx):
    name = ctx.author.id
    coins.ensure_tables()
    if coins.user_exists(name):
        await ctx.reply("😅you already had an account ... 🙃")
    elif not coins.user_exists(name):
        coins.add_xp(name)
        coins.add_user(ctx.author.id,0,0,0,0,"","","")
        await ctx.reply("😊your account is succesfully created . 🤗thank for having a part of emo bot ")


@bot.command(name="hi",aliases=["hello"])
async def hi(ctx):
    list = ["😁hey i am emo","🤗hello how are you","(●'◡'●)hiiiiiii","😁nice to meet you",f"☺️{ctx.author.display_name} yoyo","(❁´◡`❁)","🥰love you","😻you are my love","♥️ hey good user","^_~","^_____^","^0^ 😁","( *︾▽︾)😁"]
    await ctx.reply(random.choice(list))

#_________balance__________
@bot.command(name="balance",aliases=["cash"])
async def balance(ctx,message=None):
    coins.ensure_tables()
    name = ctx.author.id
    try :
        if not coins.user_exists :
            await ctx.reply("😢you didnt have an acccount first use ```e start``` command to make it!")   
        else:
            data = coins.get_user(name)
            coins.add_xp(name)
            fu = abs(data[1])
            coins.update_coins(name,fu)
            await ctx.reply(f"💰your balance is ***{fu}*** \n keep earning💸 ")
            if message == "data":
                await ctx.send(data)
    except TypeError :
        await ctx.reply("😢you didnt have an acccount first use ```e start``` command to make it!")


#___________coinflip_____________________
@bot.command(name="coinsflip",aliases=["cf"])
async def coinflip(ctx,nam:int,message=None):
    name = ctx.author.id
    if message not in ["heads","tells"]:
        await ctx.reply("🙄i dont know about your choice choose between heads/tells commands is   ```e coinflip amount heads||tells```")
    elif nam == None or nam == str :
        await ctx.reply(f"🙄please enter your amount ```e coinflip amount heads||tells```")
    else :
        user_id = ctx.author.id
        if not coins.user_exists(user_id):
            await ctx.reply("😢First create an account using `e start`.")
            return
        data = coins.get_user(user_id)
        if data[1] < 0 :
            fu = abs(data[1])
            coins.update_coins(name,fu)
        if fu < nam or nam <= 0 :
            await ctx.reply("🥺you don't have enough coins 🪙 earn more coins for it 💰")
            return
        else:
            # data = (id, coins, xp, str, lt_work
            heads_url = "https://cdn.discordapp.com/attachments/1524050709228687460/1530940736999264448/Pixel_art_game_currency_coin.jpg?ex=6a67672b&is=6a6615ab&hm=1264132aad0259350b8a5cebebf59eea58df616256843b10fb3f4beca45bae50"
            tells_url = "https://cdn.discordapp.com/attachments/1524050709228687460/1530940761187815465/gold.jpg?ex=6a676730&is=6a6615b0&hm=ec9f1e32214d3e807e62f77adbe0c2f7e98ddedb611888011e34c956ecc09769"
            val = ["heads","tells"]
            cf = random.choice(val)
            coins.add_xp(user_id)
            if cf == "heads" and cf == message:
                reward = nam + nam
                new_balance = fu + reward
                coins.update_coins(user_id,new_balance)
                embed = discord.Embed(
                    title="you won 🥳",
                    description=f"**heads** || you won ***{reward}*** coins 🥳",
                    color=discord.Color.green()
        )
                embed.set_thumbnail(url=heads_url)
                await ctx.reply(embed=embed)
            elif cf == "tells" and cf == message:
                reward = nam + nam
                new_balance = fu + reward
                coins.update_coins(user_id,new_balance)
                embed = discord.Embed(
                title="you won 🥳",
                description=f"**tells** || you won ***{reward}*** coins 🥳",
                color=discord.Color.green()
            )
                embed.set_thumbnail(url=tells_url)
                await ctx.reply(embed=embed)
            else:
                if nam == fu:
                    reward = 0
                    coins.update_coins(user_id,reward)
                else :
                    reward = nam + nam
                    new_balance = fu - reward
                    coins.update_coins(user_id,new_balance)
                    if cf == "heads" :
                        embed = discord.Embed(
                title="you loss 🥺",
                description=f"**heads** || you loss ***{reward}*** coins try again 🤠",
                color=discord.Color.green()
            )
                        embed.set_thumbnail(url=heads_url)
                        await ctx.reply(embed=embed)
                    else :
                        embed = discord.Embed(
                        title="you loss 🥺",
                        description=f"**tells** || you loss ***{reward}*** coins try again 🤠",
                color=discord.Color.green()
            )
                        embed.set_thumbnail(url=heads_url)
                        await ctx.reply(embed=embed)

#________________FLEX COMMAND_______________________0_
@bot.command(name="flex",aliases=["show"])
async def flex(ctx,nam:int):
    name = ctx.author.id
    if not coins.user_exists(name):
        await ctx.reply("😢you didn't had an account use `e start` create it")
        return
    if not coins.get_str(nam):
        await ctx.reply("😢 the ID you entered is invalid or not exist  try again other one")
        return
    if not coins.owns_item(name,"str",nam):
        await ctx.reply("🥲 you didn't had this sticker buy it by `e buy str` ")
        return
    sticker = coins.get_str(nam) 
    embed = discord.Embed(title=f"😏{ctx.author.display_name} owned sticker👾 #flex😎",color=discord.Color.blue())
    embed.set_image(url=sticker[3])
    embed.set_footer(text="by Emo bot")
    await ctx.send(embed=embed)


@bot.command(name="helpsticker",aliases=["infostr","helpstr"])
async def sticker(ctx):
    embed = discord.Embed(title="📝info for sticker",description="\n🔺step for sticker\n\n1️⃣step - open shop`e shopstr`\n\n2️⃣step - select the sticker you like \n\n3️⃣step - get the id of it\n\n4️⃣step - `e buystr ID`use to buy \n\n5️⃣step - equip it use `e es ID`")
    await ctx.reply(embed=embed)
# __________sticker help__
@bot.command(name="helpwallpaper",aliases=["infowp","helpwp"])
async def sticker(ctx):
    embed = discord.Embed(title="📝info for wallpaper",description="\n🔺step for wallpaper \n\n1️⃣step - open shop`e shopwp`\n\n2️⃣step - select the wallpaper you like \n\n3️⃣step - get the id of it\n\n4️⃣step - `e buywp ID`use to buy \n\n5️⃣step - equip it use `e ewp ID`")
    await ctx.reply(embed=embed)
#___________my stickers__________

MAX_STICKERS_SHOWN = 3

#___________________use name and aliases_________________________________________________to other commands
@bot.command(name="mystickers", aliases=["my","mystr"])
async def my_stickers(ctx):
    user_id = ctx.author.id

    if not coins.user_exists(user_id):
        await ctx.reply("😢 You don't have an account.\nUse `e start` first.")
        return
    coins.add_xp(user_id,2)
    sticker_ids = coins.get_user_stickers(user_id)

    if not sticker_ids:
        await ctx.reply("😅 You don't own any stickers yet. Try `e buy_str <id>`.")
        return

    embeds = []
    for sticker_id in sticker_ids[:MAX_STICKERS_SHOWN]:
        sticker = coins.get_str(sticker_id)
        if sticker is None:
            # sticker was deleted from the shop after the user bought it
            continue

        # sticker = (str_id, name, price, url)
        embed = discord.Embed(
            title=sticker[1],
            description=f"🆔 ID : **{sticker[0]}**\n💰 Price : **{sticker[2]}** coins",
            color=discord.Color.blue(),
        )
        embed.set_thumbnail(url=sticker[3])
        embeds.append(embed)

    if not embeds:
        await ctx.reply("😅 None of your stickers could be found — they may have been removed from the shop.")
        return

    await ctx.reply(
        content=f"🎟️ **{ctx.author.display_name}**'s stickers ({len(sticker_ids)} owned):",
        embeds=embeds,
    )


#___________equip_sticker_________________
@bot.command(name="equipstr",aliases=["es"])
async def equip_str(ctx, str_id: int, slot: int):
    user_id = ctx.author.id

    if not coins.user_exists(user_id):
        await ctx.reply("😢 You don't have an account.\nUse `e start` first.")
        return
    coins.add_xp(user_id,2)
    if slot not in (1, 2, 3):
        await ctx.reply("😅 Slot must be **1**, **2**, or **3** — e.g. `e equip_str 5 2`.")
        return

    sticker = coins.get_str(str_id)
    if sticker is None:
        await ctx.reply("😅 That sticker doesn't exist.")
        return

    if not coins.owns_sticker(user_id, str_id):
        await ctx.reply("😏 You don't own that sticker yet — try `e buy_str` first.")
        return

    coins.update_str_slot(user_id, slot, str_id)

    embed = discord.Embed(
        title="✅ Sticker equipped!",
        description=f"🏷 **{sticker['name']}** is now equipped in slot **{slot}**.",
        color=discord.Color.green(),
    )
    embed.set_thumbnail(url=sticker["url"])

    await ctx.reply(embed=embed)

#_________shop str___________________________________
@bot.command(name="shopsticker",aliases=["shopstr","s_str"])
async def shop_str(ctx):

    # ---------------- BUTTONS ----------------

    previous_button = discord.ui.Button(
        label="Previous",
        style=discord.ButtonStyle.gray,
        emoji="⬅️"
    )

    next_button = discord.ui.Button(
        label="Next",
        style=discord.ButtonStyle.gray,
        emoji="➡️"
    )

    view = discord.ui.View()

    view.add_item(previous_button)
    view.add_item(next_button)


    # ---------------- PAGE 1 ----------------
    page = 1
    page1 = discord.Embed()
    page1.set_image(
        url="https://media.discordapp.net/attachments/1524747897864978583/1532761416199569459/image.png?ex=6a6e06ce&is=6a6cb54e&hm=73bc03d50d55792bc8457579f397d4383362d134bfe914c85dca6e0f84dbad5d&=&format=webp&quality=lossless&width=485&height=693")



    # ---------------- PAGE 2 ----------------

    page2 = discord.Embed()

    page2.set_image(
        url="https://media.discordapp.net/attachments/1524747897864978583/1532758532427092078/image.png?ex=6a6e041f&is=6a6cb29f&hm=8c9429f1a88a7ca0007573132f608171c56e167060101bcbb5cba28bd125e1ec&=&format=webp&quality=lossless&width=485&height=693"
    )
    #________page 3____________________
    page3 = discord.Embed()

    page3.set_image(url="https://media.discordapp.net/attachments/1524747897864978583/1533295453473345779/image.png?ex=6a6ff82b&is=6a6ea6ab&hm=f891c0f8b3839df9f90948b8f23a42e822eaf37ed6b4d86824a16e549b1a1ce3&=&format=webp&quality=lossless&width=469&height=670")

    # ---------------- NEXT ----------------
    page = 1

    async def next_callback(interaction):
        nonlocal page
        page += 1
        if page == 2:
            page2.set_footer(text="Page [ 2|3 ]")
            await interaction.response.edit_message(
            embed=page2,
            view=view
        )
        elif page == 3:
            page3.set_footer(text="Page [ 3|3 ]")
            await interaction.response.edit_message(
            embed=page3,
            view=view
        )
        elif page == 1:
            page1.set_footer(text="Page [ 1|3 ]")
            await interaction.response.edit_message(
            embed=page1,
            view=view
        )




    # ---------------- PREVIOUS ----------------

    async def previous_callback(interaction):
        nonlocal page
        page -= 1
        if page == 1:
            page1.set_footer(text="Page [ 1|3 ]")
            await interaction.response.edit_message(
            embed=page1,
            view=view
        )
        elif page == 2:
            page2.set_footer(text="Page [ 2|3 ]")
            await interaction.response.edit_message(
            embed=page2,
            view=view
        )
        elif page == 3:
            page3.set_footer(text="Page [ 3|3 ]")
            await interaction.response.edit_message(
            embed=page3,
            view=view
        )


    # Connect buttons
    next_button.callback = next_callback
    previous_button.callback = previous_callback

    # Send ONLY ONCE
    await ctx.send(
        embed=page1,
        view=view
    )




#LIST OF URL OF STR AND LIST OF WALLPAPAER URL
#________________LEADERBOARD______________
@bot.command(name="leaderboard",aliases=["lb","rank"])
async def lb(ctx):

    users = coins.leaderboard()

    message = ""
    embed = discord.Embed(
        title = " -----------__LEADER BOARD__------------- ",
        description=message,
        color=discord.Color.blue()
    )
    for i, user in enumerate(users, start=1):
        message += f"{i}. <@{user[0]}> - 💰 {user[1]}\n"
    await ctx.reply(f"__LEADERBOARD__\n{message}")


# #_________________INVENTARY________
@bot.command(name="inventory",aliases=["inv"])
async def inv(ctx):
    name = ctx.author.id
    if not coins.user_exists(name):
        await ctx.reply("😢you ddin't had an account to create it use `e start`")
        return
    coins.add_xp(name,2)
    inv = coins.get_inventory(name)
    total = 0
    wp_total = 0
    for i in inv :
        for j in i :
            if j == "wp":
                wp_total += i[3]
            elif j == "str":
                total += i[3]


    data = coins.get_user(name)
    embed = discord.Embed(
            title = f"🧰 {ctx.author.display_name}'s Inventory ",
            description=f"owns\n",
        color=discord.Color.blue()
    )
    embed.set_author(name=ctx.author.display_name,icon_url=ctx.author.display_avatar.url)
    embed.add_field(name="Stickers👾", value=f"**{total}**", inline=True)
    embed.add_field(name="Coins🪙", value=f"**{data[1]}**", inline=True)
    embed.add_field(name="wallpaper🖼️", value=f"**{wp_total}**", inline=True)
    embed.set_footer(text="by emobot")
    await ctx.reply(embed=embed) 



# _______________WORK___________________________
@bot.command()
async def work(ctx):
    user_id = ctx.author.id

    if not coins.user_exists(user_id):
        await ctx.reply("😢 First create an account using `e start`.")
        return
    coins.add_xp(user_id,2)
    data = coins.get_user(user_id)
    # data = (id, coins, xp, str_id, wp_id, lt_work, last_daily, last_cf)
    balance = data[1]
    last_work_iso = data[7]  # lt_work — was wrongly read from data[4] (wp_id) before

    work_cooldown = coins(last_work_iso)

    if not work_cooldown.can_work():
        seconds = work_cooldown.remaining_work()
        await ctx.reply(f"⏳ Please wait **{seconds}** seconds before working again.")
        return


    if balance < 0:
        balance = 0
        coins.update_coins(user_id, balance)

    reward = random.randint(200, 3500)
    new_balance = balance + reward
    coins.update_coins(user_id, new_balance)

    # only award xp on an actual successful work, not on every attempt
    coins.add_xp(user_id)

    work_cooldown.set_time(datetime.now())
    coins.update_last_work(user_id, work_cooldown.time_iso)

    await ctx.reply(f"💼 You worked hard and earned **{reward}** coins!")




# ___________DAILY_______________________
@bot.command()
async def daily(ctx):
    user_id = ctx.author.id

    if not coins.user_exists(user_id):
        await ctx.reply("😢 First create an account using `e start`.")
        return
    coins.add_xp(user_id,2)
    data = coins.get_user(user_id)
    # data = (id, coins, xp, str_id, wp_id, lt_work, last_daily, last_cf)
    balance = data[1]
    last_daily_iso = data[8]  # last_daily — was wrongly read from data[5] (lt_work) before

    daily_cooldown = coins(last_daily_iso)

    if not daily_cooldown.can_daily():
        hours = daily_cooldown.remaining_daily()
        await ctx.reply(f"⏰ Please wait **{hours:.1f}** hours before claiming again.")
        return

    # If the balance somehow went negative, reset it before paying out
    # (old code set the balance to abs(balance), which would have turned
    # a debt into a matching positive amount instead of clearing it)
    if balance < 0:
        balance = 0
        coins.update_coins(user_id, balance)

    reward = random.randint(200, 50000)
    new_balance = balance + reward
    coins.update_coins(user_id, new_balance)

    # only award xp on an actual successful claim, not on every attempt
    coins.add_xp(user_id)

    daily_cooldown.set_time(datetime.now())
    coins.update_last_daily(user_id, daily_cooldown.time_iso)

    await ctx.reply(f"💳 You claimed your daily reward and earned **{reward}** coins!")



#_____________pay_________
@bot.command(name="pay",aliases=["send","give","transfer"])
async def pay(ctx, member: discord.Member, num: int):
    coins.ensure_tables()
    name = ctx.author.id
    send_name = member.id

    if member == ctx.author:
        await ctx.reply("❌ You can't pay yourself.🤨")
        return

    if num <= 0:
        await ctx.reply("❌ Enter a valid amount.🤨")
        return
    
    if not coins.user_exists(name):
        await ctx.reply("😢you didn't had an account to create it use`e start`")
        return
    coins.add_xp(name,2)
    if not coins.user_exists(send_name):
        coins.add_user(send_name,0,0,0,0,"","","")
    data = coins.get_user(name)
    if data[1] < 0 :
        fu = abs(data[1])
        coins.update_coins(name,fu)
    coins.add_xp(name)
    if data[1] < num:
        await ctx.reply(
            f"{ctx.author.display_name} is poor hihi ^^ 😁,\n"
            "😢Your balance is too low to pay another {member.display_name}😅."
        )
        return
    data2 = coins.get_user(send_name)
    cash2 = data2[1]
    cash = data[1]
    cash -= num
    cash2 += num
    coins.update_coins(name,cash)
    coins.update_coins(send_name,cash2)

    await ctx.reply(
        f"📤**{ctx.author.display_name}** 💸 transferred **{num}** coins to **{member.display_name}** 💰"
    )


# _______________ buy stickers ___________________
@bot.command(name="buysticker",aliases=["buystr"])
async def buy_str(ctx, str_id: int):
    user_id = ctx.author.id

    if not coins.user_exists(user_id):
        await ctx.reply("😢 You don't have an account.\nUse `e start` first.")
        return
    coins.add_xp(user_id,5)
    sticker = coins.get_str(str_id)
    if sticker is None:
        await ctx.reply("😅 That sticker doesn't exist.")
        return

    if coins.owns_sticker(user_id, str_id):
        await ctx.reply("😏 You already own this sticker.")
        return

    stickers = coins.get_user_stickers(user_id)
    if len(stickers) >= 3:
        await ctx.reply(
            "😅 Your sticker inventory is full.\n"
            "Delete one before buying another."
        )
        return

    data = coins.get_user(user_id)
    balance = data[1]

    if balance < sticker[2]:
        await ctx.reply(
            "😢 You don't have enough coins.\n"
            "Use `e work`, `e daily` or `e coinflip`."
        )
        return

    balance -= sticker[2]
    coins.update_coins(user_id, balance)
    coins.add_inventory(user_id, "str", sticker[0], 1)

    # only award xp on an actual successful purchase, not on every attempt
    coins.add_xp(user_id)

    embed = discord.Embed(
        title="🎉 You bought a new sticker!",
        description=(
            f"🆔 Sticker ID : **{sticker[0]}**\n"
            f"🏷 Name : **{sticker[1]}**\n"
            f"💰 Price : **{sticker[2]}** coins"
        ),
        color=discord.Color.blue(),
    )
    embed.set_thumbnail(url=sticker[3])

    await ctx.reply(embed=embed)







# ________________20 emotions commands ___________________________________
@bot.command()
async def smile(ctx):
    name = ctx.author.display_name
    embed =  discord.Embed(title=f"{name} is smiling",color=discord.Color.blue())
    list = ["https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZG54ajBjaG9kMWs0N29meHFlbjZteDY2dm52dzVlejZpNjEydWI0byZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/10t57cXgo7x5kI/giphy.gif","https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExZno3dGFtM2MyMjlraXg0OGg2NjR1aTNld2MyMmRoa2dpdDlvMnRibSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/h1N8JV9p3FqgM/giphy.gif","https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExajd2Mzd0c3FtOHZjaWZma2ltaDVsZjE3bHhma2F4eXI1eXRmdTduaiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/T7Qx28nEdo9NK/giphy.gif","https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXk0ZHNscDF5a3Q5YWFkODRrcTZ0ZXJjcDZ4anY5dmVzdnY0ajVpaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/A0Zt7yuDULiy4ofmVD/giphy.gif"]
    val = random.choice(list)
    embed.set_image(url=val)
    await ctx.reply(embed=embed)

MOOD_GIFS = {
    "happy": [
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExdXpjcjk0ZGk0djZnaDB6cDE4MTd1dHN0eDczM2dsenZ1Nmt1M2V2dyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/mhfqfSii6aBk3AUWY3/giphy.gif",
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExanJ2ZDYyaXZocXFiZGt1ZXZ5eWE2ZWVjNmNuYXppM2l0eDg5OTB1cSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/kalDkPUTRfV4XFEvJ5/giphy.gif",
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExZHloOWFhYXp0eGljc2dzdHdmbG84YjBzNWY4YXhsODVuanF6djRmeSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/zZC2AqB84z7zFnlkbF/giphy.gif",
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExemIwbzdsaGdiNHdsZzB6dnlzcjhpemljMmt3eTVpMXBnaTZ2YzNpNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/6GuZHgYsH9taU/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExeWM0bjE1am5sczlodXZiMTY2Y3M2cG1md2hteDAxNG8xbzE4c2s3NSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1o1vdFk0DMR5VJ1GBy/giphy.gif",
    ],
    "excited": [
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExemRrNnNva24xMGxtNjd6bmJxeGIzcHhsanV6NGp2aWM2dDRoOWpnbSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/AkFEmElfAaIbljf99G/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ3Aybjdoam0zYjV1cmhvNDFoY2Y1ZzhqZTB1dzFjZXhpcXdzOWh5OSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/qkbCdaJWt2STm/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExbm15YzFkemlqamRrMWFscWE3dDFnenZzYXAxOWkxamRna2E3aHRkYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Y64uBZCJsl0TS/giphy.gif",
    ],
    "laughing": [
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExbmd3NmFtYng0aDB3YTFpeXp0dGl6emlqeXU4MzhoZjlhMm5xOWVzcCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/B1JKtacZXunqU/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZDd6bXkwZnZyN3ExNzV4YnF5ZGFncHZqN2F6dDRrMGJ2eWprcGN0NSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/XLMakNrymMwUg/giphy.gif",
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExc2EzdGFzdm5hMXA2eGFoMHlrdXJzbzY5MWM3ZWg4c3RuOXdiY29pdSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/0SVAVxeJsnJ1WRMIPX/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExczdxd21kczViaTR0MTZ6bm0yMzZubXo2MGJ5cmtpOHp4NDFiMmoxZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/YX05pEyqtw38Kr80pH/giphy.gif",
    ],
    "playful": [
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExd2RobGNxbTNpMDg2MzJ2cHo2ZzNkb2w3dnJ2cXdrN3N0aHd3cmhwNSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/rMvQiXOggpEDxeE4Zv/giphy.gif",
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExcTF3NDFwOW1ybzN3YWJ3cTRnanJocWRpNmhveDI5NGc2aThicHBxYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/f5T1Wp8NZiz3tkM6mb/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnpoenpzMjF4d3Vldzd1bjk5eHE2MjQydjdqbm1qNzNlZGtiaGxseSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/VbKLOdvCxBFNZpYvhL/giphy.gif",
    ],
    "proud": [
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHhha25rY3Y0dTJjMm9rM3pmN2Zlc2pseG1uZGZteDR4ZW0zN3QzMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jcQqiy9IN7XOosvNeS/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExa3Yzd3J2Y25pMnRhbzI1ZGdjZjVkMmJ5ejFiNW5lNXB6bGF6NzV2ZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ZxKDG0lGPHiTJK5TJV/giphy.gif",
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmZ1Nmk4ZTNxbjczNWs4OGVrZDczYnF0ZTJjOXliNm9xcGNjOTBtNCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Vg2TAoPzDstzy/giphy.gif",
    ],
    "confident": [
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExejRzdGhic2Vic2YzemtsMmtwbHJvOGVrN3UwOW00NzIycWlrbjk4biZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/RcMcV5viJWmaY/giphy.gif",
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZHczbDlhaTVybDZ0a2phb2NkYjgwYXdndDBwZzV0amNveTZvbHE2aSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/lcZ6Gn8asVHiGizJn7/giphy.gif",
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExdjl0ejh6MXU3ajhmODQxY25nZXNrajJlNzI0eHB4OXhsbmhveDk0aSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/hpfkNVYrF7x8CTJLeC/giphy.gif",
    ],
    "relieved": [
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDE2MWVkY2V0ZWwxdmhvMDJvNzduZ3NwaWRrYXFmeWM1dXRvNXAyOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/6XP6NJ9OQaHGvYYcgB/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXhkM3RpNGdlaWlkdno5Y2h1anoydGtndWZxYngwb2dxZGU0bnZqbiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/dzTC9FaH4W28rVQN4n/giphy.gif",
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdzJteGpsMW85YWU1Z3h5cWppZzlyajJzMXRvOWtpMGswZHJ5MzdhaSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/34doY355G0vKzaSEMs/giphy.gif",
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ21za2lmazVkMnV3YjZxbDFkaHBtM3RweWdpaDhmbXNsYW02enU1diZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1zmBHwwzLNbpbgnO0a/giphy.gif",
    ],
    "shy": [
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExZXpsaDJyODB2dDU5dzQyYWNoYnNhNDZydTN0MWE4Z3FneTJ6cnQzOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/HPI9m7McNPGN2/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHF3a2h0bmRsNTQwNjg4cnd4d3ZnbzUyODZsajBjYTZvcnhxN2Y1ZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/vIIbrC80HHN7O/giphy.gif",
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ3NybzdmZXV2YzY4MmQ4bm5qaWY3Z2JqdWVqY2VrazE3bGUxb3AxdyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/aCSURh6OnUyXdOuYcq/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExNjh4NWRkcm9lYmhqdjQwbzZ5NXkxdjA3Y2J0MzJwN20zaWN5MjJ0YSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/J509hr2j0oMejwlKOS/giphy.gif",
    ],
    "embarrassed": [
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExeHo1d2lzaHdmaGxtNTlvOHJjM3c2ajkyaXJ4bHZkYzBsc2tkeDd0ZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3ohs7KViF6rA4aan5u/giphy.gif",
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExb2tsd2QzMzdxeTZ3bmNsMm5udGxybzV3MHpsanM5MDZ0OHh3a2lxZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/njPdRtrrdyoVO/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExcnFzOXo4b3ZyOHF5bXF3N2tidGo4bjVpOHlleHlyZjlpdm1hNHY4YiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/eQyIoaAWyBS35RHXkO/giphy.gif",
    ],
    "flustered": [
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3ljbWI5bmYwbHdxYTFoNnFnZWlnN2pqd3N0d21mNWNlZWFiODIyNSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/eo8jQ8FTM8nao/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExYzBoOGlqMmVjYWZwanl4eXJlNWF5djFxaXdzdTNlc21xNWFqZmJtciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/O3xLh8DF2UoCWKDo3u/giphy.gif",
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWpwcTFlZHJzdjhuanJnOWRwNXlzMXE4Z2l1bXAwYjJjOXc0ODFkaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/GefMxpASbK7ZmEq75t/giphy.gif",
    ],
    "awkward": [
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExaWppdG1oY2I0N3lwOGZvZjczbHNmMHZjaWI4aWhvZml4MzhkNWJzaiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jGZ0jiObChGytinmSL/giphy.gif",
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExbml0bmI3cmg4ZTg5azV3bTIydnVwdzdsanhoOXBsYTI3NGdneGh4aSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/bUipDsg3CwKHK0Vstv/giphy.gif",
    ],
    "nervous": [
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExdnVyeTNsNnMwdzQ2MGUzaWx5MDdlZW02cDk5NjFiamR0YWdjcHliYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/bEVKYB487Lqxy/giphy.gif",
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHg3czg1MWl4M2YwOGZqOXBldHZ3MG56d3FybG94NjdhM3Rrc2xhcSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/HThocT5vEPT9K/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ3dvMHE3dDIzNGpudGh6YWRmeGR1NmlxazE0NW1ibmszcm56MnB6aCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Am92Q8PQvAUJotvBgL/giphy.gif",
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnhrcGJyNDJ1c28xb2dlYzVsYW4xdHpzZzN0bDg4MTVvdDMwdzI1diZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/lKdtLHHuBImccjBfmq/giphy.gif",
    ],
    "bashful": [
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZjl2cWZudzI3d3l5NmRoemFrenA2YnJjYWt2MXhzZHNzaG1qemo2cyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/dKOpEntuJg4M/giphy.gif",
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExZW5pMGpqNWF4aDF1OWtodnJxdTk0bTh6czR2bDV1OGZ5emcyNTB3eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1gbQIeNzZxcSk/giphy.gif",
    ],
    "blush": [
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExMXdkZmQ2enYyM3RzYmVnbHZ5ajlxeHo1dDV2Z3dyajNydjl6c2o0NyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Oa9hTEQIlDtIlOXJXs/giphy.gif",
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExMXY3ZWR1aG1uaTJwNmkxOGxuN3JmNGxua3pscmdod3VpZzBramljbCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xF9TTmQCvpp91kmdJm/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExYnJnaDU0dTk3dDFqNGN6NnFwZjkzNGIxajd5a2E5Z3M1ZDByZmFvMiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/V216rdoG6TUVvXA0Tb/giphy.gif",
    ],
    "admiring": [
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExc2Vid290NGJnYnFjNHVnMmhsNXFndGs2bXVrYTNoZHB3d3QwNHB4NCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/YxKXWOhTSq8I14NKEn/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDkyZzQ0MDVhNnM3cG95YjUzNWtvMWs4MnllOWVneGp5cDhwNWxpaiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Y4P943aTJRCYfperyN/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbjY3ZzgwaDV4dzQwdzR4aHR5Zjl6cnhtc256azd6dDZ1eGNpZHZ6NSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/X3r0rwkBJdxAhVbYLn/giphy.gif",
    ],
    "grateful": [
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3Jqa28wN202aGgxc3g4eG40MjVnN3lwN2pob3Z5ejdkY2psb2NxeCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oz8xIsloV7zOmt81G/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExd3Y1NnZoNWFoOG8xZ2MzOW92c2I2dHVoajB5ZzB5NmEyNXF4d2FyaSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/yE288o70sguDoB30F5/giphy.gif",
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ2lnd3c4bXVsanp3N2M4MzZjMDE1cHAwN2xmbTdsOTllNjR2eWZoYSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l0MYy2GInHvLon2jS/giphy.gif",
    ],
    "sad": [
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWVtbm1hc3dsOXVmYm1lZGNtdGMxYjc0ZjNvb3doZ2cxMmxobHhycyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LdMWg0xQTfmcpFF5Yt/giphy.gif",
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExZHU1NzBmd3BicnFtcXN0Ymk5M3VnaDAyOTRrOGwxM2M3NG5hNmgzciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/TZBED1pP5m8N2/giphy.gif",
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHQ0bzFjOTh3dThrMzY3bWFoeHRnbzkxZGhuNnlwOXA5dGh4emIzbCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ujZtlj1Y7wXyE/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHA0NXJhazNyM2hvYjdzdmVjbHhkcnFqbmF3ZjZ4dWtuazBlN3czeiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Y4z9olnoVl5QI/giphy.gif",
    ],
    "cry": [
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExc3ozN3AzZ3I1emdzZGhyZjJraXliZGlxZ2ljdnRrazZxaGNpdmdwZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/BvASeTeFlWnODXGzhH/giphy.gif",
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHo0djc0dXdoc290ZGQwaXVpNzd6bmE4bWQ4dmQ1bDN5ang0MWV6eSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/AbQ8FvqjQ4lVOhkrvi/giphy.gif",
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExejUwYnplMXVtM2txZHkyb2t2czk3a3VsYnZ0azNsMnNqcHZzbmx4cSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/8YutMatqkTfSE/giphy.gif",
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExNGo0bjVocDNza3hjeGU3M3E3OW05am02MzZoNm42aDV5ZzRiMHo0ciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/q1R1ZiUskINVOn6bz3/giphy.gif",
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExMzVyNmQ4dDM5NjY1OXN1MWFwaXhzbTNzNHcxMTV4bGk3N2hvZjRxOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/cUl8fuIG75QWs/giphy.gif",
    ],


    "excited": [
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExemRrNnNva24xMGxtNjd6bmJxeGIzcHhsanV6NGp2aWM2dDRoOWpnbSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/AkFEmElfAaIbljf99G/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ3Aybjdoam0zYjV1cmhvNDFoY2Y1ZzhqZTB1dzFjZXhpcXdzOWh5OSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/qkbCdaJWt2STm/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExbm15YzFkemlqamRrMWFscWE3dDFnenZzYXAxOWkxamRna2E3aHRkYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Y64uBZCJsl0TS/giphy.gif",
    ],
    "laughing": [
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExbmd3NmFtYng0aDB3YTFpeXp0dGl6emlqeXU4MzhoZjlhMm5xOWVzcCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/B1JKtacZXunqU/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZDd6bXkwZnZyN3ExNzV4YnF5ZGFncHZqN2F6dDRrMGJ2eWprcGN0NSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/XLMakNrymMwUg/giphy.gif",
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExc2EzdGFzdm5hMXA2eGFoMHlrdXJzbzY5MWM3ZWg4c3RuOXdiY29pdSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/0SVAVxeJsnJ1WRMIPX/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExczdxd21kczViaTR0MTZ6bm0yMzZubXo2MGJ5cmtpOHp4NDFiMmoxZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/YX05pEyqtw38Kr80pH/giphy.gif",
    ],
    "playful": [
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExd2RobGNxbTNpMDg2MzJ2cHo2ZzNkb2w3dnJ2cXdrN3N0aHd3cmhwNSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/rMvQiXOggpEDxeE4Zv/giphy.gif",
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExcTF3NDFwOW1ybzN3YWJ3cTRnanJocWRpNmhveDI5NGc2aThicHBxYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/f5T1Wp8NZiz3tkM6mb/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnpoenpzMjF4d3Vldzd1bjk5eHE2MjQydjdqbm1qNzNlZGtiaGxseSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/VbKLOdvCxBFNZpYvhL/giphy.gif",
    ],
    "proud": [
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHhha25rY3Y0dTJjMm9rM3pmN2Zlc2pseG1uZGZteDR4ZW0zN3QzMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jcQqiy9IN7XOosvNeS/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExa3Yzd3J2Y25pMnRhbzI1ZGdjZjVkMmJ5ejFiNW5lNXB6bGF6NzV2ZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ZxKDG0lGPHiTJK5TJV/giphy.gif",
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmZ1Nmk4ZTNxbjczNWs4OGVrZDczYnF0ZTJjOXliNm9xcGNjOTBtNCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Vg2TAoPzDstzy/giphy.gif",
    ],
    "confident": [
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExejRzdGhic2Vic2YzemtsMmtwbHJvOGVrN3UwOW00NzIycWlrbjk4biZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/RcMcV5viJWmaY/giphy.gif",
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZHczbDlhaTVybDZ0a2phb2NkYjgwYXdndDBwZzV0amNveTZvbHE2aSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/lcZ6Gn8asVHiGizJn7/giphy.gif",
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExdjl0ejh6MXU3ajhmODQxY25nZXNrajJlNzI0eHB4OXhsbmhveDk0aSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/hpfkNVYrF7x8CTJLeC/giphy.gif",
    ],
    "relieved": [
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDE2MWVkY2V0ZWwxdmhvMDJvNzduZ3NwaWRrYXFmeWM1dXRvNXAyOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/6XP6NJ9OQaHGvYYcgB/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXhkM3RpNGdlaWlkdno5Y2h1anoydGtndWZxYngwb2dxZGU0bnZqbiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/dzTC9FaH4W28rVQN4n/giphy.gif",
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdzJteGpsMW85YWU1Z3h5cWppZzlyajJzMXRvOWtpMGswZHJ5MzdhaSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/34doY355G0vKzaSEMs/giphy.gif",
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ21za2lmazVkMnV3YjZxbDFkaHBtM3RweWdpaDhmbXNsYW02enU1diZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1zmBHwwzLNbpbgnO0a/giphy.gif",
    ],
    "shy": [
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExZXpsaDJyODB2dDU5dzQyYWNoYnNhNDZydTN0MWE4Z3FneTJ6cnQzOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/HPI9m7McNPGN2/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHF3a2h0bmRsNTQwNjg4cnd4d3ZnbzUyODZsajBjYTZvcnhxN2Y1ZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/vIIbrC80HHN7O/giphy.gif",
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ3NybzdmZXV2YzY4MmQ4bm5qaWY3Z2JqdWVqY2VrazE3bGUxb3AxdyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/aCSURh6OnUyXdOuYcq/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExNjh4NWRkcm9lYmhqdjQwbzZ5NXkxdjA3Y2J0MzJwN20zaWN5MjJ0YSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/J509hr2j0oMejwlKOS/giphy.gif",
    ],
    "embarrassed": [
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExeHo1d2lzaHdmaGxtNTlvOHJjM3c2ajkyaXJ4bHZkYzBsc2tkeDd0ZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3ohs7KViF6rA4aan5u/giphy.gif",
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExb2tsd2QzMzdxeTZ3bmNsMm5udGxybzV3MHpsanM5MDZ0OHh3a2lxZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/njPdRtrrdyoVO/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExcnFzOXo4b3ZyOHF5bXF3N2tidGo4bjVpOHlleHlyZjlpdm1hNHY4YiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/eQyIoaAWyBS35RHXkO/giphy.gif",
    ],
    "flustered": [
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3ljbWI5bmYwbHdxYTFoNnFnZWlnN2pqd3N0d21mNWNlZWFiODIyNSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/eo8jQ8FTM8nao/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExYzBoOGlqMmVjYWZwanl4eXJlNWF5djFxaXdzdTNlc21xNWFqZmJtciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/O3xLh8DF2UoCWKDo3u/giphy.gif",
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWpwcTFlZHJzdjhuanJnOWRwNXlzMXE4Z2l1bXAwYjJjOXc0ODFkaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/GefMxpASbK7ZmEq75t/giphy.gif",
    ],
    "awkward": [
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExaWppdG1oY2I0N3lwOGZvZjczbHNmMHZjaWI4aWhvZml4MzhkNWJzaiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jGZ0jiObChGytinmSL/giphy.gif",
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExbml0bmI3cmg4ZTg5azV3bTIydnVwdzdsanhoOXBsYTI3NGdneGh4aSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/bUipDsg3CwKHK0Vstv/giphy.gif",
    ],
    "nervous": [
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExdnVyeTNsNnMwdzQ2MGUzaWx5MDdlZW02cDk5NjFiamR0YWdjcHliYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/bEVKYB487Lqxy/giphy.gif",
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHg3czg1MWl4M2YwOGZqOXBldHZ3MG56d3FybG94NjdhM3Rrc2xhcSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/HThocT5vEPT9K/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ3dvMHE3dDIzNGpudGh6YWRmeGR1NmlxazE0NW1ibmszcm56MnB6aCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Am92Q8PQvAUJotvBgL/giphy.gif",
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnhrcGJyNDJ1c28xb2dlYzVsYW4xdHpzZzN0bDg4MTVvdDMwdzI1diZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/lKdtLHHuBImccjBfmq/giphy.gif",
    ],
    "bashful": [
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZjl2cWZudzI3d3l5NmRoemFrenA2YnJjYWt2MXhzZHNzaG1qemo2cyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/dKOpEntuJg4M/giphy.gif",
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExZW5pMGpqNWF4aDF1OWtodnJxdTk0bTh6czR2bDV1OGZ5emcyNTB3eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1gbQIeNzZxcSk/giphy.gif",
    ],
    "blush": [
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExMXdkZmQ2enYyM3RzYmVnbHZ5ajlxeHo1dDV2Z3dyajNydjl6c2o0NyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Oa9hTEQIlDtIlOXJXs/giphy.gif",
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExMXY3ZWR1aG1uaTJwNmkxOGxuN3JmNGxua3pscmdod3VpZzBramljbCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xF9TTmQCvpp91kmdJm/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExYnJnaDU0dTk3dDFqNGN6NnFwZjkzNGIxajd5a2E5Z3M1ZDByZmFvMiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/V216rdoG6TUVvXA0Tb/giphy.gif",
    ],
    "admiring": [
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExc2Vid290NGJnYnFjNHVnMmhsNXFndGs2bXVrYTNoZHB3d3QwNHB4NCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/YxKXWOhTSq8I14NKEn/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDkyZzQ0MDVhNnM3cG95YjUzNWtvMWs4MnllOWVneGp5cDhwNWxpaiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Y4P943aTJRCYfperyN/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbjY3ZzgwaDV4dzQwdzR4aHR5Zjl6cnhtc256azd6dDZ1eGNpZHZ6NSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/X3r0rwkBJdxAhVbYLn/giphy.gif",
    ],
    "grateful": [
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3Jqa28wN202aGgxc3g4eG40MjVnN3lwN2pob3Z5ejdkY2psb2NxeCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oz8xIsloV7zOmt81G/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExd3Y1NnZoNWFoOG8xZ2MzOW92c2I2dHVoajB5ZzB5NmEyNXF4d2FyaSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/yE288o70sguDoB30F5/giphy.gif",
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ2lnd3c4bXVsanp3N2M4MzZjMDE1cHAwN2xmbTdsOTllNjR2eWZoYSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l0MYy2GInHvLon2jS/giphy.gif",
    ],
    "sad": [
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWVtbm1hc3dsOXVmYm1lZGNtdGMxYjc0ZjNvb3doZ2cxMmxobHhycyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LdMWg0xQTfmcpFF5Yt/giphy.gif",
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExZHU1NzBmd3BicnFtcXN0Ymk5M3VnaDAyOTRrOGwxM2M3NG5hNmgzciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/TZBED1pP5m8N2/giphy.gif",
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHQ0bzFjOTh3dThrMzY3bWFoeHRnbzkxZGhuNnlwOXA5dGh4emIzbCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ujZtlj1Y7wXyE/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHA0NXJhazNyM2hvYjdzdmVjbHhkcnFqbmF3ZjZ4dWtuazBlN3czeiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Y4z9olnoVl5QI/giphy.gif",
    ],
    "cry": [
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExc3ozN3AzZ3I1emdzZGhyZjJraXliZGlxZ2ljdnRrazZxaGNpdmdwZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/BvASeTeFlWnODXGzhH/giphy.gif",
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHo0djc0dXdoc290ZGQwaXVpNzd6bmE4bWQ4dmQ1bDN5ang0MWV6eSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/AbQ8FvqjQ4lVOhkrvi/giphy.gif",
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExejUwYnplMXVtM2txZHkyb2t2czk3a3VsYnZ0azNsMnNqcHZzbmx4cSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/8YutMatqkTfSE/giphy.gif",
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExNGo0bjVocDNza3hjeGU3M3E3OW05am02MzZoNm42aDV5ZzRiMHo0ciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/q1R1ZiUskINVOn6bz3/giphy.gif",
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExMzVyNmQ4dDM5NjY1OXN1MWFwaXhzbTNzNHcxMTV4bGk3N2hvZjRxOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/cUl8fuIG75QWs/giphy.gif",
    ],
    "lovely": [
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExcmd0c3d3ZnJxbmk4ejZvbm0yMXJiaWFmdmZhNTZmeHNsOXZrNzZkaiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/u62ibpUyRSvJ0PyXJU/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExdGlpYTJoMnVhNTM5ZHg1NWtpOWdmOXlyMjRhZnNyeXA3cXN2dmRmbCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/EkOoatbIcbmmHiU7Mz/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ3Q4azhqZ3A4OW9ibjVtNTZqdGJleTliZmlucm41ejk1czl3ejhvdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/W9MrfVxE4s2Zi/giphy.gif",
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExeWNrcXQ2dGI3NWV0Z2oydWZlZ2I4dnYxdzc2eDg1OWI5ZjYybHJtMyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/iHcRqdoTI3MZO/giphy.gif",
    ],
    "bored": [
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnRkdm9wZTlkYWZsejY5YzJ4b3RuYWNkZ3c4cXI0bHR2OXJzdjE3YSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/iIJYWJPzmjlJu/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnVuOWtvamZ1dGFyNXhyeHd6bjBudHB0dWgxdjJzZ2ttdGJnejJsdCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/CkELdepdNFEunaYl86/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExY2g1NGV2bDdhdzFteHF5bzkwYWoxY2d4aGpwMmk3dHIzZnE1cWRiNCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/a9lgeWGF7Ysrm/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExajNnOGd5YTh3am9jbnlidjZ2MjU3MzI0eDY2ZzVpbzVwN2RjZm8yOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/aTCC28zhBUw9y/giphy.gif",
    ],
    "dance": [
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExejUwdmluaGQxaHFxYWhid2g5eWJrb3NteWtldWJ5dnR4cTZxZnVwdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/b7l5cvG94cqo8/giphy.gif",
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExZHQ1Z2trY25icXV1MmViZHZhYmdoMDJmM2QxZ2lwM2FxOTdhZWhhYiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/KkF4Ts9p08J1K/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ3F0a201N211MWdvc2pjajA1bGRrMXk2ZXdqeHRnYXV4ZDhmdmJnOSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/FM57qpxeflq5Woi0Bj/giphy.gif",
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExaW8wcWR4MGwyZDJrbmx5aWI0bWRwZ3R6ODliMjBoNDdiNjUyZGs0NCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/frNW1o4ujUqifFEjO0/giphy.gif",
    ],
    "angry": [
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExM2VhcG1majAwYjBxa2loaDBpNmJta3h3aGptNHd6bnM4N2g4ZHU5MiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/oQrIYTXQeju2rVaEGQ/giphy.gif",
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWJlczZvNDdqZnRoNHVxMHV0cWZlcjkzZm52eDNxcmlrY2JpOWc2NCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/VcF2XV5YXuzw44fr0R/giphy.gif",
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExajdjaTQ5aG1zaTd5anI4aXUxYjd1M252YTNobnhwYnNtdTVoYjdvYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/9w9Z2ZOxcbs1a/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExZGkxbWVsbm5wY2pmbHhueGUwOXpzaGw5bnU0bzNxem1lNWU3Ym9scyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/A3Sf1bY27bvYe8MkMT/giphy.gif",
    ],
    "surprised": [
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExem5nZ2ZtdmVtemVycThmdHlhcnJudjgzcWozM2MyYmZ6enZ1eWpuaiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/G0eIlHC2q7fWH67TpB/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExdTQzY3RoeG1vZzBidWJsdHlzNTh6MWk1MjV0enppNjA5bmxzMjl3eSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/GRk3GLfzduq1NtfGt5/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGIxcGY3eGN1c3NzczBuZDhoNzRycWlydjV0MXNtdHl4aTFpYXpiYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/NRbR2XH2NAghgScqNJ/giphy.gif",
    ],
    "shocked": [
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExaDZncGMzMmxuZXZuOG5sYjY4cWxwcTJyNjdvcW8wZGRvZmR1ZHFjYSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/135QXxqZ9d0QGk/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExNzQyeTN1ZWJ0anU1bzByNXZ2anYwcTMweXdzdzU3dndkZW5vNW1rNSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Cdkk6wFFqisTe/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXBlYTdyemZ5ang1a3EzejVjOTg5bDRmeDFudDZ5azMzbWN2aTBsYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/IKUsJYoSQ8IRx1wO5R/giphy.gif",
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExemM0N2JsY2Z3dXB3cnEwdmFhcTA0MGwzdWdjbXJtcTI5aHprdXMzZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/UUjkoeNhnn0K4/giphy.gif",
    ],
    "scared": [
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExamQ2dTZ2MTM5bWx2YnYxZThtemphajNyYjB6MXg0YngxZ3pscHhuayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/sZrIqPw81LHEyCyn2q/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXV2MGtnMGU1MmZsM2E4ZXp2Z28zN2R6dmdtcDFjMzJ5cXhlcDNvYSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/UBnPTPzgP2IPUQbsht/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExNGw4ZDdjMnU3N3gwODB3emNuNGRjdDJ4M3A0b3o4OGlnazgzMXE1ZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/MUtyUGQALqjcI/giphy.gif",
        "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHQzd2hxNDhnajdsZDFucTc2dDd6MG8xenlzeHozeGo5N2tiZjFlYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7bugi24hokjYq0Le/giphy.gif",
    ],
    "wow": [
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExdnV1emZjNXZlaDZ4dHA2bG1xdGVueGlxOG00ZmY1ODBrODBld3h4OCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/XMVsIvkUjZUqc/giphy.gif",
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHBzNWNiMDZ6OTE2a3B0cTdxanNidXphcDNnY21zcHp2ZTNpbW14eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26FfanWpoZKKf4efm/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExMml5d3hhZ2hka3dzNGptMXc5eXc3Y2ducTZieTc0ZndvamNrNzQ1eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/pXgjRCtYqYWl7DXSGJ/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExdG1xNXd5c2Y2b2tybWxwamp2cHdpbHFwM3B3OTI5aXYzdHo0dWc4eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/JmUfwENE6i4Jxig27n/giphy.gif",
    ],
    "dead": [
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHdvMnAzejZqNmRzd3l4Y2xha3o1MGllaTZ5bXVtbmlydHA3dHFlayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/yjGdFXbm8KpXF5Xqco/giphy.gif",
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExb3N3eTNlMHloOWQ3MzRkNTBuNTI4azN3NHMzOWNhcDR1MGZrdXZnNSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ZWZMwJtoqAzxS/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGFjOG1ocmswZWM2Y2JseGdkeG16MzlpdjM0NzhxMW12ZGd1dXVjbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/tVxWOUqvcE3II/giphy.gif",
    ],
    "sleepy": [
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExaTAwemI3cGw1cTB2bzRvMWVvbXNuZTVwaHEyY3EybWhhajRhamszZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Tfr91anUahoME/giphy.gif",
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExc3k5aHB3bXg0cmt3cjh1d3ZoOTJydnhjdjQ5c3B5NXdyNXVhZHZkYiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/DRNsbfCHNznxe/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExMW5nMDJmZWp3bDNndHBtY25hNzVpcHNldmlhZzg1NHhka3BibnlrcSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Y1Bl4MvP3fDq/giphy.gif",
    ]
}


def _make_mood_command(mood: str, gif_urls: list):


    @bot.command(name=mood)
    async def mood_command(ctx):
        name = ctx.author.display_name
        embed = discord.Embed(title=f"{name} is {mood}", color=discord.Color.blue())
        embed.set_image(url=random.choice(gif_urls))
        await ctx.reply(embed=embed)

    return mood_command


for _mood, _urls in MOOD_GIFS.items():
    _make_mood_command(_mood, _urls)





# ________________dine__________________

DICE_FACE_IMAGES = {
    1: "https://pixabay.com/images/download/clker-free-vector-images-dice-312625.png",
    2: "https://pixabay.com/images/download/clker-free-vector-images-two-310337_1280.png",
    3: "https://pixabay.com/images/download/clker-free-vector-images-dice-312624_1280.png",
    4: "https://pixabay.com/images/download/clker-free-vector-images-dice-312624_1280.png",  # same as 3 in the original — double check this is the right image
    5: "https://pixabay.com/images/download/clker-free-vector-images-dice-312622.png",
    6: "https://pixabay.com/images/download/clker-free-vector-images-dice-310333_1280.png",
}

ROLLING_GIF = "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3OHdzaGljMGh4aWxxemwyNzM0YzV6amU1YmNmaXhjcjByajV6dDV5dCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/kEhxvWwGBqBOHrMFyS/giphy.gif"  # generic rolling gif shown before the reveal — same one from your original, swap for a real "dice rolling" gif if you have one

# _________________dice____________________
@bot.command(name="dices", aliases=["dice", "guessnumber", "playdice"])
async def dice(ctx, val: int = None):
    if val is None:
        await ctx.reply("😢 Please enter your guess number.")
        return

    if val not in (1, 2, 3, 4, 5, 6):
        await ctx.reply("♦️ Invalid number, please enter a number between 1 and 6 😊")
        return

    user_id = ctx.author.id
    if not coins.user_exists(user_id):
        await ctx.reply("😢 You don't have an account, create one with `e start`.")
        return
    coins.add_xp(user_id)
    rolled = random.randint(1, 6)
    won = rolled == val

    # ---- phase 1: rolling, nothing revealed yet ----
    rolling_embed = discord.Embed(
        title="🎲 Rolling the dice...",
        description=f"You guessed **{val}** — let's see...!",
        color=discord.Color.blue(),
    )
    rolling_embed.set_thumbnail(url=ROLLING_GIF)
    rolling_embed.set_footer(text="by emo bot")

    message = await ctx.reply(embed=rolling_embed)

    # suspense pause — asyncio.sleep instead of time.sleep so this doesn't
    # freeze the whole bot for everyone else while it waits
    await asyncio.sleep(3)

    # ---- phase 2: reveal the actual rolled face + outcome ----
    if won:
        cash = random.randint(100, 10000)
        result_embed = discord.Embed(
            title="✅ Correct guess!",
            description=f"Dice : **{rolled}** || You guessed : **{val}**\n🥳 You won **{cash}**🪙 coins",
            color=discord.Color.blue(),
        )
        rolling_embed.set_thumbnail(url=DICE_FACE_IMAGES[rolled])
    else:
        result_embed = discord.Embed(
            title="❌ Wrong guess!",
            description=f"Dice : **{rolled}** || You guessed : **{val}** 😔😥😢",
            color=discord.Color.blue(),
        )
        rolling_embed.set_thumbnail(url=DICE_FACE_IMAGES[rolled])  
    result_embed.set_footer(text="by emo bot")
    await message.edit(embed=result_embed)

    if won:
        # add to the existing balance instead of overwriting it —
        # the original replaced the user's whole coin total with just
        # the win amount
        data = coins.get_user(user_id)
        new_balance = data[1] + cash
        coins.update_coins(user_id, new_balance)


# _______________________________spin will__________________________________________


PRIZES = [
    "+10,000",
    "-5,000",
    "+20,000",
    "-10,000",
    "+45,000",
    "-20,000"
]

def wheel_display(position):

    above = PRIZES[(position - 1) % len(PRIZES)]
    current = PRIZES[position]
    below = PRIZES[(position + 1) % len(PRIZES)]

    return (
        f"🔼 {above}\n\n"
        f"🟦➡️ **{current}**\n\n"
        f"🔽 {below}"
    )

@bot.command(name="spin",aliases=["sw","swheel","spinwheel"])
async def spin(ctx):
    name = ctx.author.id
    if not coins.user_exists(name):
        await ctx.reply("😢you don't had an account create it use `e start`")
        return
    
    coins.add_xp(name)
    button = discord.ui.Button(
        label="Start",
        style=discord.ButtonStyle.green,
        emoji="▶️"
    )

    view = discord.ui.View()
    view.add_item(button)

    embed = discord.Embed(
        title="🎡 Spin Wheel",
        description="Press the Start button!",
        color=discord.Color.gold()
    )

    message = await ctx.send(
        embed=embed,
        view=view
    )

    async def start_callback(
        interaction: discord.Interaction
    ):

        if interaction.user.id != ctx.author.id:

            await interaction.response.send_message(
                "❌ This is not your wheel!",
                ephemeral=True
            )
            return

        button.disabled = True

        await interaction.response.edit_message(
            view=view
        )

        position = 0

        for i in range(20):

            position = (
                position + 1
            ) % len(PRIZES)

            embed.title = "🎡 SPINNING..."
            embed.description = wheel_display(
                position
            )

            await message.edit(
                embed=embed
            )

            await asyncio.sleep(
                0.1 + i * 0.02
            )

        result = PRIZES[position]

        if result.startswith("+"):

            embed.title = "🎉 YOU WON!"
            embed.color = discord.Color.green()
            val = coins.get_user(name)
            amount = int(result.replace(",", ""))
            new = val[1] + amount
            coins.update_coins(name,new)

        else:

            embed.title = "🥺 YOU LOST!"
            embed.color = discord.Color.red()
            val = coins.get_user(name)
            amount = int(result.replace(",", ""))
            new = val[1] - amount
            coins.update_coins(name,new)
        embed.description = (
            f"🎡 Result:\n\n"
            f"➡️ **{result}**"
        )

        await message.edit(
            embed=embed,
            view=None
        )

    button.callback = start_callback

# _______________SLOT__________________

SLOT_SYMBOLS = ["♥️", "💎", "🍪"]

def _slot_frame(s1: str, s2: str, s3: str) -> str:
    return (
        f"🟪🟪🟪🟪🟪\n"
        f"🟪⏹️__slot__⏹️🟪\n"
        f"🟪{s1}|{s2}|{s3}🟪\n"
        f"🟪🟪🟪🟪🟪"
    )

@bot.command(name="slot", aliases=["s", "playslot"])
async def slot(ctx):

    user_id = ctx.author.id

    if not coins.user_exists(user_id):
        await ctx.reply(
            "😢 You don't have an account, create one with `e start`."
        )
        return
    coins.add_xp(user_id)
    button = discord.ui.Button(
        label="Start",
        style=discord.ButtonStyle.green,
        emoji="▶️"
    )

    view = discord.ui.View()
    view.add_item(button)

    embed = discord.Embed(
        title="🎰 Slot Machine",
        description="Press **Start** to spin!",
        color=discord.Color.gold()
    )

    message = await ctx.reply(
        embed=embed,
        view=view
    )

    async def start_callback(interaction: discord.Interaction):

        if interaction.user.id != ctx.author.id:
            await interaction.response.send_message(
                "❌ This isn't your slot machine!",
                ephemeral=True
            )
            return

        button.disabled = True

        await interaction.response.edit_message(
            view=view
        )
        cash = random.randint(500,45000)
        # decide the real outcome up front
        final = [
            random.choice(SLOT_SYMBOLS)
            for _ in range(3)
        ]



        won = (
            final[0] ==
            final[1] ==
            final[2]
        )

        embed.title = "🎰 Spinning the slots..."
        embed.description = _slot_frame(
            "❔",
            "❔",
            "❔"
        )

        await message.edit(
            embed=embed
        )

        total_ticks = 15

        reel1_locks_at = 5
        reel2_locks_at = 10
        reel3_locks_at = 15

        for i in range(
            1,
            total_ticks + 1
        ):

            reel1 = (
                final[0]
                if i >= reel1_locks_at
                else random.choice(
                    SLOT_SYMBOLS
                )
            )

            reel2 = (
                final[1]
                if i >= reel2_locks_at
                else random.choice(
                    SLOT_SYMBOLS
                )
            )

            reel3 = (
                final[2]
                if i >= reel3_locks_at
                else random.choice(
                    SLOT_SYMBOLS
                )
            )

            embed.description = _slot_frame(
                reel1,
                reel2,
                reel3
            )

            await message.edit(
                embed=embed
            )

            await asyncio.sleep(
                0.08 + i * 0.02
            )

        data = coins.get_user(
            user_id
        )

        if won:

            new_balance = (
                data[1] + cash
            )

            coins.update_coins(
                user_id,
                new_balance
            )

            embed.title = (
                "🎉 Jackpot!"
            )

            embed.description = (
                _slot_frame(*final)
                + f"\n\n🎉 {ctx.author.display_name} won **{cash}** 🥳"
            )

            embed.color = (
                discord.Color.green()
            )

        else:

            new_balance = max(
                0,
                data[1] - cash
            )

            coins.update_coins(
                user_id,
                new_balance
            )

            embed.title = (
                "🥺 No match"
            )

            embed.description = (
                _slot_frame(*final)
                + f"\n\n🥺 {ctx.author.display_name} lost **{cash}**"
            )

            embed.color = (
                discord.Color.red()
            )

        await message.edit(
            embed=embed,
            view=None
        )

    button.callback = start_callback


import random
from datetime import datetime, timedelta

import discord
from discord.ext import commands, tasks



TRUTH_PROMPTS = [
    "What's the most embarrassing thing you've done in the last month?",
    "What's a lie you told that you never got caught for?",
    "Who in this server would you trust with a secret?",
    "What's your most irrational fear?",
    "What's the weirdest thing you've Googled?",
    "What's a habit you have that you're a little embarrassed by?",
    "What's the last thing you lied about?",
    "What's your most used emoji and why?",
    "What's a rumor about you that's actually true?",
    "What's the pettiest thing you've ever been mad about?",
    "What's a food combo you love that people judge you for?",
    "Who's the last person you stalked on social media?",
    "What's the most childish thing you still do?",
    "What's a secret talent nobody knows about?",
    "What's your most unpopular opinion?",
]

DARE_PROMPTS = [
    "Type your next 3 messages using only emojis.",
    "Send the 5th photo in your camera roll (or describe it if it's private).",
    "Talk in third person for the next 5 minutes.",
    "Do your best impression of another member in this server.",
    "Let the group pick your Discord status for the next hour.",
    "Send a voice message singing any song for 10 seconds.",
    "Change your nickname to whatever the group decides for 10 minutes.",
    "Text your most-recent contact something completely random.",
    "Speak only in questions for your next 3 messages.",
    "Describe your day using only movie titles.",
    "Send a screenshot of your most-used app's screen time.",
    "Do 10 pushups right now and confirm when you're done.",
    "Let someone else pick your next profile picture for a day.",
    "Compliment the last 3 people who spoke in this channel.",
    "Reply to every message for the next 5 minutes with 'no cap'.",
]

TD_IDLE_TIMEOUT_MINUTES = 15  # auto-end a session after this long with no td activity
_td_last_activity: dict[int, tuple[datetime, int]] = {}  # guild_id -> (last_active_at, channel_id)


def _in_guild_check(ctx) -> bool:
    return ctx.guild is not None


def _get_players(guild_id: int):
    """Players ordered by position ascending. Position starts at 1 (the
    session creator) — whoever currently holds the LOWEST position is
    treated as host, since there's no separate host column."""
    return coins.get_td_players(guild_id)


def _get_host_id(guild_id: int):
    players = _get_players(guild_id)
    return players[0]["user_id"] if players else None


def _current_player_row(guild_id: int):
    """Returns the row for whoever's turn it currently is, or None if the
    session isn't started. Self-heals if current_turn points at a position
    that no longer has a player at it (e.g. they left without a clean
    handoff) by snapping to whoever's first in line instead of getting
    permanently stuck."""
    position = coins.get_current_turn(guild_id)
    if not position:  # 0 = lobby, not started
        return None

    row = coins.get_player_by_position(guild_id, position)
    if row is not None:
        return row

    players = _get_players(guild_id)
    if not players:
        return None
    coins.update_current_turn(guild_id, players[0]["position"])
    return players[0]


def _end_session_state(guild_id: int):
    """Shared teardown used by both `tdend` and the idle-timeout task, so
    there's one place that defines what 'ending a session' means."""
    for row in _get_players(guild_id):
        coins.remove_td_player(guild_id, row["user_id"])
    coins.update_current_turn(guild_id, 0)
    _td_last_activity.pop(guild_id, None)


def _touch_td_activity(ctx):
    """Called from any td command that counts as 'someone is still
    playing', so the idle-timeout task knows not to end the session."""
    if ctx.guild is not None:
        _td_last_activity[ctx.guild.id] = (datetime.now(), ctx.channel.id)


def _display_player(ctx, user_id: int) -> str:
    """Shows '(left server)' instead of a broken mention for a player who
    is no longer a member of this guild."""
    member = ctx.guild.get_member(user_id) if ctx.guild else None
    if member is None:
        return f"<@{user_id}> *(left server)*"
    return f"<@{user_id}>"


PING_MENTIONS = discord.AllowedMentions(users=True)  # insurance against a global mentions-off setting


@bot.command(
    name="tdhelp",
    aliases=["tdguide", "howtotd", "tdrules"]
)
async def tdhelp(ctx):

    embed = discord.Embed(
        title="🎭 Truth or Dare — How to Play",
        color=discord.Color.purple()
    )

    embed.add_field(
        name="1️⃣ Starting a Session",
        value=(
            "Use `e tdcreate` to create a new game.\n"
            "The creator becomes the 👑 Host and first player.\n"
            "Only one TD session can exist per server."
        ),
        inline=False
    )

    embed.add_field(
        name="2️⃣ Joining the Game",
        value=(
            "`e tdjoin` — Join the session.\n"
            "`e tdleave` — Leave the session.\n"
            "Players may join until the game starts."
        ),
        inline=False
    )

    embed.add_field(
        name="3️⃣ Viewing Players",
        value=(
            "`e tdplayers`\n"
            "Shows all players in turn order.\n"
            "👑 marks the current Host."
        ),
        inline=False
    )

    embed.add_field(
        name="4️⃣ Starting the Round",
        value=(
            "The Host uses `e tdstart`.\n"
            "Requires at least 2 players.\n"
            "The player list becomes locked."
        ),
        inline=False
    )

    embed.add_field(
        name="5️⃣ Your Turn",
        value=(
            "`e truth` → Receive a random truth question.\n"
            "`e dare` → Receive a random dare.\n"
            "Only the current player may use these commands."
        ),
        inline=False
    )

    embed.add_field(
        name="6️⃣ Passing the Turn",
        value=(
            "`e tdnext`\n"
            "Moves to the next player.\n"
            "The order loops forever until the game ends."
        ),
        inline=False
    )

    embed.add_field(
        name="7️⃣ Ending the Game",
        value=(
            "`e tdend`\n"
            "Only the Host may end the session.\n"
            "All TD data is cleared."
        ),
        inline=False
    )

    embed.add_field(
        name="📜 Extra Rules",
        value=(
            "• If the Host leaves, the next player becomes Host.\n"
            "• Sessions automatically end after 15 minutes of inactivity.\n"
            "• Truth and Dare commands have cooldowns.\n"
            "• If everyone leaves, the session ends automatically."
        ),
        inline=False
    )

    embed.add_field(
        name="⚡ Commands",
        value=(
            "`tdcreate` (`createtd`)\n"
            "`tdjoin` (`playtd`)\n"
            "`tdleave` (`leavetd`)\n"
            "`tdplayers` (`showtd`, `listtd`)\n"
            "`tdstart` (`starttd`)\n"
            "`truth` (`t`, `suggesttruth`)\n"
            "`dare` (`d`, `suggestdare`)\n"
            "`tdnext` (`next`, `nextturn`)\n"
            "`tdend` (`endtd`, `endgame`, `stoptd`)"
        ),
        inline=False
    )

    embed.set_footer(
        text="🎭 Have fun and play responsibly!"
    )

    await ctx.reply(embed=embed)
@tasks.loop(minutes=5)
async def td_idle_check():
    now = datetime.now()
    stale = [
        guild_id for guild_id, (last_active, _channel_id) in list(_td_last_activity.items())
        if coins.td_player_count(guild_id) > 0
        and (now - last_active) > timedelta(minutes=TD_IDLE_TIMEOUT_MINUTES)
    ]
    for guild_id in stale:
        _, channel_id = _td_last_activity.get(guild_id, (None, None))
        _end_session_state(guild_id)
        channel = bot.get_channel(channel_id) if channel_id else None
        if channel:
            await channel.send("⌛ This Truth or Dare session timed out from inactivity and has ended.")


# ========================================================================
# TD_CREATE
# ========================================================================

@bot.command(name="tdcreate", aliases=["createtd"])
async def td_create(ctx):
    if not _in_guild_check(ctx):
        await ctx.reply("😅 This only works in a server, not DMs.")
        return

    guild_id = ctx.guild.id

    if coins.td_player_count(guild_id) > 0:
        await ctx.reply(
            "😅 A Truth or Dare session is already active here. Use `e tdend` to end it first."
        )
        return

    coins.create_td_server(guild_id)
    coins.update_current_turn(guild_id, 0)  # 0 = lobby, not started yet
    coins.add_td_player(guild_id, ctx.author.id, 1)  # creator = position 1 = host
    _touch_td_activity(ctx)

    await ctx.reply(
        f"🎉 {ctx.author.display_name} started a Truth or Dare session!\n"
        "Others can join with `e tdjoin`. Start with `e tdstart` when ready."
    )


# ========================================================================
# TD_JOIN
# ========================================================================

@bot.command(name="tdjoin", aliases=["playtd"])
async def td_join(ctx):
    if not _in_guild_check(ctx):
        return
    guild_id = ctx.guild.id

    if coins.td_player_count(guild_id) == 0:
        await ctx.reply("😅 No active session — start one with `e tdcreate`.")
        return

    if coins.get_current_turn(guild_id) != 0:
        await ctx.reply("😅 This session already started — you can't join mid-game.")
        return

    if coins.td_player_exists(guild_id, ctx.author.id):
        await ctx.reply("😏 You're already in this game.")
        return

    players = _get_players(guild_id)
    next_position = max((row["position"] for row in players), default=0) + 1
    coins.add_td_player(guild_id, ctx.author.id, next_position)
    _touch_td_activity(ctx)

    await ctx.reply(f"✅ {ctx.author.display_name} joined the game!")


# ========================================================================
# TD_LEAVE
# ========================================================================

@bot.command(name="tdleave", aliases=["leavetd"])
async def td_leave(ctx):
    if not _in_guild_check(ctx):
        return
    guild_id = ctx.guild.id
    user_id = ctx.author.id

    if not coins.td_player_exists(guild_id, user_id):
        await ctx.reply("😅 You're not in this game.")
        return

    started = coins.get_current_turn(guild_id) != 0
    was_host = _get_host_id(guild_id) == user_id
    current = _current_player_row(guild_id)
    was_current_player = started and current is not None and current["user_id"] == user_id

    coins.remove_td_player(guild_id, user_id)
    remaining = _get_players(guild_id)

    if not remaining:
        _end_session_state(guild_id)
        await ctx.reply(f"👋 {ctx.author.display_name} left. No players remain — session ended.")
        return

    _touch_td_activity(ctx)
    new_host_note = ""
    if was_host:
        new_host_note = f" 👑 <@{remaining[0]['user_id']}> is now the host."

    if started and was_current_player:
        coins.update_current_turn(guild_id, remaining[0]["position"])
        await ctx.reply(
            f"👋 {ctx.author.display_name} left. It's now <@{remaining[0]['user_id']}>'s turn.{new_host_note}",
            allowed_mentions=PING_MENTIONS,
        )
        return

    await ctx.reply(
        f"👋 {ctx.author.display_name} left the game.{new_host_note}",
        allowed_mentions=PING_MENTIONS,
    )


# ========================================================================
# TD_PLAYERS
# ========================================================================

@bot.command(name="tdplayers", aliases=["showtd", "listtd"])
async def td_players_cmd(ctx):
    if not _in_guild_check(ctx):
        return
    guild_id = ctx.guild.id
    players = _get_players(guild_id)

    if not players:
        await ctx.reply("😅 No one has joined yet. Use `e tdcreate` or `e tdjoin`.")
        return

    host_id = players[0]["user_id"]
    lines = []
    for row in players:
        tag = " 👑 (host)" if row["user_id"] == host_id else ""
        lines.append(f"{row['position']}. {_display_player(ctx, row['user_id'])}{tag}")

    embed = discord.Embed(
        title="🎭 Truth or Dare — Players",
        description="\n".join(lines),
        color=discord.Color.purple(),
    )
    await ctx.reply(embed=embed)


# ========================================================================
# TD_START
# ========================================================================

@bot.command(name="tdstart", aliases=["starttd"])
async def td_start(ctx):
    if not _in_guild_check(ctx):
        return
    guild_id = ctx.guild.id
    players = _get_players(guild_id)

    if not players:
        await ctx.reply("😅 No active session — start one with `e tdcreate`.")
        return

    host_id = players[0]["user_id"]
    if ctx.author.id != host_id:
        await ctx.reply("😏 Only the host can start the game.")
        return

    if len(players) < 2:
        await ctx.reply("😅 You need at least 2 players to start.")
        return

    if coins.get_current_turn(guild_id) != 0:
        await ctx.reply("😅 The game already started.")
        return

    coins.update_current_turn(guild_id, players[0]["position"])
    _touch_td_activity(ctx)

    await ctx.reply(
        f"🎬 The game has started! It's <@{players[0]['user_id']}>'s turn — use `e truth` or `e dare`.",
        allowed_mentions=PING_MENTIONS,
    )


# ========================================================================
# TRUTH / DARE
# ========================================================================

async def _handle_prompt(ctx, prompts: list, kind: str):
    if not _in_guild_check(ctx):
        return
    if not prompts:
        await ctx.reply("😅 No prompts are configured for this yet.")
        return

    guild_id = ctx.guild.id
    current = _current_player_row(guild_id)

    if current is None:
        await ctx.reply("😅 No game in progress — `e tdcreate` then `e tdstart` first.")
        return

    if ctx.author.id != current["user_id"]:
        await ctx.reply(f"😏 It's not your turn — waiting on <@{current['user_id']}>.")
        return

    _touch_td_activity(ctx)
    prompt = random.choice(prompts)
    embed = discord.Embed(
        title=f"{'🤔 Truth' if kind == 'truth' else '🔥 Dare'} for {ctx.author.display_name}",
        description=prompt,
        color=discord.Color.blue() if kind == "truth" else discord.Color.red(),
    )
    embed.set_footer(text="When you're done, use `e tdnext` to pass the turn.")
    await ctx.reply(embed=embed)


@bot.command(name="truth", aliases=["t", "suggesttrust"])
@commands.cooldown(1, 10, commands.BucketType.user)
async def truth(ctx):
    await _handle_prompt(ctx, TRUTH_PROMPTS, "truth")


@bot.command(name="dare", aliases=["d", "suggestdare"])
@commands.cooldown(1, 10, commands.BucketType.user)
async def dare(ctx):
    await _handle_prompt(ctx, DARE_PROMPTS, "dare")


# ========================================================================
# TD_NEXT
# ========================================================================

@bot.command(name="tdnext", aliases=["next", "nextturn"])
async def td_next(ctx):
    if not _in_guild_check(ctx):
        return
    guild_id = ctx.guild.id
    players = _get_players(guild_id)

    if not players:
        await ctx.reply("😅 No active session.")
        return

    host_id = players[0]["user_id"]
    current = _current_player_row(guild_id)

    if current is None:
        await ctx.reply("😅 The game hasn't started yet — use `e tdstart`.")
        return

    if ctx.author.id not in (host_id, current["user_id"]):
        await ctx.reply("😏 Only the host or the current player can advance the turn.")
        return

    positions = [row["position"] for row in players]
    idx = positions.index(current["position"])
    next_idx = (idx + 1) % len(positions)
    next_row = players[next_idx]

    coins.update_current_turn(guild_id, next_row["position"])
    _touch_td_activity(ctx)

    await ctx.reply(
        f"➡️ It's now <@{next_row['user_id']}>'s turn — use `e truth` or `e dare`.",
        allowed_mentions=PING_MENTIONS,
    )


# ========================================================================
# TD_END
# ========================================================================

@bot.command(name="tdend", aliases=["endtd", "endgame", "stoptd"])
async def td_end(ctx):
    if not _in_guild_check(ctx):
        return
    guild_id = ctx.guild.id
    players = _get_players(guild_id)

    if not players:
        await ctx.reply("😅 No active session to end.")
        return

    host_id = players[0]["user_id"]
    if ctx.author.id != host_id:
        await ctx.reply("😏 Only the host can end the game.")
        return

    _end_session_state(guild_id)
    await ctx.reply("🛑 The Truth or Dare session has ended. Thanks for playing 😁!")




@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.reply(f"⏳ Slow down — try again in {error.retry_after:.1f}s.")
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("😅 You're missing something for that command.")
        return
    if isinstance(error, commands.CommandNotFound):
        return  # nothing to do, not a real error
    print(f"[on_command_error] {ctx.command}: {error!r}")
    await ctx.reply("😵 Something went wrong running that command.")


GREETING_REPLIES = [
    "😁hey i am emo", "🤗hello how are you", "(●'◡'●)hiiiiiii", "😁nice to meet you",
    "☺️yoyo", "(❁´◡`❁)", "🥰love you", "😻you are my love", "♥️ hey good user",
    "^_~", "^_____^", "^0^ 😁", "( *︾▽︾)😁",
]

_greeting_cooldowns: dict[int, datetime] = {}


def _greeting_on_cooldown(user_id: int, seconds: int = 15) -> bool:
    now = datetime.now()
    last = _greeting_cooldowns.get(user_id)
    if last and (now - last).total_seconds() < seconds:
        return True
    _greeting_cooldowns[user_id] = now
    return False


@bot.event
async def on_message(message):
    if message.author.bot:
        return  

    text = message.content.lower()

    if text in ("hello", "hey"):
        if not _greeting_on_cooldown(message.author.id):
            await message.reply(random.choice(GREETING_REPLIES))

    if text == "good night":
        list = ["https://i.pinimg.com/1200x/79/6c/36/796c36dee1c2247f5a2a811dad17f29c.jpg","https://i.pinimg.com/736x/04/7e/5d/047e5d974f488563c821ce700e316511.jpg","https://i.pinimg.com/736x/4c/2c/c7/4c2cc7e8b48f489db11f6870cba130c2.jpg","https://i.pinimg.com/736x/47/be/70/47be7044b3326d095f67b16e0d1aa8b9.jpg"]
        val = random.choice(list)
        await message.reply(val)

    if text == "good morning":
        list = ["https://i.pinimg.com/1200x/bf/9b/03/bf9b0341cea14f16a2d78ff19ad740cb.jpg","https://i.pinimg.com/736x/b5/3c/73/b53c73efcff8bf1cc7e210193881fa4f.jpg","https://i.pinimg.com/736x/e7/8c/6b/e78c6bf2a09632707cc415c37d2917ba.jpg","https://i.pinimg.com/1200x/37/7a/5c/377a5c0b316eadd0bf2f577c15a2b693.jpg"]
        val = random.choice(list)
        await message.reply(val)

    if text == "emo":
        await message.add_reaction("🌸")
        await message.reply("you call me . 😘 me emo me here my pokkie >.<")

    if text == "owo":
        await message.reply("😤 owo is boring try emo bot 🥰 ")
    elif text == "owo is good than you" or text == "no" or text == "i hate you emo":
        await message.reply("🤨whatever you with your choice hope one day you like me 🥺")

    if text == "bye" :  
        await message.add_reaction("👋")

    if text == "dead chat":
        await message.add_reaction("⚰️")
        await message.reply("so do some fun with me my pookie 🌹😘")

    if text in ("thanks", "thx", "thank you", "thank u"):
        await message.add_reaction("🌹")

    if text in ("sorry", "srry"):
        await message.add_reaction("🥺")

    if text == "e":
        await message.add_reaction("🤨")
        await message.reply("use full command `e something`")

    if text == "neobot":
        await message.add_reaction("♥️")
        await message.reply("🥰he is my lovely bro do you miss or like him ?")


    if "hello" in text or "hey" in text :
        await message.add_reaction("👋")
    if "love" in text or "i love you" in text:
        await message.add_reaction("❤️")
    if "happy" in text or "yay" in text:
        await message.add_reaction("😁")
    if "sad" in text or "cry" in text:
        await message.add_reaction("🥺")
    if "lol" in text or "lmao" in text or "haha" in text:
        await message.add_reaction("😂")
    if "wow" in text or "omg" in text:
        await message.add_reaction("😲")
    if "cute" in text or "adorable" in text:
        await message.add_reaction("🥰")
    if "thanks" in text or "thank you" in text:
        await message.add_reaction("💖")
    if "sorry" in text:
        await message.add_reaction("🫂")
    if "good morning" in text or "morning" in text:
        await message.add_reaction("🌅")
    if "good night" in text or "gn" in text:
        await message.add_reaction("🌙")
    if "bruh" in text:
        await message.add_reaction("💀")
    if "congrats" in text or "congratulations" in text:
        await message.add_reaction("🎉")
    if "good luck" in text:
        await message.add_reaction("🍀")
    if "bored" in text:
        await message.add_reaction("🥱")

    await bot.process_commands(message)



# work gif
@bot.command()
async def working(ctx):
    name = ctx.author.display_name
    embed = discord.Embed(
        title = f"{name} is working",color=discord.Color.blue()
    )
    list = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbXRzNHRseTJnbHN4MHhkaHdnZTI0enNhbnNtdHF2OTJybWlwNmViciZlcD12MV9naWZzX3NlYXJjaCZjdD1n/JIX9t2j0ZTN9S/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbXRzNHRseTJnbHN4MHhkaHdnZTI0enNhbnNtdHF2OTJybWlwNmViciZlcD12MV9naWZzX3NlYXJjaCZjdD1n/XIqCQx02E1U9W/giphy.gif","https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3OWFzNmZlb3ZrdzJpbWg3aXZsZmdrYzEya21rejI1ajlwZHN1ZHR1dyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/AE2wKBTDYI54w9afj1/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExamhwZGphajJveG4waTZ6d2EzaDE3ZWMxZmo1a2pwcXRmYTJ1MGI0NyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/kudIERso2pFiE/giphy.gif"]
    embed.set_image(url=random.choice(list))
    await ctx.send(embed=embed)


# 1. hug 🤗
@bot.command()
async def hug(ctx,member:discord.Member=None):
    await ctx.send(member.mention)
    name = ctx.author.display_name
    embed = discord.Embed(
        title = f"{name} gives hug to {member.display_name}",color=discord.Color.blue()
    )
    list = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZTJ2bzh0em8yb2U3NDd1MWxvajZkajVrMHM5ejU1a2M5d2hqZmtjZSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/IzXiddo2twMmdmU8Lv/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZTJ2bzh0em8yb2U3NDd1MWxvajZkajVrMHM5ejU1a2M5d2hqZmtjZSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/2GDHOfqcmYIX6/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExb2dpcTV0ODlmNXZzYWFoN3p2dHY4eXk5bGNnMG40bGRjaWJtejB6NCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/u9BxQbM5bxvwY/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExb2dpcTV0ODlmNXZzYWFoN3p2dHY4eXk5bGNnMG40bGRjaWJtejB6NCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/WynnqxhdFEPYY/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbnkwaDlyZHZkM2MyMDhiNmN4djVxOHkzczA1bmJjbTQ4M2oyZzZ3YiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/axdG5dnKJ9MtO/giphy.gif"]
    embed.set_image(url=random.choice(list))
    await ctx.send(embed=embed)

# 2. pat 🖐️
@bot.command()
async def pat(ctx,member:discord.Member):
    await ctx.send(member.mention)
    name = ctx.author.display_name
    embed = discord.Embed(
        title = f"{name} gives pets to {member.display_name}",color=discord.Color.blue()
    )
    list = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeWhtYTZwZzh4d242NWk4OGFnNGJmZ3M5MnQ3Y28wZzUyMGJkdGZ3dyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/xcIlI0798VgnPYUQwj/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaDdpcDc5NWowZmcyNHVsN2dnMnBkbnZsMGhmZzFtMzAwcWV2dmR4aSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/5tmRHwTlHAA9WkVxTU/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeDkzbG0zY29nZ3FscW1hZHc3YmNtZmt0a2MzNjN3aW01M2U3ZGV2NiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/DuqbTwSKChlG7sgFcZ/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeDkzbG0zY29nZ3FscW1hZHc3YmNtZmt0a2MzNjN3aW01M2U3ZGV2NiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/nQnMaGbVRahwyG09T5/giphy.gif"]
    embed.set_image(url=random.choice(list))
    await ctx.send(embed=embed)
# 3. kiss 💋
@bot.command()
async def kiss(ctx,member:discord.Member):
    await ctx.send(member.mention)
    name = ctx.author.display_name
    embed = discord.Embed(
        title = f"{name}  kiss to {member.display_name}",color=discord.Color.blue()
    )
    list = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNWMyNjJ1dzVtemZmNzR3endjejUwYWFjZjc2c2s0bzJoM3VzOG9zMyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/MQVpBqASxSlFu/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNWMyNjJ1dzVtemZmNzR3endjejUwYWFjZjc2c2s0bzJoM3VzOG9zMyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/EVODaJHSXZGta/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMGJ0eG9wa3dsbnJudjllc2pjbTZ6NnZzM2dhM2Z2N3dzcWM4ajdmaiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/hJioaFkX7sjSe7Tkd1/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYXh1MW9tMWU1MGQwc2wxdmNqMTZmaW02c3o5MWo5ZHFtZGphMDJ1MiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/W1hd3uXRIbddu/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZzZkanUyd2hkNWMyZWRzYjc0bmxicHJ0dGtuYzdsNGY1bml3MnYwcyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/WdNwaxagEghAYuFDnY/giphy.gif"]
    embed.set_image(url=random.choice(list))
    await ctx.send(embed=embed)
# side eyes
@bot.command()
async def see(ctx,member:discord.Member):
    await ctx.send(member.mention)
    name = ctx.author.display_name
    embed = discord.Embed(
        title = f"{name}  seeing  {member.display_name}",color=discord.Color.blue()
    )
    list = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaTI2Z2J1NG1jc3Z4NTc2bGNtZmppNjByaW1ldzA5bmtxc2xrdjF3MiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/hECJDGJs4hQjjWLqRV/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaTI2Z2J1NG1jc3Z4NTc2bGNtZmppNjByaW1ldzA5bmtxc2xrdjF3MiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/GAXXHdS0zXawVLOJLY/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExc3ZkdzNweGppa3EzM3hqejB2aTd6cXdkeHNweHdoMXVzZmRpeDdvMiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Y52RYuKL2j85OGJATq/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbGNhZXp4MHljYnNvMzhyZXVld2YyYTJqemljbjlkZDAwOTJncDNubSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/WRuBiZKB6xgsS9DrFA/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbGNhZXp4MHljYnNvMzhyZXVld2YyYTJqemljbjlkZDAwOTJncDNubSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Wwn5NKv4At2CIc8XQa/giphy.gif"]
    embed.set_image(url=random.choice(list))
    await ctx.send(embed=embed)
# 4. slap 👋
@bot.command()
async def slap(ctx,member:discord.Member):
    await ctx.send(member.mention)
    name = ctx.author.display_name
    embed = discord.Embed(
        title = f"{name}  slap to {member.display_name}",color=discord.Color.blue()
    )
    list = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZWt3bm1iaGtjM2FsbHV6NjZzMHVqOWhjOXc3MGM3b3ZxajNwdDl3cyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Gf3AUz3eBNbTW/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZWt3bm1iaGtjM2FsbHV6NjZzMHVqOWhjOXc3MGM3b3ZxajNwdDl3cyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/WBzRBKE0DHIB9OSvH5/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZWt3bm1iaGtjM2FsbHV6NjZzMHVqOWhjOXc3MGM3b3ZxajNwdDl3cyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/xUNd9HZq1itMkiK652/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNjdhazk3dDY2eDE0bmozNm0zNWljb3pjbDFhczB4bG8wc2c4MTVobyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/QZpDATBs8QzcLZo9uI/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNjdhazk3dDY2eDE0bmozNm0zNWljb3pjbDFhczB4bG8wc2c4MTVobyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/miFItAUiTEHlaBrzGV/giphy.gif"]
    embed.set_image(url=random.choice(list))
    await ctx.send(embed=embed)
# 5. poke 👉
@bot.command()
async def poke(ctx,member:discord.Member):
    name = ctx.author.display_name
    await ctx.send(member.mention)
    embed = discord.Embed(
        title = f"{name}  poke to {member.display_name}",color=discord.Color.blue()
    )
    list = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExanhvdzl0ajNzZTZjaTV6OGV5cGIwb21pd3Eybmk4MnMweWo2aDB6NCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/aZSMD7CpgU4Za/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExanhvdzl0ajNzZTZjaTV6OGV5cGIwb21pd3Eybmk4MnMweWo2aDB6NCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/6ITiRKIryP3MI/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExanhvdzl0ajNzZTZjaTV6OGV5cGIwb21pd3Eybmk4MnMweWo2aDB6NCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/FdinyvXRa8zekBkcdK/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZWM5M21za2VqOWFxd3ZwNnppYWN4cWVhMHc3c3lodmhuNXA4MGw3biZlcD12MV9naWZzX3NlYXJjaCZjdD1n/8PBC5GXof1G7iODApJ/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExanhvdzl0ajNzZTZjaTV6OGV5cGIwb21pd3Eybmk4MnMweWo2aDB6NCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/0H0xhd3taWF2RLGtIE/giphy.gif"]
    embed.set_image(url=random.choice(list))
    await ctx.send(embed=embed)
# 6. punch 👊
@bot.command()
async def punch(ctx,member:discord.Member):
    name = ctx.author.display_name
    await ctx.send(member.mention)
    embed = discord.Embed(
        title = f"{name}  punch to {member.display_name}",color=discord.Color.blue()
    )
    list = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZWlxN2Q5MzczY2t6dzNxN2YzbHcxamcyaGhybjFoNWtpM3hydWJqeCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/PJArDrZZp31oR4PuxT/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZWlxN2Q5MzczY2t6dzNxN2YzbHcxamcyaGhybjFoNWtpM3hydWJqeCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/S8nGEQ0yR8z6M/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZWlxN2Q5MzczY2t6dzNxN2YzbHcxamcyaGhybjFoNWtpM3hydWJqeCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/S8nGEQ0yR8z6M/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZHFpMmtuYnhxenV4cGh1NTdzb3dwZmcwemVuYmc3OWd0NTMwZmNkcyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/6iqK0cXu38mR0qxyx2/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZHFpMmtuYnhxenV4cGh1NTdzb3dwZmcwemVuYmc3OWd0NTMwZmNkcyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/zQR7qMJ3Esh0Y/giphy.gif"]
    embed.set_image(url=random.choice(list))
    await ctx.send(embed=embed)
# 7. cuddle 🥰
@bot.command()
async def cuddle(ctx,member:discord.Member):
    await ctx.send(member.mention)
    name = ctx.author.display_name
    embed = discord.Embed(
        title = f"{name}  cuddle to {member.display_name}",color=discord.Color.blue()
    )
    list = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHZ0cnFkaXpmZTN4MjBxNXc4MjMzczI1OTZvYXViMGVjbjUxbjB1NyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/BXrwTdoho6hkQ/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHZ0cnFkaXpmZTN4MjBxNXc4MjMzczI1OTZvYXViMGVjbjUxbjB1NyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/ythHeq4Qgx2De/giphy.gif","https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3NnlwZXBsMmJucTNzcHI0bXRvNmpnbWxma3NkYmRzM2dsdWZtMGt4MSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/eMpDBxxTzKety/giphy.gif","https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3NWEzMzU2dHh5ZjNrZnV0ZGdjdXV6YnF2Ynl2czQ5M3FqM216c21nZSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/ZWVRU8BCEq24lpgopT/giphy.gif","https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3NWEzMzU2dHh5ZjNrZnV0ZGdjdXV6YnF2Ynl2czQ5M3FqM216c21nZSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/3rgXBSoIApjSYTo8vK/giphy.gif"]
    embed.set_image(url=random.choice(list))
    await ctx.send(embed=embed)
# 8. tickle 😂
@bot.command()
async def tickle(ctx,member:discord.Member):
    name = ctx.author.display_name
    await ctx.send(member.mention)
    embed = discord.Embed(
        title = f"{name}  tickle to {member.display_name}",color=discord.Color.blue()
    )
    list = ["https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3bDRjM3BhZGlvamlxY3dhbm1vOGhkZ3hnb3lxbTFmejJrM3U4NXEyZCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/STqevF3TOL45WRP8hm/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExejl0N2xrcmVtOWU1Y2Y4bHluZ3d6ZXllajlkejE0amY0bHIybjN3ZyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/P3HD8ePiTcBgmXXi5V/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExejl0N2xrcmVtOWU1Y2Y4bHluZ3d6ZXllajlkejE0amY0bHIybjN3ZyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/38GzxKFzYsK2c/giphy.gif"]
    embed.set_image(url=random.choice(list))
    await ctx.send(embed=embed)
# 10. highfive ✋
@bot.command()
async def highfive(ctx,member:discord.Member):
    await ctx.send(member.mention)
    name = ctx.author.display_name
    embed = discord.Embed(
        title = f"{name}  highfive to {member.display_name}",color=discord.Color.blue()
    )
    list = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNWxuOXZqMm0xOXhlamwwOXVpbGJjNG04YWhtZzd2OG1sZ2JoZXhncyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/BFZvBtfvEbmp2ztBnv/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWlncGF4NDQ0aDB5cmV3ejQycnBsOTYwYmRjaHd3OGRwbDNrMmoyZCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/A3U0dj6a9TxQb4iNoe/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWlncGF4NDQ0aDB5cmV3ejQycnBsOTYwYmRjaHd3OGRwbDNrMmoyZCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/XZMh13cILjZfhWeEbr/giphy.gif","https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3M2VxN3BzcWFrZ3IzdGMzZGdxNXlhMzZ6cWZqNjFjZmxnMmx3OHhkcCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/719vFoSRcbAqQQUMjU/giphy.gif"]
    embed.set_image(url=random.choice(list))
    await ctx.send(embed=embed)


# sorry
@bot.command(name="sorry",aliases=["srry"])
async def sorry(ctx,member:discord.Member):
    await ctx.send(member.mention)
    name = ctx.author.display_name
    embed = discord.Embed(
        title = f"{name}  saying sorry to {member.display_name}",color=discord.Color.blue()
    )
    list = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM21kdXBwNHFsc3B5bzNweG44dXp4ZDh1a2pncmVqemkyc3lrb3IybCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/DNe4LKL6iwZ2goCSx6/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM21kdXBwNHFsc3B5bzNweG44dXp4ZDh1a2pncmVqemkyc3lrb3IybCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/l4EoMx1ooMtK6zNHa/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbGt5emZuNDlha3BsZmxjeTJiOGwxYTB0OGt4NzY3d2pyMWlpNWd0MCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/B2TG4Rx3gPuMw/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbGt5emZuNDlha3BsZmxjeTJiOGwxYTB0OGt4NzY3d2pyMWlpNWd0MCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/RM0FFEcOLBzEjtrbCK/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbGt5emZuNDlha3BsZmxjeTJiOGwxYTB0OGt4NzY3d2pyMWlpNWd0MCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/lBTpHmb03fo8U/giphy.gif"]
    embed.set_image(url=random.choice(list))
    await ctx.send(embed=embed)

# kill
@bot.command()
async def kill(ctx,member:discord.Member):
    await ctx.send(member.mention)
    name = ctx.author.display_name
    embed = discord.Embed(
        title = f"{name}  kills to {member.display_name}",color=discord.Color.blue()
    )
    list = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHNhc3R0bThlMTI5MmFhdGZyOGFjYXd4MjQxY3ZobGE3dzBqdDNzdiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/WxJea79lT6gE6aNYpC/giphy.gif","https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3cWNvNjdoMXI4Zm52NmdrdzFhY3h3ZDhybjR5bTR5cms5b205a3QxeCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/uTCAwWNtz7U2c/giphy.gif","https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3eXFqODEwcnJwaHQwMXU2NGtzNXE0OHJtdnIyNnJqYmEybWwxY2QwNSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/3F9duvK4t9hzW/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExa3hsNXdvaW0zbW4zenVtaXg4dmx4cDF0aDFucGhwN3pwcGg3OTlmbyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/WrygObkKCqXPIeixGB/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExa3hsNXdvaW0zbW4zenVtaXg4dmx4cDF0aDFucGhwN3pwcGg3OTlmbyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/wB42LcFqhYfmD9pvIC/giphy.gif"]
    embed.set_image(url=random.choice(list))
    await ctx.send(embed=embed)

# thx 
@bot.command(name="thanks",aliases=["thx","thank you"])
async def thx(ctx,member:discord.Member):
    await ctx.send(member.mention)
    name = ctx.author.display_name
    embed = discord.Embed(
        title = f"{name}  thank you  {member.display_name}",color=discord.Color.blue()
    )
    list = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExc3Z0dnJpNmQ3dHpqYzkwZHlrbDQyYzJhMW1ydm9mZGw5ZWowNXZtdCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/L9Q2rzzBHrfv4a1y4h/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExc3Z0dnJpNmQ3dHpqYzkwZHlrbDQyYzJhMW1ydm9mZGw5ZWowNXZtdCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/nnZZfXUevHdz27aH7u/giphy.gif","https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3YW00ZXBzdTVtNjBiaDFpNnBueHd3NTEwaXczZDN5c3ZuN2pkazRiYSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/po3NDGWuAE33qmWqe3/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOW15cGx0YjhueTB0dzR3bmxsbnk0eTJ3MTJzaXo4MzF6d2kzbmo4ciZlcD12MV9naWZzX3NlYXJjaCZjdD1n/3oz8xIsloV7zOmt81G/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOW15cGx0YjhueTB0dzR3bmxsbnk0eTJ3MTJzaXo4MzF6d2kzbmo4ciZlcD12MV9naWZzX3NlYXJjaCZjdD1n/ovHlQnHMZgVu9XRJfX/giphy.gif"]
    embed.set_image(url=random.choice(list))
    await ctx.send(embed=embed)

# 11. wave 👋
@bot.command()
async def wave(ctx,member:discord.Member):
    await ctx.send(member.mention)
    name = ctx.author.display_name
    embed = discord.Embed(
        title = f"{name}  waving to {member.display_name}",color=discord.Color.blue()
    )
    list = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYzRqdTljdnR3cWZobmxvNDJ0Y2ptM2R6ajQwcXQwcWw2MjZzc3Z3aCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/ZgTRcH0SbiLV1wolnR/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYzRqdTljdnR3cWZobmxvNDJ0Y2ptM2R6ajQwcXQwcWw2MjZzc3Z3aCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/yyVph7ANKftIs/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYzRqdTljdnR3cWZobmxvNDJ0Y2ptM2R6ajQwcXQwcWw2MjZzc3Z3aCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/9cZQnwdzUXTDG/giphy.gif","https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3OGpmd20wbzIwZG8wa2NpNmJwN2V4NnQ3cjBubjV4enZpZ3ltY3l1ZCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/BZlvPwfbvTkO2yCZkJ/giphy.gif","https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3OGpmd20wbzIwZG8wa2NpNmJwN2V4NnQ3cjBubjV4enZpZ3ltY3l1ZCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/6hKL8BI8rRNrMRFtAx/giphy.gif"]
    embed.set_image(url=random.choice(list))
    await ctx.send(embed=embed)


# 16. bite 😈
@bot.command()
async def bite(ctx,member:discord.Member):
    await ctx.send(member.mention)
    name = ctx.author.display_name
    embed = discord.Embed(
        title = f"{name}  bite's to {member.display_name}",color=discord.Color.blue()
    )
    list = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbnN6czhycW0wcmRocGkxMzhjZzlobjIzNDBvNTNjb3pjazV5NzY3eSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/OqQOwXiCyJAmA/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbnN6czhycW0wcmRocGkxMzhjZzlobjIzNDBvNTNjb3pjazV5NzY3eSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/lrMUMn9lnpaJDsvP0u/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbnN6czhycW0wcmRocGkxMzhjZzlobjIzNDBvNTNjb3pjazV5NzY3eSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/l0Iy0QdzD3AA6bgIg/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbnN6czhycW0wcmRocGkxMzhjZzlobjIzNDBvNTNjb3pjazV5NzY3eSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/b6mpA0JrIUsFSdhG9q/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaWxoNTEwbWpoYXR6d3IyYTNvN2NwZDA1Y3liNThzd3F4Y2w3bDYyYyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/CacB5USV4xLUbtcr2q/giphy.gif"]
    embed.set_image(url=random.choice(list))
    await ctx.send(embed=embed)
# 17. feed 🍰
@bot.command()
async def feed(ctx,member:discord.Member):
    await ctx.send(member.mention)
    name = ctx.author.display_name
    embed = discord.Embed(
        title = f"{name}  feed's to {member.display_name}",color=discord.Color.blue()
    )
    list = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHdoNjVsazJicHp5YW5weDB4cmpxbHhmdWoxNnEweTNiaHd6N3hpNSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/POl4x8sulgMF2ZrBrz/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHdoNjVsazJicHp5YW5weDB4cmpxbHhmdWoxNnEweTNiaHd6N3hpNSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/hvOIUUOg8jNKI8W1iv/giphy.gif","https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3M3E5OGFpOHJ3a2JwanE1cTRyZ3h4eDAzbGJlbjU0MzFpczJ5cGViOSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/nEc0jQfUPxa6Voi44S/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOGZjeDFxZWt3dXRoY2hwZTd5MzN6cHJmdGM3ZW54Zmc0b280bW5uNyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/4mAuYdos8Fr1Vo9x7c/giphy.gif","https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3azhnbzdzMHB6cHZncThzaGQzempwamx2aHptYndsdG5uNHkxeW90bCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/9RpSIFJqtGoLmd201s/giphy.gif"]
    embed.set_image(url=random.choice(list))
    await ctx.send(embed=embed)
# 18. holdhand 🤝
@bot.command()
async def holdhand(ctx,member:discord.Member):
    await ctx.send(member.mention)
    name = ctx.author.display_name
    embed = discord.Embed(
        title = f"{name}  holdhand to {member.display_name}",color=discord.Color.blue()
    )
    list = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNTZlcXVyb3gzOW9ycnVhbW42OXAxcjVka3RyeTBmeDVqZGhvNWMwbSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/YquUtQpCM3rGYNWfS5/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdmNteXJsa3hlOHgwdHAxcWhwamc3Z3ozZjJlOWl6bXZjN3U3bWdpcSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/jHcysJbxbIYRhd9bL7/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdmNteXJsa3hlOHgwdHAxcWhwamc3Z3ozZjJlOWl6bXZjN3U3bWdpcSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/aKsLiVDLLMsUYBANvT/giphy.gif","https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3OXFiZXA2YXVvc2loN2cyZXA3aTFvN25mcDkxcjc2a2FrdG9vc2JyOCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/HkccCz8G06uwnNQcRh/giphy.gif"]
    embed.set_image(url=random.choice(list))
    await ctx.send(embed=embed)

# ___________flykiss_________
@bot.command()
async def flykiss(ctx,member:discord.Member):
    await ctx.send(member.mention)
    name = ctx.author.display_name
    embed = discord.Embed(
        title = f"{name}  flying kiss to {member.display_name}",color=discord.Color.blue()
    )
    list = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmRoNHo3dW5pZmtoNThnZ2NrZHdnaHU3cHdrYTByaWtwbmlsZTk2biZlcD12MV9naWZzX3NlYXJjaCZjdD1n/ANjMpBvC9LeRUopsoU/giphy.gif","https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3ejE5NzE4dDEyNG0zMW9vcjYwcHJ0dTh5eXczczFpM3A5bTlwZTV1YSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/d47HFwAbGv3OmqfC/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM2F6enJoY3R3ZWVkZzgzaXlka2VtcGhrdHB5MTF4NWV6cnZ5MnNodCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/108M7gCS1JSoO4/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM2F6enJoY3R3ZWVkZzgzaXlka2VtcGhrdHB5MTF4NWV6cnZ5MnNodCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/xF77nzFm0dNK1MHnAc/giphy.gif","https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3bTJqNmhsbGhvbzBtZmJ3YjJwMjh2NGZncWMwaGQ5YWVudmJicjRzdCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Myoi71QKvCTb7C02gN/giphy.gif"]
    embed.set_image(url=random.choice(list))
    await ctx.send(embed=embed)

#  _________ flower ____________
@bot.command()
async def giveflower(ctx,member:discord.Member):
    await ctx.send(member.mention)
    name = ctx.author.display_name
    embed = discord.Embed(
        title = f"{name}  gives flower to {member.display_name}",color=discord.Color.blue()
    )
    list = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExN2cxaHUwbjVua3FleWpodndjYXRoZWUwZHNqcThkZWZvZWc2eW1pNiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/bwBYKgvEsKt4rsI1jJ/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExN2cxaHUwbjVua3FleWpodndjYXRoZWUwZHNqcThkZWZvZWc2eW1pNiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/PY3jUxrRsQVdx9CyFC/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExN2cxaHUwbjVua3FleWpodndjYXRoZWUwZHNqcThkZWZvZWc2eW1pNiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/XvtRXpbkN3e0ZOPB3X/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ3k3dXNhbW01bnM0NzBucWRrcHAxZXYxYXNiaWF5OXZhdWtiN3M2diZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Vf3tecIXrx9FQY50yl/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ3k3dXNhbW01bnM0NzBucWRrcHAxZXYxYXNiaWF5OXZhdWtiN3M2diZlcD12MV9naWZzX3NlYXJjaCZjdD1n/5SbA6ZRhiI5jriUwqu/giphy.gif"]
    embed.set_image(url=random.choice(list))
    await ctx.send(embed=embed)


# ________________ 19.u fool __________
@bot.command()
async def ufool(ctx,member:discord.Member):
    await ctx.send(member.mention)
    name = ctx.author.display_name
    embed = discord.Embed(
        title = f"{name}  saying you fool  to {member.display_name}",color=discord.Color.blue()
    )
    list = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWc0eG9kbTQyNTRscHF6bXIzY3pianJ6a2g0OXdrdDNhb21sanlqaiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/zMabidNwX7LlcqGszI/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExN3l2d29oeDJkb3A1c2ZmcDdobzVyeTZxZzVkNTVkdjI3ajR5dGN5YyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/dJE9Zd0O4prEI/giphy.gif","https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3MmkxZnp1ZDE1ZzgxM2kyZzc3ZzN5NW9nZW50ZmMzZGVzdGd6ZTJsaiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/dAJmcxTcMahP99TLOb/giphy.gif","https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3NmsybzlzMno5ZHF0a3FjMXR3cDZhNmRyMGRjMHd1dGJkNTRkbDdoaSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/OabElnUhUnPGQ9ye2h/giphy.gif"]
    embed.set_image(url=random.choice(list))
    await ctx.send(embed=embed)

# __________ 20.miss___________
@bot.command()
async def miss(ctx,member:discord.Member):
    await ctx.send(member.mention)
    name = ctx.author.display_name
    embed = discord.Embed(
        title = f"{name}  missing  you {member.display_name}",color=discord.Color.blue()
    )
    list = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExa3UzZ2lpNjRjc3VlMmp2ejFjcmV5YTM1NGZsMnRsM2tiOXV4YmRkdCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/jeqNF352Yqr2jNmLgN/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMDB6eHJmazFmOTV5bGRxMjh4YnhhZ29zNWFkOGFxM2Mwd2JlNjI3byZlcD12MV9naWZzX3NlYXJjaCZjdD1n/YLqBm9e31YM8b3aon8/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMDB6eHJmazFmOTV5bGRxMjh4YnhhZ29zNWFkOGFxM2Mwd2JlNjI3byZlcD12MV9naWZzX3NlYXJjaCZjdD1n/1DJhlWrKNnvwbW5Uyn/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMDB6eHJmazFmOTV5bGRxMjh4YnhhZ29zNWFkOGFxM2Mwd2JlNjI3byZlcD12MV9naWZzX3NlYXJjaCZjdD1n/RI8sVAn6lEyQZFpZfb/giphy.gif","https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3Nm5vM2prdGk2dnZnMWFhc200dXR0a3Nwd3BndXMydW9tOXNmMWZmYyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/NfOD0Bv11XnhK/giphy.gif"]
    embed.set_image(url=random.choice(list))
    await ctx.send(embed=embed)


# _____________user avatar command_______________
@bot.command()
async def avatar(ctx,member:discord.Member=None):
    val = member
    if val != None :
        name = val.display_name
        embed = discord.Embed(title=f"{name}'s avatar 🌸",color=discord.Color.blue())
        embed.set_image(url=val.avatar.url)
        await ctx.send(embed=embed)
    else:
        user = ctx.author.display_name
        embed = discord.Embed(title=f"{user}'s avatar 🌸",color=discord.Color.blue())
        embed.set_image(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)


@bot.command()
async def help(ctx):

    embed = discord.Embed(
        title="🌸 Emo Bot Help",
        description="Welcome to Emo Bot! Here are all available commands.",
        color=discord.Color.purple()
    )

    embed.add_field(
        name="💰 Economy",
        value="`start` `balance` `daily` `work` `pay` `leaderboard` `coinsflip` `dices` `slot` `spin` `profile`",
        inline=False
    )

    embed.add_field(
        name="🛒 Shop",
        value="`shopsticker` `shopwallpaper` `buysticker` `buywallpaper` `inventory` `mystickers` `equipstr` `equipwp`",
        inline=False
    )

    embed.add_field(
        name="🎭 Truth or Dare",
        value="`tdcreate` `tdjoin` `tdleave` `tdplayers` `tdstart` `tdnext` `tdend` `truth` `dare` `tdhelp`",
        inline=False
    )

    embed.add_field(
        name="💕 Interaction - mention command",
        value="`hug` `kiss` `see` `wave` `cuddle` `pat` `poke` `slap` `punch` `highfive` `holdhand` `tickle` `bite` `kill` `feed` `giveflower` `flykiss` `miss`",
        inline=False
    )

    embed.add_field(
        name="😊 Emotions",
        value="`happy` `sad` `cry` `angry` `bored` `sleepy` `smile` `laughing` `excited` `playful` `proud` `relieved` `blush` `bashful` `shy` `nervous` `embarrassed` `flustered` `awkward` `shocked` `surprised` `scared` `lovely` `grateful` `thanks` `sorry` `wow` `confident` `admiring`",
        inline=False
    )

    embed.add_field(
        name="🎉 Fun",
        value="`dance` `dead` `working` `flex` `ufool`",
        inline=False
    )

    embed.add_field(
        name="👋 Social",
        value="`hi` `hello` `avatar` `profile`",
        inline=False
    )

    embed.add_field(
        name="📚 Help",
        value="`help` `helpsticker` `helpwallpaper` `tdhelp`",
        inline=False
    )

    embed.add_field(
        name="🧪 other's",
        value="`dev` `emo` `debug` `feedback` `illusion` `choice` `tell` `rate` `compliment` `fact` `joke` `nickname` `luck` `cuteness` `something` ",
        inline=False
    )
    embed.set_footer(
        text="✨ Prefix: e • Emo Bot"
    )

    await ctx.reply(embed=embed)

@bot.command()
async def something(ctx):
    list = ["","https://i.pinimg.com/736x/a7/6c/9d/a76c9d1a085feeb9755fdfc9af0b47f3.jpg","https://i.pinimg.com/736x/0d/a4/4c/0da44c9bfb41a1a6765d197931ba0f60.jpg","https://i.pinimg.com/736x/36/56/31/3656317424b811c3997f1d39f70df1c0.jpg","https://i.pinimg.com/736x/a7/70/6c/a7706c6dcc8d4232aaec2097d08c7112.jpg","https://i.pinimg.com/736x/62/bf/06/62bf06317b81532aee178cd60d39a041.jpg","https://i.pinimg.com/736x/0a/6c/f8/0a6cf8bb558af3bf2351ed3de6dbe9d6.jpg","https://i.pinimg.com/736x/8f/33/00/8f330010ec2ff0ff5b73e3b64d4fc73f.jpg","https://i.pinimg.com/736x/be/52/d5/be52d53cff32462c42ae7c2a24f45c5f.jpg","https://i.pinimg.com/736x/3a/9c/33/3a9c33305ee689435c1635300f3dbc19.jpg","https://i.pinimg.com/736x/ab/17/f5/ab17f5821205a9fa08b41663b6669d01.jpg","https://i.pinimg.com/736x/5c/06/e6/5c06e6932fac73770aadfd3db0216fc5.jpg","https://i.pinimg.com/1200x/a9/1b/a4/a91ba418ad25c01b35413b8d9952a738.jpg"]
    await ctx.reply(random.choice(list))

@bot.command()
async def cuteness(ctx,member:discord.Member=None):
    if member != None :
        num = random.randint(30,100)
        text = ""
        if num <= 50 :
            text = "cute 😳"
        elif num >= 75 :
            text = "so cute 😍"
        elif num >= 90 :
            text = "cutest 😍🌹🥰😘"
        await ctx.send(f"- 🙂 - this is computer's choice don't feel bad if result are bad\n📊 {member.display_name} is {num}% {text} 🌸")
    else :
        num = random.randint(30,100)
        text = ""
        if num <= 50 :
            text = "cute 😳"
        elif num >= 75 :
            text = "so cute 😍"
        elif num >= 90 :
            text = "cutest 😍🌹🥰😘"
        await ctx.send(f"- 🙂 - this is computer's choice don't feel bad if result are bad\n📊 {ctx.author.display_name} is {num}% {text} 🌸")


@bot.command()
async def luck(ctx,member:discord.Member=None):
    if member != None :
        num = random.randint(30,100)
        await ctx.send(f"- 🙂 - this is computer's choice don't feel sad if result are bad\n📊 {member.display_name} is {num}% lucky 🍀")
    else :
        num = random.randint(30,100)
        await ctx.send(f"- 🙂 - this is computer's choice don't feel sad if result are bad\n📊 {ctx.author.display_name} is {num}% lucky 🍀")        

@bot.command()
async def nickname(ctx):
    nicknames = [
    "Shadow",
    "Moonlight",
    "Sunshine",
    "Cupcake",
    "Marshmallow",
    "Dragon",
    "Nugget",
    "Peanut",
    "Potato",
    "Pickle",
    "Cookie",
    "Muffin",
    "Panda",
    "Koala",
    "Kitten",
    "Tiger",
    "Wolfie",
    "Bunny",
    "Foxy",
    "Sparkles",
    "Princess",
    "Prince",
    "Legend",
    "Boss",
    "Champ",
    "Captain",
    "Giggles",
    "Troublemaker",
    "Sleepyhead",
    "Cheeseball"
]
    val = random.choice(nicknames)
    await ctx.reply(f"😁**nickname-**{val}")



@bot.command()
async def joke(ctx):
    jokes = [
    "😂 Why don't skeletons fight each other? They don't have the guts.",
    "🤣 I told my computer I needed a break. It said 'No problem, I'll go to sleep.'",
    "😆 Why did the scarecrow win an award? Because he was outstanding in his field.",
    "😂 Why don't eggs tell jokes? They'd crack each other up.",
    "🤣 What do you call fake spaghetti? An impasta.",
    "😆 Why did the math book look sad? Because it had too many problems.",
    "😂 Why can't a bicycle stand on its own? Because it's two tired.",
    "🤣 What do you call cheese that isn't yours? Nacho cheese.",
    "😆 Why did the golfer bring two pairs of pants? In case he got a hole in one.",
    "😂 What do you call a bear with no teeth? A gummy bear.",
    "🤣 Why was six afraid of seven? Because seven ate nine.",
    "😆 Why did the cookie go to the doctor? Because it felt crumbly.",
    "😂 What do you call a fish wearing a bowtie? Sofishticated.",
    "🤣 Why did the tomato blush? Because it saw the salad dressing.",
    "😆 What kind of tree fits in your hand? A palm tree.",
    "😂 Why don't scientists trust atoms? Because they make up everything.",
    "🤣 What do you call a sleeping bull? A bulldozer.",
    "😆 Why did the student eat his homework? Because the teacher said it was a piece of cake.",
    "😂 What do you call an alligator in a vest? An investigator.",
    "🤣 Why did the coffee file a police report? It got mugged.",
    "😂 Why did the chicken join a band? Because it had the drumsticks.",
    "🤣 What do you call a lazy kangaroo? A pouch potato.",
    "😆 Why don't oysters donate to charity? Because they're shellfish.",
    "😂 What do you call a snowman with a six-pack? An abdominal snowman.",
    "🤣 Why was the broom late? It swept in.",
    "😆 Why did the banana go to the doctor? It wasn't peeling well.",
    "😂 What do you call a cow with no legs? Ground beef.",
    "🤣 Why did the stadium get hot after the game? All the fans left.",
    "😆 Why are frogs so happy? They eat whatever bugs them.",
    "😂 Why did the duck get a time out? Because he was acting fowl.",
    "🤣 What do you call a dinosaur that crashes cars? Tyrannosaurus Wrecks.",
    "😆 Why did the computer catch a cold? It left its Windows open.",
    "😂 What do you call a boomerang that won't come back? A stick.",
    "🤣 Why was the belt arrested? For holding up a pair of pants.",
    "😆 What do you call a dog magician? A labracadabrador.",
    "😂 Why did the pillow go to school? To improve its sheet knowledge.",
    "🤣 Why did the smartphone need glasses? It lost its contacts.",
    "😆 What did one wall say to the other wall? I'll meet you at the corner.",
    "😂 Why don't sharks eat clowns? Because they taste funny.",
    "🤣 Why was the calendar so popular? Because it had a lot of dates."
]
    val = random.choice(jokes)
    await ctx.reply(f"🙂**joke-**{val}")


@bot.command()
async def fact(ctx):
    facts = [
    "🐙 Octopuses have three hearts.",
    "🍯 Honey never spoils and can last thousands of years.",
    "🦒 A giraffe's tongue can be up to 20 inches long.",
    "🌍 Earth is the only known planet with life.",
    "🦈 Sharks existed before dinosaurs.",
    "🍌 Bananas are technically berries.",
    "🐧 Penguins can jump up to 6 feet out of water.",
    "☀️ The Sun makes up 99.86% of the Solar System's mass.",
    "🦋 Butterflies taste with their feet.",
    "🐢 Some turtles can breathe through their rear end.",
    "⚡ A lightning bolt is five times hotter than the Sun's surface.",
    "🐨 Koalas sleep up to 22 hours a day.",
    "🌊 More than 80% of the ocean remains unexplored.",
    "🦩 Flamingos are born gray, not pink.",
    "🐘 Elephants can recognize themselves in a mirror.",
    "🌙 The Moon is slowly moving away from Earth every year.",
    "🐬 Dolphins have unique names for each other.",
    "🍎 Apples float because they are 25% air.",
    "🕸️ Spiders can't get caught in their own webs.",
    "🐝 Bees communicate through dancing."
]
    val = random.choice(facts)
    await ctx.reply(f"**fact-**{val}")

@bot.command(name="motivation",aliases=["tell"])
async def tell(ctx):
    thoughts = [
    "🌱 Practice makes a person perfect.",
    "💪 Success comes to those who never give up.",
    "✨ Small steps every day lead to big results.",
    "🌈 Every mistake is a lesson in disguise.",
    "🔥 Hard work beats talent when talent doesn't work hard.",
    "🚀 Your future is created by what you do today.",
    "🌸 Be proud of how far you've come.",
    "⏳ Great things take time.",
    "💎 Pressure creates diamonds.",
    "🌞 A positive mindset changes everything.",
    "📚 Learning never exhausts the mind.",
    "🎯 Focus on progress, not perfection.",
    "🌊 Difficult roads often lead to beautiful destinations.",
    "🦋 Growth begins outside your comfort zone.",
    "🏆 Winners are ordinary people with extraordinary determination.",
    "🌟 Believe in yourself even when nobody else does.",
    "💖 Kindness costs nothing but means everything.",
    "🌳 The best time to plant a tree was years ago. The second best time is now.",
    "🚶 Don't compare yourself to others; compare yourself to yesterday's you.",
    "🎉 Every day is a new chance to become better."
    ]
    val = random.choice(thoughts)
    await ctx.reply(val)

@bot.command(aliases=["flart","me"])
async def compliment(ctx):
    list = ["🌸 You're the kind of person that makes every server better.",
    "😊 Your smile could brighten the darkest day.",
    "💖 You're more amazing than you realize.",
    "✨ You're proof that good people still exist.",
    "🌈 You have a talent for making others feel welcome.",
    "🌟 You bring positive energy wherever you go.",
    "🥰 You're appreciated more than you know.",
    "🎉 You make ordinary moments special.",
    "💫 The server wouldn't be the same without you.",
    "❤️ You're one of the coolest people around."]
    val = random.choice(list)
    await ctx.reply(f"{ctx.author.display_name} - {val}")
@bot.command()
async def rate(ctx,member:discord.Member=None):
    if member == None :
        num = random.randint(30,100)
        text = ""
        if num <= 50 :
            text = ["ok -ok","normal","fine","aah","its ok still i like you"]
        elif num >= 75 :
            text = ["noice","very good","you are best","someone had crush on you ","cutie","pro"]
        elif num >= 90 :
            text = ["legends are here","very very good","hacker","you are best","everone had crush on you","sweety"]
        await ctx.send(f"- 🙂 - this is computer's choice don't feel bad if result are bad\n📊 {member.display_name} is {num}% {random.choice(text)}")
    else :
        num = random.randint(30,100)
        text = ""
        if num <= 50 :
            text = ["ok -ok","normal","fine","aah","its ok still i like you"]
        elif num >= 75 :
            text = ["noice","very good","you are best","someone had crush on you ","cutie","pro"]
        elif num >= 90 :
            text = ["legends are here","very very good","hacker","you are best","everone had crush on you","sweety"]
        await ctx.send(f"- 🙂 - this is computer's choice don't feel bad if result are bad\n📊 {ctx.author.display_name} is {num}% {random.choice(text)}")      
@bot.command(name="choice")
async def choice(ctx, val: str, val2: str):

    messages = [
        "Of course - ",
        "My choice is ",
        "I guess ",
        "Always - ",
        "I'm confused but this - ",
        "Choice = "
    ]

    cho = random.choice([val, val2])
    msg = random.choice(messages)

    await ctx.reply(f"{msg}**{cho}**")
@bot.command()
async def illusion(ctx):
    embed = discord.Embed(title="ILLUSION 😵‍💫",color=discord.Color.blue())
    list = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNnVpdnh3NDUzZnEwdzkxNDFocnljaHk2b2JiaDl0eWcxMTZ1aGkyYiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/IfxBjGrbIK3vwkODkA/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNnVpdnh3NDUzZnEwdzkxNDFocnljaHk2b2JiaDl0eWcxMTZ1aGkyYiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/GmWeN9bM2VCIlxoIfw/giphy.gif","https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNnVpdnh3NDUzZnEwdzkxNDFocnljaHk2b2JiaDl0eWcxMTZ1aGkyYiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/DbFeWEtstFGxFQrTOj/giphy.gif","https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3b3ZlOXRzbWQ5N3ZnczVzc2o4bmwybmNvenl2NzFsYWE0NXM2d2M5NSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/xThuWjALRV2QRodVvy/giphy.gif","https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3bDhrcW5oamdlZjg1ZjkyN2R0cnd6OXd6Mmx5M2ZkOXZ0NXJlMmtsNSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/thiGCB0V7WJdC/giphy.gif"]
    embed.set_image(url=random.choice(list))
    await ctx.send(embed=embed)
@bot.command()
async def debug(ctx):

    embed = discord.Embed(
        title="🐞 Emo Bot Debug Center",
        description="Found a bug, broken command, missing image, or unexpected behavior? Let me know and I'll try to fix it!",
        color=discord.Color.red()
    )

    embed.add_field(
        name="📩 Contact Developer",
        value="[Click here to DM the developer]\nhttps://discord.gg/NpYabKPd",
        inline=False
    )

    embed.add_field(
        name="📝 What to Include",
        value=
        "• Command used\n"
        "• Screenshot (if possible)\n"
        "• Error message\n"
        "• What you expected to happen",
        inline=False
    )

    embed.set_footer(text="Emo Bot • Bug reports help improve the bot ❤️")

    await ctx.reply(embed=embed)
@bot.command()
async def emo(ctx):

    embed = discord.Embed(
        title="🌸 Emo Bot",
        description="A fun community Discord bot featuring economy, truth or dare, wallpapers, stickers, interaction commands, emotions, and more!",
        color=discord.Color.purple()
    )

    embed.add_field(
        name="✨ Features",
        value=
        "💰 Economy System\n"
        "🛒 Wallpapers & Stickers\n"
        "🎭 Truth or Dare\n"
        "💕 Interaction Commands\n"
        "😊 Emotion Commands\n"
        "🎮 Fun Games",
        inline=False
    )

    embed.add_field(
        name="📊 Commands",
        value="**99** commands and growing!",
        inline=False
    )

    embed.set_thumbnail(url=bot.user.display_avatar.url)

    embed.set_footer(text="Made with ❤️ by Neo")

    await ctx.reply(embed=embed)
@bot.command(aliases=["feedback"])
async def fb(ctx):

    embed = discord.Embed(
        title="💡 Emo Bot Feedback",
        description="Have a suggestion, idea, feature request, or complaint? We'd love to hear it!",
        color=discord.Color.green()
    )

    embed.add_field(
        name="🌐 Support Server",
        value="[Join Here]\nhttps://discord.gg/wGxVswvEK",
        inline=False
    )

    embed.add_field(
        name="📝 Feedback Ideas",
        value=
        "• New commands\n"
        "• New games\n"
        "• Economy improvements\n"
        "• UI improvements\n"
        "• Bug reports",
        inline=False
    )

    embed.set_footer(text="Every suggestion helps Emo Bot grow 🌸")

    await ctx.reply(embed=embed)

@bot.command(name="dev", aliases=["developer"])
async def dev(ctx):

    embed = discord.Embed(
        title="👨‍💻 Meet The Developer",
        description="Hi! I'm **Neo**, the creator of **Emo Bot** 🌸",
        color=discord.Color.blurple()
    )

    embed.add_field(
        name="🚀 What I Do",
        value=
        "• Discord Bot Development\n"
        "• Economy Systems\n"
        "• Custom Commands\n"
        "• Truth or Dare Systems\n"
        "• Profile Systems\n"
        "• SQLite Databases\n",
        inline=False
    )

    embed.add_field(
        name="💼 Available For",
        value=
        "• Custom Discord Bots\n"
        "• Bot Fixes & Debugging\n"
        "• New Features\n"
        "• Database Work\n"
        "• Server Management Tools",
        inline=False
    )

    embed.add_field(
        name="📩 Contact Me",
        value="[DM Me Here]\nhttps://discord.gg/NpYabKPd",
        inline=False
    )

    embed.add_field(
        name="🌸 About Emo Bot",
        value=
        "Emo Bot is my personal project built with ❤️ featuring economy, games, wallpapers, stickers, Truth or Dare, and more.",
        inline=False
    )

    embed.set_thumbnail(url=bot.user.display_avatar.url)

    embed.set_footer(
        text="Thanks for using Emo Bot ❤️"
    )

    await ctx.reply(embed=embed)


@bot.event
async def on_ready():
    print(bot.guilds)
    print(f"Servers: {len(bot.guilds)}")

# ___________________________________________________________
@bot.event
async def on_guild_join(guild):
    print(f"Joined: {guild.name}")

    embed = discord.Embed(
        title="🌸 Thanks for adding Emo Bot!",
        description=(
            "Hello everyone! I'm **Emo Bot** 💕\n\n"
            "✨ Economy System\n"
            "🎭 Truth or Dare\n"
            "🛒 Wallpapers & Stickers\n"
            "💕 Interaction Commands\n"
            "😊 Emotion Commands\n\n"
            "Use `e help` to see all commands!"
        ),
        color=discord.Color.purple()
    )

    embed.set_thumbnail(url=bot.user.display_avatar.url)

    try:
        if guild.system_channel:
            await guild.system_channel.send(embed=embed)
            print("Sent to system channel")
            return

        for channel in guild.text_channels:
            perms = channel.permissions_for(guild.me)

            if perms.send_messages and perms.embed_links:
                await channel.send(embed=embed)
                print(f"Sent to {channel.name}")
                return

    except Exception as e:
        print(f"Welcome error: {e}")
# ___________________________________________________________


@bot.command(name="shopwallpaper",aliases=["shopwp","swp"])
async def shop_wp(ctx):
    # ---------------- BUTTONS ----------------

    previous_button = discord.ui.Button(
        label="Previous",
        style=discord.ButtonStyle.gray,
        emoji="⬅️"
    )

    next_button = discord.ui.Button(
        label="Next",
        style=discord.ButtonStyle.gray,
        emoji="➡️"
    )

    view = discord.ui.View()

    view.add_item(previous_button)
    view.add_item(next_button)

    page = 1
    wp1 = "https://raw.githubusercontent.com/Neoknight5/EMO-WALLPAPER-URL/main/download%20(1).jpg"

    wp2 = "https://raw.githubusercontent.com/Neoknight5/EMO-WALLPAPER-URL/main/afbf94d44d85219a24bf99dcfc712e1c.webp"

    wp3 = "https://raw.githubusercontent.com/Neoknight5/EMO-WALLPAPER-URL/main/wp3.jpg"

    wp4 = "https://raw.githubusercontent.com/Neoknight5/EMO-WALLPAPER-URL/main/wp4.jpg"

    wp5 = "https://raw.githubusercontent.com/Neoknight5/EMO-WALLPAPER-URL/main/wp5.jpg"

    wp6 = "https://raw.githubusercontent.com/Neoknight5/EMO-WALLPAPER-URL/main/wp6.jpg"

    wp7 = "https://raw.githubusercontent.com/Neoknight5/EMO-WALLPAPER-URL/main/wp7.jpg"

    wp8 = "https://raw.githubusercontent.com/Neoknight5/EMO-WALLPAPER-URL/main/wp8.jpg"

    wp9 = "https://raw.githubusercontent.com/Neoknight5/EMO-WALLPAPER-URL/main/wp9.jpg"

    wp10 = "https://raw.githubusercontent.com/Neoknight5/EMO-WALLPAPER-URL/main/wp10.jpg"

    # ---------------- PAGE 1 ----------------
    page1 = discord.Embed(
        title="🖼️wallpaper shop",
        description="shop it by using the id `WALLPAPER ID : 1` PRICE : `100K`"
    )
    page1.set_image(url=wp1)

    page2 = discord.Embed(
        title="🖼️wallpaper shop",
        description="shop it by using the id `WALLPAPER ID : 2` PRICE : `270K`"
    )
    page2.set_image(url=wp2)

    page3 = discord.Embed(
        title="🖼️wallpaper shop",
        description="shop it by using the id `WALLPAPER ID : 3` PRICE : `290K`"
    )
    page3.set_image(url=wp3)

    page4 = discord.Embed(
        title="🖼️wallpaper shop",
        description="shop it by using the id `WALLPAPER ID : 4` PRICE : `300K`"
    )
    page4.set_image(url=wp4)

    page5 = discord.Embed(
        title="🖼️wallpaper shop",
        description="shop it by using the id `WALLPAPER ID : 5` PRICE : `320K`"
    )
    page5.set_image(url=wp5 )
    page6 = discord.Embed(
        title="🖼️wallpaper shop",
        description="shop it by using the id `WALLPAPER ID : 6` PRICE : `350K`"
    )
    page6.set_image(url=wp6)
    page7 = discord.Embed(
        title="🖼️wallpaper shop",
        description="shop it by using the id `WALLPAPER ID : 7` PRICE : `380K`"
    )
    page7.set_image(url=wp7)
 

    page8 = discord.Embed(
        title="🖼️wallpaper shop",
        description="shop it by using the id `WALLPAPER ID : 8` PRICE : `400K`"
    )
    page8.set_image(url=wp8)

    page9 = discord.Embed(
        title="🖼️wallpaper shop",
        description="shop it by using the id `WALLPAPER ID : 9` PRICE : `500K`"
    )
    page9.set_image(url=wp9)
    page10 = discord.Embed(
        title="🖼️wallpaper shop",
        description="shop it by using the id `WALLPAPER ID : 10` PRICE : `500K`"
    )
    page10.set_image(url=wp10)
    pages = [page1, page2, page3, page4, page5, page6, page7, page8, page9, page10]
    async def next_callback(interaction):
        nonlocal page
        if page < 10:
            page += 1
            val = pages[page-1]
            val.set_footer(text=f"[{page}||10]")
        await interaction.response.edit_message(embed=pages[page - 1], view=view)

    async def previous_callback(interaction):
        nonlocal page
        if page > 1:
            page -= 1
            val = pages[page-1]
            val.set_footer(text=f"[{page}||10]")
        await interaction.response.edit_message(embed=pages[page - 1], view=view)

    next_button.callback = next_callback
    previous_button.callback = previous_callback

    await ctx.send(embed=page1, view=view)





# _________________BUG FIX BY CLAUDE___________________________________________________________


import discord
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# `coins` is your existing db class, `bot` is your bot instance
# from db import coins
# bot = ...


# ========================================================================
# TABLES
# ========================================================================

def create_wallpaper_table():
    """The shop — every wallpaper that exists to be bought."""
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wallpapers(
        wallpaper_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price INTEGER NOT NULL DEFAULT 0,
        url TEXT NOT NULL
    )
    """)
    conn.commit()


def create_user_wallpaper_table():
    """Ownership — who owns which wallpaper. PRIMARY KEY(user_id, wallpaper_id)
    makes a duplicate purchase structurally impossible, not just
    application-logic-prevented."""
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_wallpapers(
        user_id INTEGER NOT NULL,
        wallpaper_id INTEGER NOT NULL,
        PRIMARY KEY(user_id, wallpaper_id),
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(wallpaper_id) REFERENCES wallpapers(wallpaper_id)
    )
    """)
    conn.commit()


def create_profile_table():
    """Equip state — which ONE wallpaper (if any) is currently active."""
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profiles(
        user_id INTEGER PRIMARY KEY,
        equipped_wallpaper_id INTEGER DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(equipped_wallpaper_id) REFERENCES wallpapers(wallpaper_id)
    )
    """)
    conn.commit()


# ========================================================================
# HELPER FUNCTIONS
# ========================================================================

def add_wallpaper(wallpaper_id: int, name: str, price: int, url: str):
    """Add/update a wallpaper in the shop — for you (admin), not players."""
    cursor.execute(
        "INSERT OR REPLACE INTO wallpapers(wallpaper_id, name, price, url) VALUES(?,?,?,?)",
        (wallpaper_id, name, price, url),
    )
    conn.commit()


def get_wallpaper(wallpaper_id: int):
    cursor.execute("SELECT * FROM wallpapers WHERE wallpaper_id=?", (wallpaper_id,))
    return cursor.fetchone()


def owns_wallpaper(user_id: int, wallpaper_id: int) -> bool:
    cursor.execute(
        "SELECT 1 FROM user_wallpapers WHERE user_id=? AND wallpaper_id=?",
        (user_id, wallpaper_id),
    )
    return cursor.fetchone() is not None


def add_user_wallpaper(user_id: int, wallpaper_id: int):
    cursor.execute(
        "INSERT OR IGNORE INTO user_wallpapers(user_id, wallpaper_id) VALUES(?,?)",
        (user_id, wallpaper_id),
    )
    conn.commit()


def get_profile(user_id: int):
    """Always returns a row — creates one with defaults on first call, so
    callers never have to special-case 'no profile row yet'."""
    cursor.execute("SELECT * FROM profiles WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    if row is None:
        cursor.execute("INSERT OR IGNORE INTO profiles(user_id) VALUES(?)", (user_id,))
        conn.commit()
        cursor.execute("SELECT * FROM profiles WHERE user_id=?", (user_id,))
        row = cursor.fetchone()
    return row


def equip_wallpaper(user_id: int, wallpaper_id: int):
    get_profile(user_id)  # ensure a row exists before updating it
    cursor.execute(
        "UPDATE profiles SET equipped_wallpaper_id=? WHERE user_id=?",
        (wallpaper_id, user_id),
    )
    conn.commit()


def get_equipped_wallpaper(user_id: int):
    """Returns the full wallpaper row the user has equipped, or None if
    they have nothing equipped OR their equipped id no longer exists in
    the shop (self-healing handled in the profile command below)."""
    profile = get_profile(user_id)
    wallpaper_id = profile["equipped_wallpaper_id"]
    if not wallpaper_id:
        return None
    return get_wallpaper(wallpaper_id)


def buy_wallpaper(user_id: int, wallpaper_id: int):
    """Does the whole purchase transaction. Returns (success, reason) —
    reason is a short code the command maps to a user-facing message.
    Kept separate from the Discord command so this same logic is reusable
    later (a shop UI, an admin grant command, etc.) without duplicating it."""
    wallpaper = get_wallpaper(wallpaper_id)
    if wallpaper is None:
        return False, "not_found"

    if owns_wallpaper(user_id, wallpaper_id):
        return False, "already_owned"

    user = coins.get_user(user_id)
    balance = user["coins"]
    if balance < wallpaper["price"]:
        return False, "insufficient_funds"

    coins.update_coins(user_id, balance - wallpaper["price"])
    add_user_wallpaper(user_id, wallpaper_id)
    return True, "ok"


def _download_image(url: str):
    """Returns an RGBA PIL Image, or None on any failure. Logs WHY it
    failed instead of swallowing the exception silently."""
    if not url:
        print("[_download_image] called with an empty/None url")
        return None
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return Image.open(BytesIO(response.content)).convert("RGBA")
    except Exception as e:
        print(f"[_download_image] failed for url={url!r}: {e!r}")
        return None


# call once at startup, after your existing table-creation calls:
create_wallpaper_table()
create_user_wallpaper_table()
create_profile_table()


# ========================================================================
# COMMANDS




# ========================================================================

@bot.command(name="buywp")
async def buy_wp(ctx, wallpaper_id: int):
    user_id = ctx.author.id

    if not coins.user_exists(user_id):
        await ctx.reply("😢 You don't have an account.\nUse `e start` first.")
        return

    success, reason = buy_wallpaper(user_id, wallpaper_id)

    if not success:
        messages = {
            "not_found": "😅 That wallpaper doesn't exist.",
            "already_owned": "😏 You already own this wallpaper.",
            "insufficient_funds": "😢 You don't have enough coins for that.",
        }
        await ctx.reply(messages.get(reason, "😵 Something went wrong."))
        return

    wallpaper = get_wallpaper(wallpaper_id)
    embed = discord.Embed(
        title="🎉 You bought a new wallpaper!",
        description=(
            f"🆔 ID: **{wallpaper['wallpaper_id']}**\n"
            f"🏷 Name: **{wallpaper['name']}**\n"
            f"💰 Price: **{wallpaper['price']}** coins"
        ),
        color=discord.Color.blue(),
    )
    embed.set_thumbnail(url=wallpaper["url"])
    await ctx.reply(embed=embed)


@bot.command(name="equipwp",aliases=["ewp","equipwallpaper"])
async def equip_wp(ctx, wallpaper_id: int):
    user_id = ctx.author.id

    if not coins.user_exists(user_id):
        await ctx.reply("😢 You don't have an account.\nUse `e start` first.")
        return

    wallpaper = get_wallpaper(wallpaper_id)
    if wallpaper is None:
        await ctx.reply("😅 That wallpaper doesn't exist.")
        return

    if not owns_wallpaper(user_id, wallpaper_id):
        await ctx.reply("😏 You don't own that wallpaper yet — try `e buywp` first.")
        return

    if not wallpaper["url"]:
        await ctx.reply("😵 That wallpaper has no image URL set — contact an admin.")
        return

    equip_wallpaper(user_id, wallpaper_id)

    embed = discord.Embed(
        title="✅ Wallpaper equipped!",
        description=f"🖼 **{wallpaper['name']}** is now your active wallpaper.",
        color=discord.Color.green(),
    )
    embed.set_thumbnail(url=wallpaper["url"])
    await ctx.reply(embed=embed)


@bot.command()
async def profile(ctx):
    user_id = ctx.author.id

    if not coins.user_exists(user_id):
        await ctx.send("😢 You don't have an account yet — create one with `e start`.")
        return
    data = coins.get_user(user_id)
    coin = data["coins"]
    xp = data["xp"]

    canvas_size = Image.open("default_profile.png").size
    profile_img = None

    equipped = get_equipped_wallpaper(user_id)
    if equipped is not None:
        profile_img = _download_image(equipped["url"])
        if profile_img is None:
            print(
                f"[profile] user {user_id}'s equipped wallpaper "
                f"(id={equipped['wallpaper_id']}) failed to load from "
                f"url={equipped['url']!r}"
            )
    elif get_profile(user_id)["equipped_wallpaper_id"]:
        # equipped id is set but points at a wallpaper no longer in the
        # shop — self-heal so this doesn't repeat every profile call
        stale_id = get_profile(user_id)["equipped_wallpaper_id"]
        print(f"[profile] user {user_id}'s equipped wallpaper (id={stale_id}) "
              "no longer exists — resetting")
        equip_wallpaper(user_id, 0)

    if profile_img is None:
        profile_img = Image.open("default_profile.png").convert("RGBA")

    profile_img = profile_img.resize(canvas_size)
    draw = ImageDraw.Draw(profile_img)

    # ---------------- avatar ----------------
    avatar = _download_image(ctx.author.display_avatar.url)
    if avatar is not None:
        avatar = avatar.resize((220, 220))
        profile_img.paste(avatar, (50, 50), avatar)

    # ---------------- text ----------------
    font = ImageFont.truetype("arial.ttf", 30)
    big_font = ImageFont.truetype("arial.ttf", 70)
    username = ctx.author.display_name

    draw.text((320, 60), username, font=big_font, fill="#3B1E7F")
    draw.text((320, 150), f"💰 {coin} coins", font=font, fill="white")
    draw.text((320, 200), f"{xp} XP", font=font, fill="white")
    draw.text((100,480),"AN POOKIE >.< user of EMO bot ",font=font,fill="#3B1E7F")

    # ---------------- xp bar ----------------
    max_xp = 1000
    progress = min(xp / max_xp, 1)

    bar_x1, bar_y1 = 340, 260
    bar_width, bar_height = 300, 25
    bar_x2, bar_y2 = bar_x1 + bar_width, bar_y1 + bar_height

    draw.rounded_rectangle((bar_x1, bar_y1, bar_x2, bar_y2), radius=10, fill=(60, 60, 60))
    fill_x2 = bar_x1 + int(bar_width * progress)
    draw.rounded_rectangle((bar_x1, bar_y1, fill_x2, bar_y2), radius=10, fill=(0, 255, 255))
    draw.rounded_rectangle((bar_x1, bar_y1, bar_x2, bar_y2), radius=10, outline="white", width=2)
    draw.text((bar_x1 + 90, bar_y1 - 30), f"{xp}/{max_xp} XP", font=font, fill="#304655")

    # ---------------- send ----------------
    buffer = BytesIO()
    profile_img.save(buffer, format="PNG")
    buffer.seek(0)
    await ctx.send(file=discord.File(fp=buffer, filename="profile.png"))


# wp1 = "https://raw.githubusercontent.com/Neoknight5/EMO-WALLPAPER-URL/main/download%20(1).jpg"

# wp2 = "https://raw.githubusercontent.com/Neoknight5/EMO-WALLPAPER-URL/main/afbf94d44d85219a24bf99dcfc712e1c.webp"

# wp3 = "https://raw.githubusercontent.com/Neoknight5/EMO-WALLPAPER-URL/main/wp3.jpg"

# wp4 = "https://raw.githubusercontent.com/Neoknight5/EMO-WALLPAPER-URL/main/wp4.jpg"

# wp5 = "https://raw.githubusercontent.com/Neoknight5/EMO-WALLPAPER-URL/main/wp5.jpg"

# wp6 = "https://raw.githubusercontent.com/Neoknight5/EMO-WALLPAPER-URL/main/wp6.jpg"

# wp7 = "https://raw.githubusercontent.com/Neoknight5/EMO-WALLPAPER-URL/main/wp7.jpg"

# wp8 = "https://raw.githubusercontent.com/Neoknight5/EMO-WALLPAPER-URL/main/wp8.jpg"

# wp9 = "https://raw.githubusercontent.com/Neoknight5/EMO-WALLPAPER-URL/main/wp9.jpg"

# wp10 = "https://raw.githubusercontent.com/Neoknight5/EMO-WALLPAPER-URL/main/wp10.jpg"


# add_wallpaper(1,"wp1",100000,wp1)
# add_wallpaper(2,"wp2",270000,wp2)
# add_wallpaper(3,"wp3",290000,wp3)
# add_wallpaper(4,"wp4",300000,wp4)
# add_wallpaper(5,"wp5",320000,wp5)
# add_wallpaper(6,"wp6",350000,wp6)
# add_wallpaper(7,"wp7",380000,wp7)
# add_wallpaper(8,"wp8",400000,wp8)
# add_wallpaper(9,"wp9",500000,wp9)
# add_wallpaper(10,"wp10",500000,wp10)





print(f"Bot has {len(bot.commands)} commands")

import os

bot.run(os.getenv("TOKEN"))
