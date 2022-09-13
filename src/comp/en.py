from nextcord import *
import nextwave as wavelink
from func import emojis
import func

class MusicSelect(ui.Select):
    def __init__(self , vc : wavelink.Player ,  musicArray : list , q , admin : Member = None):
        option = []
        i = 0
        for music in musicArray:
            option.append(SelectOption(label = music.title , value = str(i)))
            i += 1
        super().__init__(placeholder = "Choose your music here!" , options = option)
        vc.loop = True
        self.vc = vc
        self.q = q
        self.musicArray = musicArray
        self.admin = admin

    async def callback(self , inter : Interaction):
        if self.admin == inter.user or self.admin == None:
            await inter.response.defer()
            try:await inter.user.voice.channel.connect(cls = wavelink.Player)
            except:pass
            MUSIC : wavelink.Track = self.musicArray[int(self.values[0])]
            self.play = await self.vc.play(MUSIC)
            if self.vc.volume == 100:
                await self.vc.set_volume(50)
            embed = Embed(title = f"{MUSIC}{emojis.music()}" , description = f"volume : {self.vc.volume}" , color = func.GRAY)
            await inter.message.edit(embed = embed)
            print(MUSIC.uri)
            img = f"https://img.youtube.com/vi/{MUSIC.identifier}/mqdefault.jpg"
            url = MUSIC.uri
            embed.set_image(url = img)
            embed.url = url
            await inter.message.edit(embed = embed)
        else:
            await inter.response.send_message(embed = Embed(title = "Please use your own!" , description = f"Have you ever wanted to invite a bot to your server? Click [here] ({func.ADD}) to invite!" , color = 0xeeeeee) , ephemeral = True)

class MusicModal(ui.Modal):
    def __init__(self , vc : wavelink.Player):
        super().__init__("Change the music!")
        self.music = ui.TextInput(label = "Enter the song you want to change" , placeholder = "enter here!")
        self.vc = vc
        self.add_item(self.music)
        

    async def callback(self, inter : Interaction):
        await inter.message.edit(embed = Embed(title = "Changing..." , color = func.GRAY) , view = MusicPlayer(vc = self.vc , musicArray = array , q = self.music.value))
        array = await wavelink.YouTubeTrack.search(query = self.music.value , return_first = False)
        embed = Embed(title = f"select music here" , color = func.GRAY)
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
            if self.vc.volume == 0:return await inter.response.send_message("volume is 0" , ephemeral = True)
            await self.vc.set_volume(self.vc.volume-10)

            try:
                embed = Embed(title = inter.message.embeds[0].title , description = f"volume : {self.vc.volume}" , color = inter.message.embeds[0].color)
                embed.set_image(url = str(inter.message.embeds[0].image.url))
                embed.url = inter.message.embeds[0].url
                await inter.message.edit(embed = embed)
            except:
                embed = Embed(title = inter.message.embeds[0].title , description = f"volume : {self.vc.volume}" , color = inter.message.embeds[0].color)
                await inter.message.edit(embed = embed)
        else:
            await inter.response.send_message(embed = Embed(title = "Please use your own!" , description = f"Have you ever wanted to invite a bot to your server? Click [here] ({func.ADD}) to invite!" , color = 0xeeeeee) , ephemeral = True)

    @ui.button(style = ButtonStyle.red , emoji = emojis.musicStop())
    async def stop(self , button : ui.Button , inter : Interaction):
        if self.admin == inter.user or self.admin == None:
            self.vc.loop = False
            try:await inter.user.voice.channel.connect(cls = wavelink.Player)
            except:pass
            await self.vc.stop()
            
            embed = Embed(title = f"Please select a song to play!" , color = func.GRAY)
            await inter.message.edit(embed = embed) 
        else:
            await inter.response.send_message(embed = Embed(title = "Please use your own!" , description = f"Have you ever wanted to invite a bot to your server? Click [here] ({func.ADD}) to invite!" , color = 0xeeeeee) , ephemeral = True)

    @ui.button(style = ButtonStyle.gray , emoji = emojis.search())
    async def change(self , button : ui.Button , inter : Interaction):
        if self.admin == inter.user or self.admin == None:

            for item in self.children:
                item.disabled = True
            
            await inter.response.send_modal(MusicModal(vc = self.vc))
        else:
            await inter.response.send_message(embed = Embed(title = "Please use your own!" , description = f"Have you ever wanted to invite a bot to your server? Click [here] ({func.ADD}) to invite!" , color = 0xeeeeee) , ephemeral = True)
    
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
            
            embed = Embed(title = f"finish playing music" , color = func.GRAY)
            # embed.set_image(url = MUSIC)

            await inter.message.edit(embed = embed , view = self)
        else:
            await inter.response.send_message(embed = Embed(title = "Please use your own!" , description = f"Have you ever wanted to invite a bot to your server? Click [here] ({func.ADD}) to invite!" , color = 0xeeeeee) , ephemeral = True)
   

    @ui.button(style = ButtonStyle.green , emoji = emojis.musicVloumeU())
    async def up(self , button : ui.Button , inter : Interaction):
        if self.admin == inter.user or self.admin == None:
            await self.vc.set_volume(self.vc.volume+10)
            try:
                embed = Embed(title = inter.message.embeds[0].title , description = f"volume : {self.vc.volume}" , color = inter.message.embeds[0].color)
                embed.set_image(url = str(inter.message.embeds[0].image.url))
                embed.url = inter.message.embeds[0].url
                await inter.message.edit(embed = embed)
            except:
                embed = Embed(title = inter.message.embeds[0].title , description = f"volume : {self.vc.volume}" , color = inter.message.embeds[0].color)
                await inter.message.edit(embed = embed)
        else:
            await inter.response.send_message(embed = Embed(title = "Please use your own!" , description = f"Have you ever wanted to invite a bot to your server? Click [here] ({func.ADD}) to invite!" , color = 0xeeeeee) , ephemeral = True)
