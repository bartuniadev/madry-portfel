from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule

OUT='/home/user/madry-portfel/pliki/budzet-domowy-madry-portfel.xlsx'
F='Arial'
PLN='#,##0 "zł";-#,##0 "zł";"-"'
PCT='0.0%;-0.0%;"-"'
YELLOW=PatternFill('solid', start_color='FFF4C2')
GREEN=PatternFill('solid', start_color='1F7A4D')
LIGHT=PatternFill('solid', start_color='EEF7F0')
GREY=PatternFill('solid', start_color='F4F2EA')
thin=Side(style='thin', color='D9D5CA')
BOX=Border(left=thin,right=thin,top=thin,bottom=thin)
def f(bold=False,size=10,color='1F2A24',italic=False): return Font(name=F,bold=bold,size=size,color=color,italic=italic)
INPUT_FONT=f(color='0000FF')

wb=Workbook()

# ---------- Instrukcja ----------
ws=wb.active; ws.title='Instrukcja'
ws.column_dimensions['A'].width=3; ws.column_dimensions['B'].width=95
rows=[
 ('Budżet domowy 50/30/20 — Mądry Portfel', f(True,16,'145C39')),
 ('Darmowy arkusz do planowania miesięcznego budżetu. Działa w Excelu, Arkuszach Google i LibreOffice.', f(size=11)),
 ('',None),
 ('Jak korzystać', f(True,12,'145C39')),
 ('1. Wypełniaj tylko żółte komórki z niebieskim tekstem — reszta liczy się sama.', f(size=11)),
 ('2. Arkusz „Budżet miesiąca”: wpisz dochody netto, a przy każdym wydatku plan i faktyczną kwotę oraz typ (Potrzeby, Zachcianki, Oszczędności).', f(size=11)),
 ('3. Podsumowanie pokaże, jaki procent dochodu idzie na każdy typ, w porównaniu z celem 50/30/20 (cele możesz zmienić).', f(size=11)),
 ('4. Arkusz „Rok”: przepisuj sumy z każdego miesiąca, żeby widzieć trend i stopę oszczędności.', f(size=11)),
 ('5. Arkusz „Cele”: wpisz cel, kwotę, ile już masz i ile miesięcy zostało — zobaczysz, ile odkładać co miesiąc.', f(size=11)),
 ('',None),
 ('Wpisane kwoty są przykładowe — zastąp je swoimi. Dodawaj lub usuwaj wiersze wydatków w środku tabeli, a sumy się dopasują.', f(italic=True,size=10,color='5B6A62')),
 ('',None),
 ('Więcej o metodzie: https://bartuniadev.github.io/madry-portfel/artykuly/budzet-50-30-20.html', f(size=10,color='1F7A4D')),
 ('Kalkulator online: https://bartuniadev.github.io/madry-portfel/narzedzia/kalkulator-budzetu.html', f(size=10,color='1F7A4D')),
 ('',None),
 ('Arkusz ma charakter edukacyjny. Możesz go dowolnie kopiować i udostępniać.', f(italic=True,size=9,color='5B6A62')),
]
for i,(txt,font) in enumerate(rows, start=2):
    c=ws.cell(row=i,column=2,value=txt or None)
    if font: c.font=font
    c.alignment=Alignment(wrap_text=True,vertical='top')
ws.row_dimensions[2].height=26

# ---------- Budżet miesiąca ----------
m=wb.create_sheet('Budżet miesiąca')
for col,w in zip('ABCDEF',[34,16,16,16,16,4]): m.column_dimensions[col].width=w
m['A1']='Budżet miesiąca'; m['A1'].font=f(True,16,'145C39')
m['A2']='Miesiąc:'; m['A2'].font=f(True)
m['B2']='listopad 2026'; m['B2'].font=INPUT_FONT; m['B2'].fill=YELLOW
# income
m['A4']='DOCHODY (netto)'; m['A4'].font=f(True,11,'FFFFFF'); m['A4'].fill=GREEN
m['B4']='Kwota'; m['B4'].font=f(True,11,'FFFFFF'); m['B4'].fill=GREEN
inc=[('Wynagrodzenie netto',5500),('Dodatkowe zlecenia',400),('Inne dochody',0)]
for i,(name,val) in enumerate(inc, start=5):
    m.cell(row=i,column=1,value=name).font=f()
    c=m.cell(row=i,column=2,value=val); c.font=INPUT_FONT; c.fill=YELLOW; c.number_format=PLN
m['A8']='Dochody razem'; m['A8'].font=f(True)
m['B8']='=SUM(B5:B7)'; m['B8'].font=f(True); m['B8'].number_format=PLN; m['B8'].fill=LIGHT
# expenses
hdr=['WYDATKI','Typ','Plan','Faktycznie','Różnica (plan − fakt)']
for j,h in enumerate(hdr, start=1):
    c=m.cell(row=10,column=j,value=h); c.font=f(True,11,'FFFFFF'); c.fill=GREEN; c.alignment=Alignment(wrap_text=True,vertical='center')
