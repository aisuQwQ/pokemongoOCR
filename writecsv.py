import os
from rapidfuzz.process import extractOne

nametable={}
#日付とプレイヤー名の対応表
with open('config.txt', encoding='utf-8') as f:
    lines=f.read().splitlines()
    for line in lines:
        if(line.startswith('#')):
            continue
        nametable[line.split(':')[0]]=line.split(':')[1]

#登録済み？プレイヤー名：None
def getPlayername(date):
    keys=[x for x in nametable.keys()]
    exactdate,score,index=extractOne(date, keys)
    if(score < 80):
        return None
    return nametable[exactdate]

def makeNewcsv(filename):
    with open(filename, mode='w', encoding='shift-jis') as f:
            f.write("日付,時刻,XP,歩いた距離,つかまえたポケモン,訪れたポケストップ,トータルXP,ファイルid\n")


def writecsv(data):
    playername=getPlayername(data['始めた日'])
    if(playername is None):
        print("CSV:ERROR 未登録のプレイヤー")
        return False
    filename=f'{playername}.csv'
    if(os.path.isfile(filename)==False):
        makeNewcsv(filename)
    with open(filename, mode='a', encoding='shift-jis') as f:
        s=''
        s+=f'{data["日付"]},'
        s+=f'{data["時刻"]},'
        s+=f'"{data["XP"]}",'
        s+=f'"{data["歩いた距離"]}",'
        s+=f'"{data["つかまえたポケモン"]}",'
        s+=f'"{data["訪れたポケストップ"]}",'
        s+=f'"{data["トータルXP"]}",'
        s+=f'"{data["id"]}"\n'
        f.write(s)
    return True

