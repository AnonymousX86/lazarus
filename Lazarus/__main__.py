# -*- coding: utf-8 -*-
from logging import basicConfig, getLogger
from os import environ

from discord import Intents, ApplicationContext, Embed, Color, Option
from discord.ext.commands import Bot
from requests import get
from rich.logging import RichHandler

from Lazarus.utils.wiki import WikiPagePreview, get_wiki_snippet

if __name__ == '__main__':
    basicConfig(
        level='INFO',
        format='%(message)s',
        datefmt='[%x]',
        handlers=[RichHandler()]
    )
    log = getLogger('rich')
    bot = Bot(
        command_prefix='lz!',
        description='Bot for a Witcher\'s fan',
        intents=Intents.default(),
        owner_id=309270832683679745
    )
    bot.log = log

    @bot.event
    async def on_ready():
        log.info(f'✅ Logged in as {bot.user}')


    @bot.slash_command(
        name='ping',
        description='Check bot\'s latency'
    )
    async def ping(ctx: ApplicationContext):
        await ctx.respond(embed=Embed(
            title='Pong!',
            color=Color.blurple()
        ).add_field(
            name='Latency',
            value=f'{round(bot.latency * 1000)}ms'
        ))


    @bot.slash_command(
        name='hello',
        description='Introduce yourself to the bot'
    )
    async def hello(
            ctx: ApplicationContext,
            name: Option(str, 'What\'s your name?')
    ) -> None:
        embed = Embed(
            title=f'Hello, {name}!',
            color=Color.blurple()
        )
        await ctx.respond(embed=embed)

    @bot.slash_command(
        name='wiki_search',
        description='Search Witcher Wiki'
    )
    async def wiki_search(ctx: ApplicationContext, query: Option(str, 'What do you want to search?')):
        req = get(
            'https://witcher.fandom.com/api.php'
            '?action=query'
            '&format=json'
            '&assert=anon'
            '&prop='
            '&list=search'
            '&utf8=1'
            '&srsearch={}'
            '&srnamespace=0'
            '&srlimit=12'.format(query)
        )
        if req.status_code != 200:
            await ctx.respond(embed=Embed(
                title='Wiki unreachable'
            ))
        else:
            await ctx.respond(embed=Embed(
                title=':hourglass: Loading...',
                color=Color.gold()
            ))
            res = req.json()
            pages = [WikiPagePreview(x['title'], x['pageid']) for x in res['query']['search']]
            embed=Embed(
                title='Results',
                description=f'Of search: `{query}`'
            )
            for index, page in enumerate(pages, start=1):
                embed.add_field(
                    name='{}{}. *{}*'.format("0" if index < 10 else "", index, page.title),
                    value=f'> {get_wiki_snippet(page.page_id)}\n'
                          f'[ [Wiki](https://witcher.fandom.com/wiki/{page.title.replace(" ", "_")}) ]'
                )
            await ctx.edit(embed=embed)

    bot.run(environ.get('BOT_TOKEN'))
