import discord
from discord.ext import commands

from discord.ui import View, Button, Modal, TextInput

from src.dependencies import auth_use_case, chat_use_case
from src.domain.model import UserGrantEnum


class PersonaModal(Modal, title="페르소나 생성"):
    title_input = TextInput(
        label="제목",
        placeholder="페르소나 제목을 입력하세요",
        style=discord.TextStyle.short,
        required=True
    )
    prompt_input = TextInput(
        label="내용",
        placeholder="페르소나 내용을 입력하세요",
        style=discord.TextStyle.paragraph,
        required=True
    )

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    async def on_submit(self, interaction):
        try:
            # 권한 확인
            auth_use_case.check_grant(
                user_id=self.user_id,
                grant_enum=UserGrantEnum.USE_CHAT_BOT
            )

            # 페르소나 생성
            ret = chat_use_case.create_prompt(
                user_id=self.user_id,
                title=self.title_input.value,
                prompt=self.prompt_input.value,
            )
            await interaction.response.send_message(
                f"페르소나가 성공적으로 생성되었습니다.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"오류가 발생했습니다: {e}",
                ephemeral=True
            )


class PersonaView(View):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    @discord.ui.button(label="페르소나 생성", style=discord.ButtonStyle.green)
    async def create_persona(self, interaction, button):
        # 버튼 클릭 시 모달 표시
        modal = PersonaModal(user_id=self.user_id)
        await interaction.response.send_modal(modal)


class ChatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='chat', aliases=['c'], help='{chat, c} 챗봇 기능')
    async def chat(self, ctx, *, user_input: str):
        auth_use_case.check_grant(
            user_id=ctx.author.name,
            grant_enum=UserGrantEnum.USE_CHAT_BOT
        )
        answer = chat_use_case.create_chat(
            user_id=ctx.author.name,
            question=user_input,
        )
        await ctx.send(answer)

    @commands.command(name='persona', aliases=['p'], help='{persona, p} 페르소나 추가 기능 예제)!p 제목 내용')
    async def persona(self, ctx):
        auth_use_case.check_grant(
            user_id=ctx.author.name,
            grant_enum=UserGrantEnum.USE_CHAT_BOT
        )
        view = PersonaView(user_id=ctx.author.name)
        await ctx.send("아래 버튼을 클릭하여 페르소나를 생성하세요.", view=view)


async def setup(bot):
    await bot.add_cog(ChatCog(bot))
