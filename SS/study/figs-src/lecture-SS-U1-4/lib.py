import re, math
INK='#263238'; MUT='#607d8b'; BLUE='#1565c0'; GREEN='#2e7d32'; RED='#c62828'
ORG='#ef6c00'; PUR='#6a1b9a'; STEEL='#eceff1'; EDGE='#455a64'; TEAL='#00838f'
LBLUE='#e3f2fd'; LORG='#fff3e0'; LRED='#ffebee'; LGRN='#e8f5e9'; LPUR='#f3e5f5'
SERIF='"Times New Roman",Times,serif'

def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def rich(s, size):
    """markup: _{..} subscript, ^{..} superscript, ~{..} italic serif variable."""
    out=[]; i=0; shift=0.0
    def span(txt, dy=0, extra=''):
        d=f' dy="{dy:.1f}"' if dy else ''
        return f'<tspan{d}{extra}>{esc(txt)}</tspan>'
    pat=re.compile(r'(_\{|\^\{|~\{)')
    while i < len(s):
        m=pat.search(s,i)
        if not m:
            out.append(span(s[i:], -shift)); shift=0; break
        if m.start()>i:
            out.append(span(s[i:m.start()], -shift)); shift=0
        j=s.index('}',m.end()); inner=s[m.end():j]
        kind=m.group(1)[0]
        if kind=='_':
            dy=0.32*size-shift; out.append(span(inner, dy, f' font-size="{0.72*size:.1f}"')); shift=0.32*size
        elif kind=='^':
            dy=-0.38*size-shift; out.append(span(inner, dy, f' font-size="{0.72*size:.1f}"')); shift=-0.38*size
        elif '\u0304' in inner:
            base=inner
            out.append(span(base, -shift, f' font-family={SERIF!r} font-size="{1.12*size:.1f}"'.replace("'",'"'))); shift=0
        else:
            out.append(span(inner, -shift, f' font-family={SERIF!r} font-style="italic" font-size="{1.12*size:.1f}"'.replace("'",'"'))); shift=0
        i=j+1
    if shift: out.append(f'<tspan dy="{-shift:.1f}"></tspan>')
    return ''.join(out)

def T(x,y,s,size=13,fill=INK,anchor='start',weight=None,extra=''):
    w=f' font-weight="{weight}"' if weight else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"{w}{extra}>{rich(s,size)}</text>'

def L(x1,y1,x2,y2,c=EDGE,w=1.5,dash=None,marker=None,extra=''):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    m=''
    if marker:
        for k,v in marker.items(): m+=f' marker-{k}="url(#{v})"'
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}{m}{extra}/>'

def R(x,y,w,h,fill='none',c=EDGE,sw=1.5,rx=0,dash=None,extra=''):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{c}" stroke-width="{sw}"{d}{extra}/>'

def C(x,y,r,fill='#fff',c=EDGE,sw=1.5,extra=''):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" stroke="{c}" stroke-width="{sw}"{extra}/>'

def P(pts,fill='none',c=EDGE,sw=1.5,close=True,dash=None,extra=''):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    tag='polygon' if close else 'polyline'
    s=' '.join(f'{x:.1f},{y:.1f}' for x,y in pts)
    return f'<{tag} points="{s}" fill="{fill}" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"{d}{extra}/>'

def path(d,fill='none',c=EDGE,sw=1.5,dash=None,marker=None,extra=''):
    dd=f' stroke-dasharray="{dash}"' if dash else ''
    m=''
    if marker:
        for k,v in marker.items(): m+=f' marker-{k}="url(#{v})"'
    return f'<path d="{d}" fill="{fill}" stroke="{c}" stroke-width="{sw}"{dd}{m} stroke-linejoin="round"{extra}/>'

def markers(pfx, colors):
    out=['<defs>']
    for name,c in colors.items():
        out.append(f'<marker id="{pfx}-{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')
    out.append('</defs>')
    return ''.join(out)

def arrow(x1,y1,x2,y2,c,w,pfx,name):
    return L(x1,y1,x2,y2,c,w,marker={'end':f'{pfx}-{name}'})

def num(x,y,n,c,r=10):
    return C(x,y,r,c,c,1)+T(x,y+4.5,str(n),12.5,'#fff','middle','700')

def dimh(x1,x2,y,label,c=MUT,size=12,ty=None,pfx=None):
    s=L(x1,y,x2,y,c,1)+L(x1,y-5,x1,y+5,c,1)+L(x2,y-5,x2,y+5,c,1)
    s+=T((x1+x2)/2, (y-5 if ty is None else ty), label, size, c, 'middle')
    return s

def dimv(x,y1,y2,label,c=MUT,size=12,side='left'):
    s=L(x,y1,x,y2,c,1)+L(x-5,y1,x+5,y1,c,1)+L(x-5,y2,x+5,y2,c,1)
    if side=='left': s+=T(x-7,(y1+y2)/2+4,label,size,c,'end')
    else: s+=T(x+7,(y1+y2)/2+4,label,size,c,'start')
    return s

def svg(w,h,body,label):
    return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(label)}" font-family="inherit">{body}</svg>'
