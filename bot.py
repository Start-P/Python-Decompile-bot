import os
import subprocess
from shlex import quote

import discord

def Decompiler(file_name):
    file_name = quote(file_name)
    adjusted_file_name = ".".join(file_name.split(".")[:-1])
    pyc_path = adjusted_file_name + ".pyc"
    extract_folder_path = file_name + "_extracted"
    extract_pyc_path = extract_folder_path + "/" + pyc_path
    os.system(f"python3 pyinstxtractor.py {file_name}")
    os.system(f"cp {extract_pyc_path} {pyc_path}")
    os.system(f"rm -rf {extract_folder_path}")
    os.system(f"rm -rf {file_name}")
    result = subprocess.run(["pycdc", pyc_path], text=True, capture_output=True).stdout
    with open(f"{adjusted_file_name}.py", "w") as f:
        f.write(result)

    return adjusted_file_name + ".py"

client = discord.Client(intents=discord.Intents.all())
token = "TOKEN HERE"
alias_list = ["decompile", "dc"]

@client.event
async def on_ready():
    print("Running as", client.user.name)

@client.event
async def on_message(msg):
    content = msg.content.lower()
    if content.startswith("!"):
        if content.replace("!", "") in alias_list:
            attachment = msg.attachments
            if attachment:
                filename = attachment[0].filename
                await attachment[0].save(filename)
                decompiled_file_name = Decompiler(filename)
                await msg.reply(file=discord.File(decompiled_file_name))

client.run(token)
