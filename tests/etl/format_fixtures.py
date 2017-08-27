
FORMATS = {}
FMTDICT = {}

FORMATS['V1'] = '''
value $H1S
" "="Missing"
"1"="12 years old or younger"
"2"="13 years old"
"3"="14 years old"
"4"="15 years old"
"5"="16 years old"
"6"="17 years old"
"7"="18 years old or older"
other="** Data Error **";
value $H2S
" "="Missing"
"1"="Female"
"2"="Male"
other="** Data Error **";
'''

FMTDICT['V1'] = {
'$h1s':{
    1: '12 years old or younger',
    2: '13 years old',
    3: '14 years old',
    4: '15 years old',
    5: '16 years old',
    6: '17 years old',
    7: '18 years old or older'},
'$h2s':{
    1: 'Female',
    2: 'Male'}
}


FORMATS['V2'] = '''
     VALUE AD2DEPEV
           .                   =    "Not asked or Missing"
           .D                  =    "DK/NS"
           .R                  =    "REFUSED"
           1                   =    "Yes"
           2                   =    "No"
           7                   =    "Don't know/Not sure"
           9                   =    "Refused"
           ;
     VALUE ADLTCHLD
           .                   =    "Not asked or Missing"
           .D                  =    "DK/NS"
           .R                  =    "REFUSED"
           0                   =    "No selection"
           1                   =    "Adult"
           2                   =    "Child"
           ;
     VALUE ADSLEEP
           .                   =    "Not asked or Missing"
           .D                  =    "DK/NS"
           .R                  =    "REFUSED"
           1       - 14        =    "01-14 days"
           77                  =    "Don't know/Not sure"
           88                  =    "None"
           99                  =    "Refused"
           ;
'''

FMTDICT['V2'] = {
'ad2depev':{
    1: 'Yes',
    2: 'No',
    7: 'Dont know/Not sure',
    9: 'Refused'},
'adltchld':{
    0: 'No selection',
    1: 'Adult',
    2: 'Child'},
'adsleep':{
    77: 'Dont know/Not sure',
    88: 'None',
    99: 'Refused'}
}


FORMATS['V3'] = '''
  VALUE ALCOHOL
                 101-102 = '1-2 TIMES PER WEEK'
                 103-106 = '3-6 TIMES PER WEEK'
                 107     = 'DAILY'
                 201-203 = 'LT ONCE PER WEEK'
                 204-211 = '1-2 TIMES PER WEEK'
                 212-229 = '3-6 TIMES PER WEEK'
                 230     = 'DAILY'
                 777,999 = 'UNK/REF';

  VALUE ASPUNSAF
                 1 = 'YES, NOT STOMACH RELATED'
                 2 = 'YES, STOMACH PROBLEMS'
                 3 = 'NO'
           .,0,7,9 = 'UNK/REF' ;

  VALUE BADHLTX
                 1 = 'NONE'
                 2 = '1 DAY'
               3-5 = '>= 2 DAYS'
         .,0,77,99 = 'UNK/REF' ;

  VALUE BCCHK
                 1 = 'NO CHECK'
                 2 = 'HAD CHECK'
             .,7,9 = 'UNK/REF' ;
'''

FMTDICT['V3'] = {
'alcohol': {
    107: 'DAILY',
    230: 'DAILY',
    777: 'UNK/REF',
    999: 'UNK/REF'},
'aspunsaf':{
    1: 'YES NOT STOMACH RELATED',
    2: 'YES STOMACH PROBLEMS',
    3: 'NO',
    0: 'UNK/REF',
    7: 'UNK/REF',
    9: 'UNK/REF'},
'badhltx':{
    1: 'NONE',
    2: '1 DAY',
    0: 'UNK/REF',
    77: 'UNK/REF',
    99: 'UNK/REF'},
'bcchk':{
    1: 'NO CHECK',
    2: 'HAD CHECK',
    7: 'UNK/REF',
    9: 'UNK/REF'}
}
