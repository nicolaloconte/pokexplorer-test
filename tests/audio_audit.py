"""T10: local audio integrity, duration, bitrate and scene references."""
from pathlib import Path
import json, subprocess, re
root=Path(__file__).resolve().parents[1]
music=(root/'js/music.js').read_text()
files=sorted((root/'assets/audio').glob('*.mp3'))
report=[]
for file in files:
 output=subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration,bit_rate','-of','json',str(file)],text=True)
 info=json.loads(output)['format']
 assert float(info['duration'])>1
 assert file.name in music, f'Unused audio file: {file.name}'
 report.append({'name':file.name,'seconds':round(float(info['duration']),1),'kbps':round(int(info['bit_rate'])/1000),'size_mb':round(file.stat().st_size/1e6,2)})
print(json.dumps({'status':'PASS','tracks':len(report),'total_mb':round(sum(f.stat().st_size for f in files)/1e6,2),'audit':report},ensure_ascii=False,indent=2))
