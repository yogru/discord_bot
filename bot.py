import discord
from discord.ext import commands

from src.dependencies import env, gpt

# 봇 초기화
intents = discord.Intents.default()
intents.message_content = True  # 메시지 콘텐츠 접근 허용
bot = commands.Bot(command_prefix='!', intents=intents)

m_dict = {

}


# 봇이 준비되었을 때
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')


# 간단한 명령어 추가
@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.name}!')


@bot.command()
async def m(ctx, *, user_input: str):
    if ctx.author.name == "brony2684":
        d = m_dict.get(ctx.author.name, [])
        d.append(user_input)
        m_dict[ctx.author.name] = d


@bot.command()
async def mc(ctx, *, user_input: str):
    if ctx.author.name == "brony2684":
        m_dict[ctx.author.name] = []


@bot.command()
async def c(ctx, *, user_input: str):
    if ctx.author.name == "brony2684":
        prompt_list = m_dict.get(ctx.author.name, [])
        messages = prompt_list.copy()
        messages.append(user_input)
        gpt.add_message(role='user', message=' '.join(messages))
        ret = gpt.compilation()
        await ctx.send(ret)
        return
    await ctx.send(f'선생님 돈내세요, {ctx.author.name}!')


@bot.command()
async def k(ctx):
    image_url = 'https://cdn.discordapp.com/attachments/1064150890761691159/1313424686587052032/IMG_3133.webp?ex=6750158f&is=674ec40f&hm=b3173fe15dc33f799b15633b63f30dd4191b32c88880dde331b8ab446d407689&'
    await ctx.send(image_url)


# 봇 실행
bot.run(env.BOT_KEY)
