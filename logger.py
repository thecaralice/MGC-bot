import logging
import logging.handlers as handlers
import requests
import traceback
from datetime import datetime as dt

a =  None

colors =  {
    'DEBUG': 0x00ff00,
    'INFO': 0xffff00,
    'WARNING': 0xff7700,
    'ERROR': 0xff0000,
    'CRITICAL': 0x770000
}

class DiscordHandler(logging.Handler):
    def __init__(self, url, level=logging.NOTSET):
        logging.Handler.__init__(self)
        self.url = url
        self.level = level
    
    def emit(self, record: logging.LogRecord):
        print(record.msg, record.args, record.msg % record.args)
        em = {'embeds':
              [
                  {'title': record.levelname.capitalize(),
                   'description': record.msg % record.args,
                   'color': colors[record.levelname],
                   'timestamp': dt.fromtimestamp(record.created).isoformat(),
                   'author': {
                       'name': record.name,
                   },
                   'fields': [
                       {
                           'name': 'File',
                           'value': record.pathname
                        },
                       {
                           'name': 'Function',
                           'value': record.funcName,
                       }
                   ]
                   }
              ]
              } 
        if record.levelname == 'ERROR':
            em['embeds'][0]['description'] = f'```py\n{"".join(traceback.format_exception(*record.exc_info))}```'
            em['embeds'][0]['fields'].append(
                {
                    'name': 'Message',
                    'value': record.msg
                }
            )           
        requests.post(url=self.url, json=em)            

logging.basicConfig(format="%(levelname)s -- %(name)s.%(funcName)s : %(message)s", level=logging.INFO)

dhandler = DiscordHandler('https://discordapp.com/api/webhooks/558371669865922571/Jc5HdfqbnNHCtRjvP9weEy0rrrzCyDSvjdgRXhjnAhlDP8jjoBgXJgAKBFMyobZxvA63')
fhandler = logging.FileHandler('logs.log')
_fhandler = logging.FileHandler('logs.log')
_fhandler.setLevel(logging.DEBUG)

_liblogger = logging.getLogger('discord')
_liblogger.setLevel(level=logging.WARNING)
_liblogger.addHandler(dhandler)
_liblogger.addHandler(fhandler)

logger = logging.getLogger('MGC-bot')
logger.setLevel(level=logging.DEBUG)
logger.addHandler(dhandler)
logger.addHandler(fhandler)