import discord
import asyncio
from EZPaginator import Paginator

class Expander(Paginator):
    def __init__(self, ctx, message, contents=None, embeds=None, timeout=60, only=None):
        super().__init__(ctx, message, contents=contents, embeds=embeds, timeout=timeout, use_more=False, only=only)
        self.reactions = ["⬆️", "⬇️"]
    
    async def pagination(self, emoji):
        
        if str(emoji) == "⬇️":
            await self.go_first()
        elif str(emoji) == "⬆️":
            await self.go_last()
    
    async def start(self):
        await self.add_reactions()

        while True:
            try:
                add_reaction = asyncio.ensure_future(
                    self.ctx.wait_for(
                        "raw_reaction_add", check=self.emoji_checker
                    )
                )
                remove_reaction = asyncio.ensure_future(
                    self.ctx.wait_for(
                        "raw_reaction_remove", check=self.emoji_checker
                    )
                )

                done, pending = await asyncio.wait(
                    (add_reaction, remove_reaction),
                    return_when=asyncio.FIRST_COMPLETED,
                    timeout=self.timeout,
                )

                for i in pending:
                    i.cancel()

                if len(done) == 0:
                    raise asyncio.TimeoutError()

                payload = done.pop().result()  ## done : set
                await self.pagination(payload.emoji)

            except asyncio.TimeoutError:
                try:
                    await self.message.clear_reactions()
                    await self.go_first()
                    break
                except (discord.Forbidden, discord.HTTPException):
                    break