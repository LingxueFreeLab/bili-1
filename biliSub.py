from file import spfn
from requests import Session
from biliTime import tostr3
import os
def downsub(r:Session,fn:str,i:dict,ip:dict,se:dict) :
    "下载字幕"
    fq=spfn(fn)[0]
    fn="%s_%s.srt"%(fq,i['lan'])
    i['fn']=fn
    if os.path.exists(fn) :
        fg=False
        bs=True
        if 'y' in ip :
            if ip['y'] :
                fg=True
                bs=False
            else :
                bs=False
        while bs:
            inp=input('"%s"文件已存在，是否覆盖？(y/n)'%(fn))
            if len(inp)>0 :
                if inp[0].lower()=='y' :
                    fg=True
                    bs=False
                elif inp[0].lower()=='n' :
                    bs=False
        if fg:
            try :
                os.remove('%s'%(fn))
            except :
                print('删除原有文件失败，跳过下载')
                return 0
    re=r.get(i['url'])
    re.encoding='utf8'
    re=re.json()
    assrt(fn,re['body'])
    return 0
def assrt(fn:str,b:list):
    "保存至srt格式"
    try :
        f=open(fn,'w',encoding="utf8")
    except :
        print('保存"%s"失败！'%(fn))
        return -1
    i=1
    for k in b:
        try :
            f.write('%s\n'%(i))
            f.write('%s --> %s\n'%(tostr3(k['from']),tostr3(k['to'])))
            f.write('%s\n\n'%(k['content']))
        except :
            print('写入到文件"%s"时失败！'%(fn))
            f.close()
            return -1
        i=i+1
    f.close()
    return 0
def ffinputstr(i:list,n:int) ->(str,str):
    "分别解析出ffmpeg输入参数和元数据参数"
    s=""
    r=""
    z=n
    for k in i :
        s=s+' -i "%s"'%(k['fn'])
        r=r+' -metadata:s:%s language="%s" -metadata:s:%s title="%s"'%(z,k['lan'],z,k['land'])
        z=z+1
    for i in range(z) :
        r=r+' -map %s'%(i)
    return s,r