m.row_dimensions[10].height=30
exp=[
 ('Czynsz / najem','Potrzeby',2000,2000),('Media, internet, telefon','Potrzeby',400,430),
 ('Jedzenie i chemia','Potrzeby',1100,1150),('Transport','Potrzeby',200,190),
 ('Zdrowie i leki','Potrzeby',100,60),('Minimalne raty','Potrzeby',0,0),
 ('Jedzenie na mieście','Zachcianki',300,360),('Rozrywka i wyjścia','Zachcianki',300,250),
 ('Ubrania i rzeczy','Zachcianki',250,190),('Subskrypcje','Zachcianki',80,80),
 ('Poduszka finansowa','Oszczędności',600,600),('IKE / IKZE / inwestycje','Oszczędności',300,300),
 ('Cele (wakacje, prezenty)','Oszczędności',270,270),
]
first=11
for i,(name,typ,plan,act) in enumerate(exp, start=first):
    m.cell(row=i,column=1,value=name).font=INPUT_FONT; m.cell(row=i,column=1).fill=YELLOW
    t=m.cell(row=i,column=2,value=typ); t.font=INPUT_FONT; t.fill=YELLOW
    for col,val in ((3,plan),(4,act)):
        c=m.cell(row=i,column=col,value=val); c.font=INPUT_FONT; c.fill=YELLOW; c.number_format=PLN
    d=m.cell(row=i,column=5,value=f'=C{i}-D{i}'); d.font=f(); d.number_format=PLN
last=first+len(exp)-1
tot=last+1
m.cell(row=tot,column=1,value='Wydatki razem').font=f(True)
for col in 'CDE':
    c=m[f'{col}{tot}']; c.value=f'=SUM({col}{first}:{col}{last})'; c.font=f(True); c.number_format=PLN; c.fill=LIGHT
m.cell(row=tot+1,column=1,value='Zostaje z dochodu (dochody − wydatki faktycznie)').font=f(True)
r=m.cell(row=tot+1,column=4,value=f'=B8-D{tot}'); r.font=f(True); r.number_format=PLN; r.fill=LIGHT
dv=DataValidation(type='list', formula1='"Potrzeby,Zachcianki,Oszczędności"', allow_blank=True, showErrorMessage=True,
                  errorTitle='Typ wydatku', error='Wybierz: Potrzeby, Zachcianki albo Oszczędności.')
m.add_data_validation(dv); dv.add(f'B{first}:B{last+20}')
for rr in range(10,tot+2):
    for cc in range(1,6): m.cell(row=rr,column=cc).border=BOX
# summary 50/30/20
s0=tot+4
heads=['PODSUMOWANIE','Cel (% dochodu)','Faktycznie (zł)','Faktycznie (% dochodu)','Różnica vs cel (pp)']
for j,h in enumerate(heads, start=1):
    c=m.cell(row=s0,column=j,value=h); c.font=f(True,11,'FFFFFF'); c.fill=GREEN; c.alignment=Alignment(wrap_text=True,vertical='center')
m.row_dimensions[s0].height=30
targets=[('Potrzeby',0.5),('Zachcianki',0.3),('Oszczędności',0.2)]
for k,(name,tg) in enumerate(targets, start=s0+1):
    m.cell(row=k,column=1,value=name).font=f(True)
    c=m.cell(row=k,column=2,value=tg); c.font=INPUT_FONT; c.fill=YELLOW; c.number_format='0%'
    a=m.cell(row=k,column=3,value=f'=SUMIFS($D${first}:$D${last+20},$B${first}:$B${last+20},A{k})'); a.font=f(); a.number_format=PLN
    p=m.cell(row=k,column=4,value=f'=IFERROR(C{k}/$B$8,0)'); p.font=f(); p.number_format=PCT
    d=m.cell(row=k,column=5,value=f'=D{k}-B{k}'); d.font=f(); d.number_format='+0.0%;-0.0%;"-"'
    for cc in range(1,6): m.cell(row=k,column=cc).border=BOX
chk=s0+4
m.cell(row=chk,column=1,value='Suma celów (powinna wynosić 100%)').font=f(italic=True,color='5B6A62')
c=m.cell(row=chk,column=2,value=f'=SUM(B{s0+1}:B{s0+3})'); c.number_format='0%'; c.font=f(italic=True,color='5B6A62')
m.cell(row=chk+2,column=1,value='Wskazówka: przy wysokim czynszu cel 60/20/20 bywa bardziej realny niż 50/30/20. Kwoty w tabeli są przykładowe.').font=f(italic=True,size=9,color='5B6A62')
m.conditional_formatting.add(f'E{first}:E{last}', CellIsRule(operator='lessThan', formula=['0'], font=Font(name=F,color='B4553F')))
m.conditional_formatting.add(f'D{tot+1}', CellIsRule(operator='lessThan', formula=['0'], font=Font(name=F,bold=True,color='B4553F')))
m.freeze_panes='A11'

