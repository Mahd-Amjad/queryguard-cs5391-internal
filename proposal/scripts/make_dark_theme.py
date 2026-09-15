# Theme transform: white editorial -> ink editorial (SM53, Sep 3)
# Usage: edit SRC/DST at the top, then python3 make_dark_theme.py
# Requires: the source deck uses the white editorial palette (see DECK_REBUILD_RECORD.md
# Sep 3 addenda). Context-aware: spPr fills vs rPr text colors are mapped by separate
# tables; red E74C3C passes through unchanged; white text stays white only on dark fills.
# Close any officecli resident on the file BEFORE running (write-trap, see OFFICECLI SSOT).
import zipfile, re, os, shutil

SRC = 'PROPOSAL_DECK_EDITORIAL.pptx'
DST = 'PROPOSAL_DECK_EDITORIAL_DARK.pptx'
shutil.copy(SRC, DST)

FILL = {
    'FFFFFF': '121418',
    '2C3E50': '39485C',
    'F7F9FA': '1B2027', 'ECF0F2': '232A32', 'E4E9EC': '2A313A',
    'F5F6F7': '1B2027', 'F0F2F4': '20262E', 'EAF2F8': '1D2733',
    '85929E': '7A8794',
    'BDC3C7': '5A6B7A',
}
TXT = {
    '2C3E50': 'F2F0E8',
    '5D6D7E': 'A8B2BB',
    'C0392B': 'E74C3C',
    '34495E': '9FB3C8',
}
DARKFILL_OK = {'E74C3C', '39485C', '2C3E50'}
FONTS = {}

ATTR = re.compile(r'srgbClr val="([0-9A-Fa-f]{6})"')
P_TAG = re.compile(r'<a:p[ >]')

def attr_sub(s, table, white_rule=None):
    out, pos = [], 0
    for m in ATTR.finditer(s):
        c = m.group(1).upper()
        if c == 'E74C3C':
            continue
        if white_rule is not None and c == 'FFFFFF':
            new = 'FFFFFF' if white_rule() in DARKFILL_OK else 'F2F0E8'
        elif c in table:
            new = table[c]
        else:
            continue
        out.append(s[pos:m.start()]); out.append(f'srgbClr val="{new}"'); pos = m.end()
    out.append(s[pos:]); return ''.join(out)

def convert_shape(block):
    pm = P_TAG.search(block)
    if not pm:
        return attr_sub(block, FILL)
    head, body = block[:pm.start()], block[pm.start():]
    ls = head.find('<a:lstStyle')
    if ls >= 0:
        head = attr_sub(head[:ls], FILL) + attr_sub(head[ls:], TXT)
    else:
        head = attr_sub(head, FILL)
    fm = re.search(r'<a:solidFill><a:srgbClr val="([0-9A-F]{6})"', head)
    new_fill = fm.group(1) if fm else '121418'
    return head + attr_sub(body, TXT, white_rule=(lambda: new_fill))

zin = zipfile.ZipFile(SRC); zout = zipfile.ZipFile(DST, 'w', zipfile.ZIP_DEFLATED)
n_sp = 0
for it in zin.infolist():
    data = zin.read(it.filename)
    if re.match(r'ppt/slides/slide\d+\.xml$', it.filename):
        s = data.decode('utf8')
        s = re.sub(r'(<p:bg>.*?srgbClr val=")FFFFFF(")', r'\g<1>121418\g<2>', s, flags=re.S)
        out, pos = [], 0
        for m in re.finditer(r'<p:sp>.*?</p:sp>', s, flags=re.S):
            out.append(s[pos:m.start()]); out.append(convert_shape(m.group(0))); pos = m.end(); n_sp += 1
        out.append(s[pos:]); s = ''.join(out)
        data = s.encode('utf8')
    elif re.match(r'ppt/slides/charts/chart\d+\.xml$', it.filename):
        s = data.decode('utf8')
        for old, new in {'2C3E50': '8FA3B5', '85929E': '7A8794', 'BDC3C7': '5A6B7A'}.items():
            s = s.replace(f'srgbClr val="{old}"', f'srgbClr val="{new}"')
        data = s.encode('utf8')
    zout.writestr(it, data)
zin.close(); zout.close()
print(f'dark variant written: {n_sp} shapes')
