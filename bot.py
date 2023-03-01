import pickle

from asyncio import get_event_loop

from pyrogram import Client, filters, idle


classifiers = [
    (
        f"classifier{i}.pkl",
        [
            "a",
            "Toxic",
            "SevereToxic",
            "Obscene",
            "Threat",
            "IdentityHate",
            "Insult",
            "NonToxic",
        ][i],
    )
    for i in range(1, 8)
]
classifiers_dict = {}

for i, j in classifiers:
    with open(i, "rb") as f:
        classifiers_dict[j] = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

client = Client(
    in_memory=True,
    name="bot",
    bot_token="5688227296:AAFPg1r2cOb3dDuoy0FSyL0bnGYSM2eIv4w",
    api_id=6,
    api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e",
)


@client.on_message(filters.private)
async def a_(_, message):
    user_input = message.text

    vector = vectorizer.transform([user_input])
    text = ""

    for i in classifiers_dict:
        text += f"**{i.title()}:** {int(classifiers_dict[i].predict_proba(vector)[0][1] * 100)}\n"
    await message.reply(text)

client.run()