# ---------- Rok ----------
y=wb.create_sheet('Rok')
for col,w in zip('ABCDEFG',[16,16,16,16,16,16,18]): y.column_dimensions[col].width=w
y['A1']='Podsumowanie roku'; y['A1'].font=f(True,16,'145C39')
y['A2']='Po każdym miesiącu przepisz sumy z arkusza „Budżet miesiąca” (kolumna „Faktycznie”).'; y['A2'].font=f(italic=True,color='5B6A62')
h=['Miesiąc','Dochody','Potrzeby','Zachcianki','Oszczędności','Zostało','Stopa oszczędności']
for j,t in enumerate(h, start=1):
    c=y.cell(row=4,column=j,value=t); c.font=f(True,11,'FFFFFF'); c.fill=GREEN; c.alignment=Alignment(wrap_text=True,vertical='center')
months=['styczeń','luty','marzec','kwiecień','maj','czerwiec','lipiec','sierpień','wrzesień','październik','listopad','grudzień']
for i,mn in enumerate(months, start=5):
    y.cell(row=i,column=1,value=mn).font=f()
    for col in range(2,6):
        c=y.cell(row=i,column=col); c.font=INPUT_FONT; c.fill=YELLOW; c.number_format=PLN
    if mn=='styczeń':
        for col,val in zip(range(2,6),(5900,3790,880,1170)): y.cell(row=i,column=col,value=val)
    z=y.cell(row=i,column=6,value=f'=IF(B{i}="","",B{i}-C{i}-D{i}-E{i})'); z.font=f(); z.number_format=PLN
    so=y.cell(row=i,column=7,value=f'=IF(OR(B{i}="",B{i}=0),"",(E{i}+F{i})/B{i})'); so.font=f(); so.number_format=PCT
    for cc in range(1,8): y.cell(row=i,column=cc).border=BOX
y['A17']='Razem'; y['A17'].font=f(True)
y['A18']='Średnio / mies.'; y['A18'].font=f(True)
for col in 'BCDEF':
    c=y[f'{col}17']; c.value=f'=SUM({col}5:{col}16)'; c.font=f(True); c.number_format=PLN; c.fill=LIGHT
    a=y[f'{col}18']; a.value=f'=IFERROR(AVERAGE({col}5:{col}16),0)'; a.font=f(True); a.number_format=PLN; a.fill=LIGHT
g=y['G17']; g.value='=IFERROR((E17+F17)/B17,0)'; g.font=f(True); g.number_format=PCT; g.fill=LIGHT
y['A20']='Stopa oszczędności = (oszczędności + to, co zostało) ÷ dochody. Przykładowe kwoty w styczniu — zastąp swoimi.'; y['A20'].font=f(italic=True,size=9,color='5B6A62')
y.freeze_panes='A5'

# ---------- Cele ----------
g=wb.create_sheet('Cele')
for col,w in zip('ABCDEF',[30,16,16,16,18,16]): g.column_dimensions[col].width=w
g['A1']='Cele oszczędnościowe'; g['A1'].font=f(True,16,'145C39')
g['A2']='Każdy cel na osobnym subkoncie, z kwotą i terminem. Przelew ustaw jako stałe zlecenie dzień po wypłacie.'; g['A2'].font=f(italic=True,color='5B6A62')
h=['Cel','Kwota docelowa','Już odłożone','Brakuje','Miesięcy do terminu','Odkładaj miesięcznie']
for j,t in enumerate(h, start=1):
    c=g.cell(row=4,column=j,value=t); c.font=f(True,11,'FFFFFF'); c.fill=GREEN; c.alignment=Alignment(wrap_text=True,vertical='center')
goals=[('Poduszka finansowa',12000,2000,20),('Wakacje',3600,600,8),('Nowy laptop',4500,0,18),('Opłaty roczne (ubezpieczenia, prezenty)',2400,0,12)]
for i in range(5,15):
    vals=goals[i-5] if i-5 < len(goals) else (None,None,None,None)
    for col,val in zip(range(1,4),vals[:3]):
        c=g.cell(row=i,column=col,value=val); c.font=INPUT_FONT; c.fill=YELLOW
        if col>1: c.number_format=PLN
    c=g.cell(row=i,column=5,value=vals[3]); c.font=INPUT_FONT; c.fill=YELLOW; c.number_format='0'
    d=g.cell(row=i,column=4,value=f'=IF(B{i}="","",MAX(B{i}-C{i},0))'); d.font=f(); d.number_format=PLN
    o=g.cell(row=i,column=6,value=f'=IF(OR(B{i}="",E{i}="",E{i}=0),"",D{i}/E{i})'); o.font=f(True); o.number_format=PLN
    for cc in range(1,7): g.cell(row=i,column=cc).border=BOX
g['A16']='Razem miesięcznie na cele'; g['A16'].font=f(True)
t=g['F16']; t.value='=SUM(F5:F14)'; t.font=f(True); t.number_format=PLN; t.fill=LIGHT
g['A18']='Przykładowe cele — zastąp swoimi. Jeśli suma przekracza Twoje możliwości, wydłuż terminy zamiast rezygnować z celów.'; g['A18'].font=f(italic=True,size=9,color='5B6A62')

for wsx in wb.worksheets:
    wsx.sheet_view.showGridLines = False if wsx.title=='Instrukcja' else True
wb.active=1
wb.save(OUT); print('saved',OUT)
