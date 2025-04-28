from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
from string import hexdigits

cache = dict()
EMBED_BASE_URL = "https://gogoplay.io/streaming.php?id=" # <-- Set your new embed base here


def get_hash(data, back):
    while True:
        hash = "".join(random.choices(hexdigits, k=10))
        if not cache.get(hash):
            cache[hash] = (data, back)
            break
    return hash


def get_hash_btn(data=None, hash=None):
    if hash:
        cache[hash] = data
        return hash

    while True:
        new_hash = "".join(random.choices(hexdigits, k=10))
        if not cache.get(new_hash):
            cache[new_hash] = data or ""
            break
    return new_hash


def get_hash_anime(data):
    while True:
        hash = "".join(random.choices(hexdigits, k=10))
        if not cache.get(hash):
            cache[hash] = data
            break
    return hash


class BTN:
    @staticmethod
    def searchCMD(id, data, back):
        temp = []
        for i in data:
            cb = f"AnimeS {id} " + get_hash(i["id"], back)
            temp.append([InlineKeyboardButton(text=i["title"], callback_data=cb)])
        
        pos = len(temp)
        hash = get_hash_btn()

        if len(temp) > 10:
            b_parts = []
            x = 0
            page = 0

            while pos > 10:
                t = temp[x:x+10]
                if not t:
                    break
                b_parts.append(t)
                x += 10
                pos -= 10

                if page == 0:
                    b_parts[page].append([
                        InlineKeyboardButton(text="Next ⫸", callback_data=f"switch_anime {id} {hash} 1")
                    ])
                else:
                    b_parts[page].append([
                        InlineKeyboardButton(text="⫷ Prev", callback_data=f"switch_anime {id} {hash} {page-1}"),
                        InlineKeyboardButton(text="Next ⫸", callback_data=f"switch_anime {id} {hash} {page+1}")
                    ])
                page += 1

            if pos > 0:
                b_parts.append(temp[x:])
                b_parts[page].append([
                    InlineKeyboardButton(text="⫷ Prev", callback_data=f"switch_anime {id} {hash} {page-1}")
                ])

            get_hash_btn((b_parts, back), hash)
            return InlineKeyboardMarkup(b_parts[0])
        else:
            return InlineKeyboardMarkup(temp)

    @staticmethod
    def AnimeS(id, data, back):
        temp = []
        x = []
        pos = 1

        for i in data:
            cb = f"episode {id} " + get_hash(i[1], back)
            x.append(InlineKeyboardButton(text=i[0], callback_data=cb))
            if pos % 4 == 0:
                temp.append(x)
                x = []
            pos += 1

        if x:
            temp.append(x)

        hash = get_hash_btn()

        if len(temp) > 23:
            b_parts = []
            x = 0
            page = 0

            while len(temp) - x > 23:
                t = temp[x:x+23]
                if not t:
                    break
                b_parts.append(t)
                x += 23

                if page == 0:
                    b_parts[page].append([
                        InlineKeyboardButton(text="Back", callback_data=f"searchBACK {id} {back}"),
                        InlineKeyboardButton(text="Next ⫸", callback_data=f"switch_ep {id} {hash} 1")
                    ])
                else:
                    b_parts[page].append([
                        InlineKeyboardButton(text="⫷ Prev", callback_data=f"switch_ep {id} {hash} {page-1}"),
                        InlineKeyboardButton(text="Next ⫸", callback_data=f"switch_ep {id} {hash} {page+1}")
                    ])
                b_parts[page].append([
                    InlineKeyboardButton(text="Back", callback_data=f"searchBACK {id} {back}")
                ])
                page += 1

            if len(temp) - x > 0:
                b_parts.append(temp[x:])
                b_parts[page].append([
                    InlineKeyboardButton(text="⫷ Prev", callback_data=f"switch_ep {id} {hash} {page-1}"),
                    InlineKeyboardButton(text="Back", callback_data=f"searchBACK {id} {back}")
                ])

            get_hash_btn((b_parts, back), hash)
            return InlineKeyboardMarkup(b_parts[0])
        else:
            temp.append([
                InlineKeyboardButton(text="Back", callback_data=f"searchBACK {id} {back}")
            ])
            return InlineKeyboardMarkup(temp)

    @staticmethod
    def episode(id, surl, murl, back, dl_open_cb):
        temp = []

        temp.append([InlineKeyboardButton(text="⬇️ Direct Url ⬇️", callback_data="engSUB")])

        x = []
        pos = 1
        for i in surl:
            x.append(InlineKeyboardButton(text=i[0], url=f"{EMBED_BASE_URL}{i[1]}"))
            if pos % 3 == 0:
                temp.append(x)
                x = []
            pos += 1
        if x:
            temp.append(x)

        if murl:
            temp.append([InlineKeyboardButton(text="➖➖➖➖➖➖➖➖➖➖", callback_data="line")])
            temp.append([InlineKeyboardButton(text="⬇️ Mirror Url ⬇️", callback_data="engDUB")])

            x = []
            pos = 1
            for i in murl:
                x.append(InlineKeyboardButton(text=i[0].title(), url=i[1]))
                if pos % 3 == 0:
                    temp.append(x)
                    x = []
                pos += 1
            if x:
                temp.append(x)

        temp.append([InlineKeyboardButton(text="📥 Download 📥", callback_data=dl_open_cb)])
        temp.append([InlineKeyboardButton(text="Back", callback_data=f"AnimeS {id} {back}")])

        return InlineKeyboardMarkup(temp)

    @staticmethod
    def download(id, links, back):
        temp = []

        for q, l in links.items():
            resolution = q.split("x")[1] + "p"
            temp.append([InlineKeyboardButton(text=resolution, url=l)])

        temp.append([InlineKeyboardButton(text="Back", callback_data=back)])
        return InlineKeyboardMarkup(temp)