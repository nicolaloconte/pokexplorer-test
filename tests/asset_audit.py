"""Local asset integrity and explicit references, no third-party packages."""
from pathlib import Path
from xml.etree import ElementTree as ET
import re, subprocess, shutil, sys
root=Path(__file__).resolve().parents[1]
assets=root/'assets'
problems=[];checked=0
for file in assets.rglob('*'):
    if not file.is_file():continue
    checked+=1
    data=file.read_bytes()
    suffix=file.suffix.lower()
    if suffix=='.png' and data[:8]!=b'\x89PNG\r\n\x1a\n':problems.append(f'PNG non valido: {file}')
    if suffix=='.webp' and not (data[:4]==b'RIFF' and data[8:12]==b'WEBP'):problems.append(f'WebP non valido: {file}')
    if suffix in ('.jpeg','.jpg') and not data.startswith(b'\xff\xd8'):problems.append(f'JPEG non valido: {file}')
    if suffix=='.svg':
        try: ET.fromstring(data)
        except ET.ParseError:problems.append(f'SVG non valido: {file}')
    if suffix=='.mp3' and not (data.startswith(b'ID3') or (data[:1]==b'\xff')):
        problems.append(f'MP3 non valido: {file}')
if shutil.which('ffprobe'):
    for file in (assets/'audio').glob('*.mp3'):
        output=subprocess.run(['ffprobe','-v','error','-show_entries','stream=codec_name','-of','default=noprint_wrappers=1:nokey=1',str(file)],capture_output=True,text=True)
        if output.returncode or 'mp3' not in output.stdout:problems.append(f'MP3 non decodificabile: {file}')
for file in [root/'index.html',root/'style.css',*sorted((root/'js').glob('*.js'))]:
    content=file.read_text()
    # Literal local references only; ignores calculated template strings.
    for raw in re.findall(r'''assets/[a-zA-Z0-9_./-]+''',content):
        rel=raw.rstrip('/.')
        if '${' in rel:continue
        # Runtime-generated folder templates can be composed over multiple strings.
        if rel.startswith(('assets/${','assets/characters/npc-')):continue
        if (assets/rel.removeprefix('assets/')).exists():continue
        if re.search(r'\.(svg|png|webp|jpg|jpeg|mp3)$',rel,re.I):problems.append(f'Riferimento mancante in {file.name}: {rel}')
print(f'ASSET AUDIT: {checked} file, {len(problems)} anomalie')
for item in problems:print('  -',item)
sys.exit(1 if problems else 0)
