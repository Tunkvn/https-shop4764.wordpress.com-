import sys, subprocess
from docx import Document
from docx.shared import Pt, Cm
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
src=sys.argv[1]; f=src[:-3]+'.docx'
subprocess.run(['pandoc',src,'-f','gfm','-o',f],check=True)
d=Document(f)
for sec in d.sections:
    sec.left_margin=sec.right_margin=Cm(1.8); sec.top_margin=sec.bottom_margin=Cm(1.8)
for t in d.tables:
    b=OxmlElement('w:tblBorders')
    for e in ('top','left','bottom','right','insideH','insideV'):
        x=OxmlElement(f'w:{e}'); x.set(qn('w:val'),'single'); x.set(qn('w:sz'),'4'); x.set(qn('w:color'),'808080'); b.append(x)
    t._tbl.tblPr.append(b)
    for i,r in enumerate(t.rows):
        for c in r.cells:
            if i==0:
                sh=OxmlElement('w:shd'); sh.set(qn('w:val'),'clear'); sh.set(qn('w:fill'),'DCE6F1'); c._tc.get_or_add_tcPr().append(sh)
            for para in c.paragraphs:
                for run in para.runs: run.font.size=Pt(10)
d.save(f); print(f,len(d.tables),'tables')
