from discord.ext import commands


class FileCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='vote', help="투표 기능: 질의 옵션1 옵션2 옵션3.. (최대 10개까지) ")
    async def vote(self, ctx, *, question_and_options):
        # 사용자가 입력한 질문과 옵션 분리
        parts = question_and_options.split(" ")
        if len(parts) < 2:
            await ctx.send("올바른 형식으로 입력해주세요. 예: !vote \"질문\" \"옵션1\" \"옵션2\"")
            return

        question = parts[0]
        options = parts[1:]

        if len(options) > 10:
            await ctx.send("최대 10개의 옵션만 지원됩니다.")
            return

        # 이모지 목록 (1~10까지 숫자 이모지)
        emoji_list = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

        # 투표 메시지 생성
        description = f"**{question}**\n\n"
        for i, option in enumerate(options):
            description += f"{emoji_list[i]}: {option}\n"

        embed = self.bot.Embed(title="📊 투표", description=description, color=0x00FF00)
        message = await ctx.send(embed=embed)

        # 옵션에 따라 이모지 추가
        for i in range(len(options)):
            await message.add_reaction(emoji_list[i])


async def setup(bot):
    await bot.add_cog(FileCog(bot))
