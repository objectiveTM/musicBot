from .emojis import *
from .musicSearch import *
from .colors import *
from .locale import *

DISCORD = "https://discord.com/invite/w2Fw7UeZmY" #자신의 디스코드 url
ADD = "https://discord.com/oauth2/authorize?client_id=871348411356545057&permissions=8&scope=bot%20applications.commands" #자신의 봇추가 url

def isKo(inter:Interaction):
    return inter.locale == "ko"
