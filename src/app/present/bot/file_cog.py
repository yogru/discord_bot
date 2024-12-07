import os

from discord.ext import commands

from src.dependencies import file_use_case
from src.domain.model import FileStorageEnum


class FileCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='upload_file', aliases=['uf'], help='{upload_file, uf} 파일 업로드 기능 예)!uf 태그1 태그2 태그3')
    async def upload_file(self, ctx, *, user_input: str):
        tags = user_input.split(' ')
        if not tags:
            await ctx.send(f"태그를 지정 해주세요")
            return
        if not ctx.message.attachments:
            await ctx.send("파일을 첨부 하세요")
            return
        attachment = ctx.message.attachments[0]
        filename = attachment.filename
        save_path = f"./downloads/{filename}"
        # 파일 다운로드 및 저장
        await attachment.save(save_path)
        await ctx.send(f"`{filename}` 로컬로 저장 되었습니다.")
        file_use_case.upload_file(
            user_id=ctx.author.name,
            filename=filename,
            saved_path=save_path,
            tags=tags,
            storage=FileStorageEnum.MIN_IO,
            url=None
        )
        await ctx.send(f"`{filename}` 파일 서버로 저장 되었습니다.")
        os.remove(save_path)

    @commands.command(name='get_url', aliases=['g'], help='{get_url, g} 파일 조회 예)!g 태그1 태그2 태그3')
    async def get_url(self, ctx, *, user_input: str):
        tags = user_input.split(' ')
        if not tags:
            await ctx.send(f"태그를 지정 해주세요")
            return
        urls = file_use_case.get_url(tags=tags)
        await ctx.send(f"{" ".join(urls)}")


async def setup(bot):
    await bot.add_cog(FileCog(bot))
