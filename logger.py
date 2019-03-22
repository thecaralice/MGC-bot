import logging
import logging.handlers as handlers
import traceback
import  datetime

from discord_webhook import DiscordEmbed, DiscordWebhook

colors =  {
    'DEBUG': 0x0,
    'INFO': 0x0,
    'WARNING': 0x0,
    'ERROR': 0x0,
    'CRITICAL': 0x0
}

class DiscordHandler(logging.Handler):
    def __init__(self, url, level=logging.NOTSET):
        logging.Handler.__init__(self)
        self.url = url
        self.level = level
    
    def emit(self, record: logging.LogRecord):
        global a,  e
        a = record
        webhook = DiscordWebhook(self.url, username='Logger', avatar_url='https://cdn.discordapp.com/avatars/543148124768829451/44d1ec20a0fa7f35ca4b7aec4b8b4af7.png')
        embed = DiscordEmbed(title=record.levelname.capitalize(),
                             description=record.msg,
                             color=colors[record.levelname])
        embed.set_author(name=record.name)
        embed.add_embed_field(name='Module', value=record.module)
        embed.add_embed_field(name='File', value=record.pathname)
        embed.add_embed_field(name='Function', value=record.funcName)
        embed.add_embed_field(name='Process', value=record.processName)
        embed.add_embed_field(name='Thread', value=record.threadName)
        if record.levelname == 'ERROR':
            embed.add_embed_field(name='Exception', value = f'```py\n{"".join(traceback.format_exception(*record.exc_info))}```')
            webhook.add_file(record.pathname, record.filename)
        webhook.add_embed(embed)
        webhook.execute()
        

handler = DiscordHandler('https://canary.discordapp.com/api/webhooks/557957697597603840/Fm2r0kAVZ5cdNmpEAinX_XdtfKnoBc4f0MXrnEancMvWhCL38L67kSxViDVGyxjEv3b-')

_liblogger = logging.getLogger('discord')
_liblogger.setLevel(level=logging.WARNING)
_liblogger.addHandler(handler)

logger = logging.getLogger('MGC-bot')
logger.setLevel(level=logging.DEBUG)
logger.addHandler(handler)