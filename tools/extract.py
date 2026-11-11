import sys, re, json, html, pathlib
from html.parser import HTMLParser

src = pathlib.Path(sys.argv[1]); out = pathlib.Path(sys.argv[2])
t = src.read_text(encoding='utf-8', errors='ignore')
m = re.search(r'const CHAPTERS_DATA = (\[.*?\]);\s*\n', t, re.S)
data = json.loads(m.group(1))
(out/'chapters.json').write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')

class MD(HTMLParser):
    def __init__(s):
        super().__init__(); s.o=[]; s.stack=[]; s.dv=[]; s.row=[]; s.rows=[]; s.intable=False; s.cell=None
    def w(s,x):
        if s.cell is not None: s.cell.append(x)
        else: s.o.append(x)
    def handle_starttag(s,tag,a):
        a=dict(a); cls=a.get('class','')
        if tag=='table': s.intable=True; s.rows=[]
        elif tag=='tr': s.row=[]
        elif tag in('td','th'): s.cell=[]
        elif tag=='h4': s.w('\n\n#### ')
        elif tag=='ul' or tag=='ol': s.stack.append([tag,0]); s.w('\n')
        elif tag=='li':
            ind='  '*(len(s.stack)-1)
            if s.stack and s.stack[-1][0]=='ol':
                s.stack[-1][1]+=1; s.w(f'\n{ind}{s.stack[-1][1]}. ')
            else: s.w(f'\n{ind}- ')
        elif tag=='br': s.w(' ' if s.cell is not None else '\n')
        elif tag=='p': s.w('\n\n')
        elif tag in('strong','b'): s.w('**')
        elif tag=='em': s.w('*')
        elif tag=='div':
            k='box-title' if 'box-title' in cls else 'q-title' if 'q-title' in cls else 'other'
            s.dv.append(k)
            if k=='box-title': s.w('\n\n> **')
            elif k=='q-title': s.w('\n\n**')
            elif 'q-options' in cls: s.w('\n')
            elif 'q-ans-box' in cls: s.w('\n\n> ')
        elif tag=='span' and 'hl-red' in cls: s.w('⟦紅⟧')
        elif tag=='span' and 'hl-blue' in cls: s.w('⟦藍⟧')
        elif tag=='span' and 'hl-green' in cls: s.w('⟦綠⟧')
    def handle_endtag(s,tag):
        if tag in('td','th'):
            s.row.append(''.join(s.cell).strip().replace('\n',' ').replace('|','／')); s.cell=None
        elif tag=='tr': s.rows.append(s.row)
        elif tag=='table':
            s.intable=False
            if s.rows:
                n=len(s.rows[0]); s.o.append('\n\n| '+' | '.join(s.rows[0])+' |\n|'+'---|'*n)
                for r in s.rows[1:]: s.o.append('\n| '+' | '.join(r)+' |')
                s.o.append('\n')
        elif tag in('ul','ol'): s.stack.pop(); s.w('\n')
        elif tag in('strong','b'): s.w('**')
        elif tag=='em': s.w('*')
        elif tag=='h4': s.w('\n')
        elif tag=='div':
            k=s.dv.pop() if s.dv else 'other'
            if k in('box-title','q-title'): s.w('**\n\n')
    def handle_data(s,d): s.w(re.sub(r'\s+',' ',d) if s.cell is not None else d.replace('\n',' ') if s.stack==[] else d.strip('\n'))
def tomd(h):
    p=MD(); p.feed(h); x=''.join(p.o)
    x=re.sub(r'(\*\*)\s*\n\n(?=>)',r'\1\n\n',x)
    x='\n'.join(l.rstrip() for l in x.split('\n'))
    x=re.sub(r'\n{3,}','\n\n',x); return x.strip()

for c in data:
    n=int(re.search(r'\d+',c['number']).group())
    lines=[f"# {c['number']}｜{c['title']}", '', f"- 標籤：{c['badge']}", f"- 命題趨勢：{c['analysis']}", '']
    for s in c['sections']:
        lines += [f"## {s['sub_title']}", '', tomd(s['content']), '']
    (out/f"ch{n:02d}.md").write_text('\n'.join(lines),encoding='utf-8')
print(len(data),'chapters')
for c in data:
    q=sum(len(re.findall('quiz-item',s['content'])) for s in c['sections'])
    print(c['number'],c['title'][:20],len(c['sections']),'sec',q,'quiz')
