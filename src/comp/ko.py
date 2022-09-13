from nextcord import *
import nextwave as wavelink
from func import emojis
import func

class MusicModal(ui.Modal):
    def __init__(self , vc : wavelink.Player):
        super().__init__("음악 변경!")
        self.music = ui.TextInput(label = "변경할 곡을 입력하세요" , placeholder = "여기에 입력해주세요!")
        self.vc = vc
        self.add_item(self.music)
        

    async def callback(self, inter : Interaction):
        await inter.message.edit(embed = Embed(title = "변경중..." , color = func.GRAY) , view = MusicPlayer(vc = self.vc , musicArray = array , q = self.music.value))
        array = await wavelink.YouTubeTrack.search(query = self.music.value , return_first = False)
        embed = Embed(title = f"여기서 음악을 선택해주세요" , color = func.GRAY)
        await inter.message.edit(embed = embed , view = MusicPlayer(vc = self.vc , musicArray = array , q = self.music.value))

class MusicPlayer(ui.View):
    def __init__(self , vc : wavelink.Player , musicArray : list , q : str , admin : Member = None):
        super().__init__(timeout = 60*60)
        self.add_item(MusicSelect(vc = vc , musicArray = musicArray , q = q , admin = admin))
        # self.add_item(MusicButton(select = select))

        self.vc = vc
        self.admin = admin
    @ui.button(style = ButtonStyle.green , emoji = emojis.musicVloumeD())
    async def down(self , button : ui.Button , inter : Interaction):
        if self.admin == inter.user or self.admin == None:
            if self.vc.volume == 0:return await inter.response.send_message("볼륨이 0입니다" , ephemeral = True)
            await self.vc.set_volume(self.vc.volume-10)

            try:
                embed = Embed(title = inter.message.embeds[0].title , description = f"볼륨 : {self.vc.volume}" , color = inter.message.embeds[0].color)
                embed.set_image(url = str(inter.message.embeds[0].image.url))
                embed.url = inter.message.embeds[0].url
                await inter.message.edit(embed = embed)
            except:
                embed = Embed(title = inter.message.embeds[0].title , description = f"볼륨 : {self.vc.volume}" , color = inter.message.embeds[0].color)
                await inter.message.edit(embed = embed)
        else:
            await inter.response.send_message(embed = Embed(title = "자신의것을 사용해주세요!" , description = f"혹시 자신의 서버에 봇을 초대하고 싶으신가요? [여기]({func.ADD})를 클릭하여 초대해보세요!" , color = 0xeeeeee) , ephemeral = True)

    @ui.button(style = ButtonStyle.red , emoji = emojis.musicStop())
    async def stop(self , button : ui.Button , inter : Interaction):
        if self.admin == inter.user or self.admin == None:
            self.vc.loop = False
            try:await inter.user.voice.channel.connect(cls = wavelink.Player)
            except:pass
            await self.vc.stop()
            
            embed = Embed(title = f"재생할곡을 선택해주세요!" , color = func.GRAY)
            await inter.message.edit(embed = embed) 
        else:
            await inter.response.send_message(embed = Embed(title = "자신의것을 사용해주세요!" , description = f"혹시 자신의 서버에 봇을 초대하고 싶으신가요? [여기]({func.ADD})를 클릭하여 초대해보세요!" , color = 0xeeeeee) , ephemeral = True)

    @ui.button(style = ButtonStyle.gray , emoji = emojis.search())
    async def change(self , button : ui.Button , inter : Interaction):
        if self.admin == inter.user or self.admin == None:

            for item in self.children:
                item.disabled = True
            
            await inter.response.send_modal(MusicModal(vc = self.vc))
        else:
            await inter.response.send_message(embed = Embed(title = "자신의것을 사용해주세요!" , description = f"혹시 자신의 서버에 봇을 초대하고 싶으신가요? [여기]({func.ADD})를 클릭하여 초대해보세요!" , color = 0xeeeeee) , ephemeral = True)
    
    @ui.button(style = ButtonStyle.red , emoji = emojis.musicDisabled())
    async def kill(self , button : ui.Button , inter : Interaction):
        if self.admin == inter.user or self.admin == None:
            try:await inter.user.voice.channel.connect(cls = wavelink.Player)
            except:pass

            for item in self.children:
                item.disabled = True

            self.vc.loop = False
            await self.vc.stop()
            await self.vc.disconnect()
            
            embed = Embed(title = f"음악재생을 마칩니다." , color = func.GRAY)
            # embed.set_image(url = MUSIC)

            await inter.message.edit(embed = embed , view = self)
        else:
            await inter.response.send_message(embed = Embed(title = "자신의것을 사용해주세요!" , description = f"혹시 자신의 서버에 봇을 초대하고 싶으신가요? [여기]({func.ADD})를 클릭하여 초대해보세요!" , color = 0xeeeeee) , ephemeral = True)
   

    @ui.button(style = ButtonStyle.green , emoji = emojis.musicVloumeU())
    async def up(self , button : ui.Button , inter : Interaction):
        if self.admin == inter.user or self.admin == None:
            await self.vc.set_volume(self.vc.volume+10)
            try:
                embed = Embed(title = inter.message.embeds[0].title , description = f"볼륨 : {self.vc.volume}" , color = inter.message.embeds[0].color)
                embed.set_image(url = str(inter.message.embeds[0].image.url))
                embed.url = inter.message.embeds[0].url
                await inter.message.edit(embed = embed)
            except:
                embed = Embed(title = inter.message.embeds[0].title , description = f"볼륨 : {self.vc.volume}" , color = inter.message.embeds[0].color)
                await inter.message.edit(embed = embed)
        else:
            await inter.response.send_message(embed = Embed(title = "자신의것을 사용해주세요!" , description = f"혹시 자신의 서버에 봇을 초대하고 싶으신가요? [여기]({func.ADD})를 클릭하여 초대해보세요!" , color = 0xeeeeee) , ephemeral = True)
