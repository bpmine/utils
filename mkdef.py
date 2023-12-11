import re

###############################################################
# Exemple of table defined in C:
#
#   const T_IO mapping[]=
#   {
#	{PIOA,PIO_PA0},			///< OUT_DBG1
#	{PIOA,PIO_PA1},			///< OUT_DBG2
#   }
#
# or
#
#   const int mapping[]=
#   {
#       1, ///< OUT1
#       2, ///< OUT2
#   }
#
# Then call the function:
#
# make_defines_from_ctab('myfile.c','mapping')
#
###############################################################

def make_defines_from_ctab(filename,tabName):
    IDLE=0
    SCANNING=1

    pTable=re.compile(r'([0-9a-zA-Z_]+) (.+)\[.*\].*=.*')
    pElm=re.compile(r'(.+),*.*\/\/\/< (.+) *[0-9]*')    

    dicDefines={}
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
                    hard=m.group(1).strip()
                    nme=m.group(2).strip()
                    if nme in dicDefines.keys():
                        raise Exception('ERREUR: %s est en double' % nme)
                    else:
                        dicDefines[nme]=hard
                elif '};' in ln:
                    break;

    if len(dicDefines.keys())==0:
        print('ERREUR: Aucun élément détecté')
        return

    print('_'*40)
    print()
    print('/**%s' % ('*'*59))
    print('* DEBUT CODE AUTOGENERE: NE PAS MODIFIER (Utiliser mkdef.py)')
    print('* @{')
    print('%s*/' % ('*'*60))
    for i,nme in enumerate(dicDefines.keys()):
        print('#define %-30s %-4d    ///< %s' % (nme,i,dicDefines[nme]))
        
    print('/**%s' % ('*'*59))
    print('* @}')
    print('* FIN CODE AUTOGENERE: NE PAS MODIFIER (Utiliser mkdef.py)')
    print('%s*/' % ('*'*60))


make_defines_from_ctab('input.c','nomTableau')
