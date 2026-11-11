import random, subprocess, datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS

OUT=Path("output"); OUT.mkdir(exist_ok=True)
W,H=1080,1920
STORIES=[
("THE LIGHT THAT NEVER MOVED","For 11 nights, a light appeared in the same empty window.","A night guard noticed it in an abandoned building. Every evening at exactly 2:17, the pale light returned. He checked the rooms. There was no electricity, no furniture, and no one inside. On the twelfth night, he watched from across the street. The light appeared again. Then it moved to the window directly behind him.","He never worked another night shift there. What do you think caused the light?"),
("THE MESSAGE FROM TOMORROW","A woman received a text from her own number, dated tomorrow.","The message contained one sentence: Do not take the 8:10 train. She thought it was a prank. The next morning, she nearly boarded that train, but remembered the message and stayed behind. Minutes later, news reports described a serious delay on that route. The sender was never identified.","Would you trust a message from your future self?"),
("THE VILLAGE THAT WENT SILENT","At sunrise, every clock in a small village stopped.","The clocks stopped at 6:04. Phones lost their signal, radios produced static, and even the church bell refused to ring. The rest of the world continued normally. By noon, everything worked again. Nobody could explain why so many unrelated devices had failed at the exact same minute.","Coincidence, or something nobody noticed? You decide."),
("THE DOOR IN THE WALL","Builders found a door where the plans showed a solid wall.","It had an old brass handle and no keyhole. Behind it was a narrow staircase descending into darkness. The manager ordered the team not to enter until the architect arrived. When they returned the next morning, the wall was smooth again. There was no door, no handle, and no trace of a staircase.","If you found that door, would you open it?"),
("THE LAST PHOTOGRAPH","A family photo showed a person nobody remembered inviting.","The picture was taken at a birthday dinner. Everyone recognized the guests, except for a figure standing near the curtains. The face was blurred. They checked other photos from the evening. The figure appeared in every single one, always standing in a different corner of the room.","Who—or what—was standing behind them?"),
("THE SIGNAL UNDER THE OCEAN","A research team detected a repeating sound deep below the sea.","It arrived in groups of three pulses, paused, then repeated. The team compared it with known animal calls, ship noise, and geological activity. Nothing matched perfectly. After several hours, the signal stopped. Weeks later, the same pattern was detected thousands of kilometres away.","Was it natural, mechanical, or something still unknown?")
]
def getfont(size,bold=False):
    p="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p,size)
def make_card(text,path,n):
    im=Image.new("RGB",(W,H),(12,22,42)); d=ImageDraw.Draw(im)
    for y in range(H):
        shade=int(12+18*y/H)
        d.line((0,y,W,y),fill=(shade,shade+8,shade+24))
    d.ellipse((760,-180,1300,360),outline=(90,105,130),width=4)
    d.rounded_rectangle((65,95,1015,185),radius=28,outline=(205,174,120),width=3)
    d.text((95,120),f"UNKNOWN FILES  •  {n}/3",font=getfont(30,True),fill=(230,207,165))
    f=getfont(58 if len(text)<100 else 48,True)
    words=text.split(); lines=[]; line=""
    for word in words:
        test=(line+" "+word).strip()
        if d.textbbox((0,0),test,font=f)[2] < 900: line=test
        else: lines.append(line); line=word
    if line: lines.append(line)
    y=(H-len(lines)*78)//2
    for line in lines:
        box=d.textbbox((0,0),line,font=f); d.text(((W-(box[2]-box[0]))//2,y),line,font=f,fill=(250,248,242))
        y+=78
    d.text((80,1750),"FOLLOW FOR MORE UNEXPLAINED STORIES",font=getfont(26,True),fill=(230,207,165))
    im.save(path)
def main():
    title,hook,body,end=random.choice(STORIES)
    stamp=datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    work=OUT/("work_"+stamp); work.mkdir()
    texts=[title+". "+hook,body,end]
    aud=[]
    for i,t in enumerate(texts,1):
        make_card(t,work/f"card{i}.png",i)
        p=work/f"voice{i}.mp3"; gTTS(t,lang="en").save(str(p)); aud.append(p)
    concat=work/"audio.txt"
    concat.write_text("".join("file '"+str(p.resolve())+"'\\n" for p in aud))
    narration=work/"narration.mp3"
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(concat),"-c","copy",str(narration)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    durations=[]
    for p in aud:
        x=subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",str(p)],text=True)
        durations.append(float(x.strip())+0.4)
    args=["ffmpeg","-y"]
    for i,dur in enumerate(durations,1): args += ["-loop","1","-t",str(dur),"-i",str(work/f"card{i}.png")]
    filters=[]
    for i in range(3): filters.append(f"[{i}:v]scale=1080:1920,setsar=1,fps=24[v{i}]")
    filters.append("[v0][v1][v2]concat=n=3:v=1:a=0[v]")
    out=OUT/f"UNKNOWN_FILES_{stamp}.mp4"
    args += ["-i",str(narration),"-filter_complex",";".join(filters),"-map","[v]","-map","3:a","-shortest","-c:v","libx264","-preset","ultrafast","-pix_fmt","yuv420p","-c:a","aac","-b:a","128k","-movflags","+faststart",str(out)]
    subprocess.run(args,check=True)
    (OUT/f"UNKNOWN_FILES_{stamp}.txt").write_text("\n\n".join(texts))
    print("Created",out)
if __name__=="__main__": main()
