import func , json
import nextwave as wavelink
from func import emojis
from nextcord import *

@client.slash_command(name = "misic" , description = "play music" , name_localizations=func.locale("음악" , "music") , description_localizations=func.locale("음악" , "music"))
async def 음악(inter : Interaction , 검색 : str = SlashOption(name = "query" , description = "Write a song to search" , name_localizations=func.locale("검색" , "query") , description_localizations=func.locale("검색할 곡을 쓰세요" , "Write a song to search"))):
    func.musicSearch(user = inter.user , text = 검색).read()
    try: inter.user.voice.channel
    except:
        if func.isKo(inter):
            await inter.response.send_message(embed = Embed(title = "엥...?" , description = "음성채널에 먼저 들어가주세요!" , color=func.PERPLE) , ephemeral=True)
        else:
            await inter.response.send_message(embed = Embed(title = "Eh...?" , description = "Please join the voice channel first!" , color=func.PERPLE) , ephemeral=True)
        return
    await inter.response.defer()
    
    t = 0
    try:
        vc : wavelink.Player = await inter.user.voice.channel.connect(cls = wavelink.Player)
        vc.loop = True
    except:
        for voiceChannel in inter.guild.voice_channels:
            if (client.user in voiceChannel.members):
                t = 1
                if (len(voiceChannel.members) <= 2):
                    vc : wavelink.Player = inter.guild.voice_client
                    break
        if (t == 0):
            vc : wavelink.Player = inter.guild.voice_client
        
        try:vc
        except:
            if func.isKo(inter):
                await inter.followup.send(embed = Embed(title = "이미 생성된 플레이어가 있어요!" , description = f"자신의서버에서 음악을 듣고싶나요? [여기]({func.ADD})를 클릭하여 초대해보세요!" , color = func.PERPLE) , ephemeral=True)
            else:
                await inter.followup.send(embed = Embed(title = "There are already created players!" , description = f"Do you want to listen to music from your own server? Click [here] ({func.ADD}) to invite them!" , color = func.PERPLE) , ephemeral=True)
            return


    array = await wavelink.YouTubeTrack.search(query = 검색 , return_first = False)
    if func.isKo(inter):
        embed = Embed(title = f"재생할곡을 선택해주세요!" , color = func.GRAY)
        await inter.followup.send(embed = embed , view = Comp.ko.MusicPlayer(vc = vc , musicArray = array , q = 검색 , admin = inter.user))
    else:
        embed = Embed(title = f"Please select a song to play!" , color = func.GRAY)
        await inter.followup.send(embed = embed , view = Comp.en.MusicPlayer(vc = vc , musicArray = array , q = 검색 , admin = inter.user))

@음악.on_autocomplete("검색")
async def TagUpdate(inter : Interaction , text : str):
    Text = []
    for t in func.musicSearch(user = inter.user).load():
        if text in t:Text.append(t)
    if Text == []:
        if func.isKo(inter):
            Text = ["추천검색어가 없습니다."]
        else:
            Text = ["There are no suggested search terms."]
    await inter.response.send_autocomplete(Text)
