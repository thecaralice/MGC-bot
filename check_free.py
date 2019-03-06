from discord_webhook import DiscordEmbed, DiscordWebhook
import aiohttp
import asyncio
import async_timeout
import requests
import lxml.html

async def get_free_games(session=aiohttp.ClientSession()):
    with async_timeout.timeout(10):
        async with session.get("https://freesteam.ru/category/active/") as response:
            r = await response.text()
    doc = lxml.html.document_fromstring(r)

    xpath = '//*[@id="blog-grid"]/div'
    a = doc.xpath(xpath)
    b = []  
    for i in a[::-1]:
        href = i[0][0][0].get('href')
        with async_timeout.timeout(10):
            async with session.get(href) as response:
                r = await response.text()
        page = lxml.html.document_fromstring(r)    
        yield {
            'title': page.xpath('//*[@id="main"][1]/article/header/h1')[0].text_content(),
            'url': href,
            'author': page.xpath('//*[@id="main"][1]/article/header/div[3]/span[3]')[0].text_content(),
            'author_url': page.xpath('//*[@id="main"][1]/article/header/div[3]/span[3]')[0].get('href'),
            'author_image': page.xpath('//*[@id="main"][1]/article/header/div[3]/span[1]/img')[0].get('src').split('?')[0] + '.png',
            'text':'\n'.join([j.text_content() for j in page.xpath('//*[@id="main"][1]/article/div[1]/p')]),
            'image': page.xpath('//*[@id="main"][1]/article/header/div[1]/img')[0].get('src')
               }
    #return b

async def main():
    with open('games.txt') as f:
        urls = f.read().split('\n')
    while True:
        async for i in get_free_games():
            if i['url'] not in urls:
                webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/548562668223725569/MYPKHBCbVorW4L_4Z1hd63J5BFhOCMbdYTdGkTcasvxSzVWdmORqaFI_nRSLTe6UQTZA', username='FreeSteam.ru', avatar_url='https://pp.userapi.com/c9343/v9343466/1f61/hE9ubFnmzEc.jpg')
                embed = DiscordEmbed(title=i['title'], description=i['text'], url=i['url'], color=0x0000aa, image={'url':i['image']})   
                embed.set_author(name=i['author'], url=i['author_url'], icon_url=i['author_image'])
                embed.set_footer(text='Сделал •MGC•Mr_ChAI#7272', icon_url='https://cdn.discordapp.com/avatars/426757590022881290/3bd1ba31dd8eeeff839cb9be406ee1c3.png')
                webhook.add_embed(embed)
                print(len(embed.description), embed.__dict__)
                webhook.execute()
                with open('games.txt', 'a') as f:
                    f.write(i['url'] + '\n')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())