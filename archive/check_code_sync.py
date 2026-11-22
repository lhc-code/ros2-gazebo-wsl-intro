"""practice/*.md의 `<!-- sync: 경로 -->` 바로 아래 코드 블록이 answers/ 파일과 같은지 검사.

사용법: python3 archive/check_code_sync.py   (저장소 루트에서)
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PATTERN = re.compile(r'<!-- sync: (\S+) -->\s*\n```\w*\n(.*?)```', re.S)

failed = 0
checked = 0
for md in sorted((ROOT / 'practice').glob('*.md')):
    for path, block in PATTERN.findall(md.read_text(encoding='utf-8')):
        checked += 1
        target = ROOT / path
        if not target.exists():
            print(f'[실패] {md.name}: {path} 없음')
            failed += 1
        elif target.read_text(encoding='utf-8') != block:
            print(f'[실패] {md.name}: {path} 내용 다름')
            failed += 1
        else:
            print(f'[OK]   {md.name}: {path}')

print(f'{checked}개 검사, {failed}개 불일치')
sys.exit(1 if failed or checked == 0 else 0)
