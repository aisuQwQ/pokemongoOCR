from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

import shutil
import ocr
import writecsv

class EventHandler(FileSystemEventHandler):
    def on_any_event(self,e):
        time.sleep(1)
        if e.event_type == "created":
            path=e.src_path
            name=path.split('./')[1]
            if name.split('.')[1] not in ['jpg', 'png']:
                return

            unixsec=str(int(time.time()))
            data=ocr.readImg(path)
            data['id']=unixsec
            if(writecsv.writecsv(data)):
                newname=name.split('.')[0]+'-'+unixsec+'.'+name.split('.')[1]
                shutil.move(path, f'./used/{newname}')

            

observer=Observer()
observer.schedule(EventHandler(), path='./')
observer.start()

while True:
    time.sleep(1)