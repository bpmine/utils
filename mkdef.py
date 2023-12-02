import re

def make_defines_from_ctab(filename,tabName):
    IDLE=0
    SCANNING=1

    pTable=re.compile(r'([0-9a-zA-Z_]+) (.+)\[.*\].*=.*{')
    pElm=re.compile(r'.+,*.*///< (.+)')    

    lstDefines=[]
    with open(filename) as fp:
        state=IDLE
        for ln in fp.readlines():
            ln=ln.strip()
            if state==IDLE:
                m=pTable.match(ln)
                if m!=None:
                    state=SCANNING
            elif state==SCANNING:
                m=pElm.match(ln)
                if m!=None:
                    nme=m.group(1).strip()
                    if nme in lstDefines:
                        raise Exception('ERREUR: %s est en double' % nme)
                    else:
                        lstDefines.append(nme)
                elif '};' in ln:
                    break;

    if len(lstDefines)==0:
        print('ERREUR: Aucun élément détecté')
        return

    print('_'*40)
    print()
    print('/**%s' % ('*'*59))
    print('* DEBUT CODE AUTOGENERE: NE PAS MODIFIER (Utiliser mkdef.py)')
    print('* @{')
    print('%s*/' % ('*'*60))
    for i,nme in enumerate(lstDefines):
        print('#define %-30s %d' % (nme,i))
        
    print('/**%s' % ('*'*59))
    print('* @}')
    print('* FIN CODE AUTOGENERE: NE PAS MODIFIER (Utiliser mkdef.py)')
    print('%s*/' % ('*'*60))


make_defines_from_ctab('input.c','nomTableau')
