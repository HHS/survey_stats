* 
This SPSS syntax reads ASCII format (text format) 2007 YRBS data and creates a formatted 
and labeled SPSS data file that you can analyze in SPSS;

*
Change the file location specifications from "c:\yrbs2007" to the location where you have 
stored the SPSS syntax and the YRBS ASCII data file before you run this syntax;  
Change the location specification in three places - in the "data list" statement at the top 
of the syntax and in the "save" and "get" statements at the end of the syntax;.

DATA LIST FILE="c:\yrbs2007\yrbs2007.dat"/
Q1 17-17 (A)  
Q2 18-18 (A)  Q3 19-19 (A)  Q4 20-20 (A)  
Q5 21-28 (A) Q6 29-32  Q7 33-38  
Q8 39-39 (A)  Q9 40-40 (A)  Q10 41-41 (A)  
Q11 42-42 (A)  Q12 43-43 (A)  Q13 44-44 (A)  
Q14 45-45 (A)  Q15 46-46 (A)  Q16 47-47 (A)  
Q17 48-48 (A)  Q18 49-49 (A)  Q19 50-50 (A)  
Q20 51-51 (A)  Q21 52-52 (A)  Q22 53-53 (A)  
Q23 54-54 (A)  Q24 55-55 (A)  Q25 56-56 (A)  
Q26 57-57 (A)  Q27 58-58 (A)  Q28 59-59 (A)  
Q29 60-60 (A)  Q30 61-61 (A)  Q31 62-62 (A)  
Q32 63-63 (A)  Q33 64-64 (A)  Q34 65-65 (A)  
Q35 66-66 (A)  Q36 67-67 (A)  Q37 68-68 (A)  
Q38 69-69 (A)  Q39 70-70 (A)  Q40 71-71 (A)  
Q41 72-72 (A)  Q42 73-73 (A)  Q43 74-74 (A)  
Q44 75-75 (A)  Q45 76-76 (A)  Q46 77-77 (A)  
Q47 78-78 (A)  Q48 79-79 (A)  Q49 80-80 (A)  
Q50 81-81 (A)  Q51 82-82 (A)  Q52 83-83 (A)  
Q53 84-84 (A)  Q54 85-85 (A)  Q55 86-86 (A)  
Q56 87-87 (A)  Q57 88-88 (A)  Q58 89-89 (A)  
Q59 90-90 (A)  Q60 91-91 (A)  Q61 92-92 (A)  
Q62 93-93 (A)  Q63 94-94 (A)  Q64 95-95 (A)  
Q65 96-96 (A)  Q66 97-97 (A)  Q67 98-98 (A)  
Q68 99-99 (A)  Q69 100-100 (A)  Q70 101-101 (A)  
Q71 102-102 (A)  Q72 103-103 (A)  Q73 104-104 (A)  
Q74 105-105 (A)  Q75 106-106 (A)  Q76 107-107 (A)  
Q77 108-108 (A)  Q78 109-109 (A)  Q79 110-110 (A)  
Q80 111-111 (A)  Q81 112-112 (A)  Q82 113-113 (A)  
Q83 114-114 (A)  Q84 115-115 (A)  Q85 116-116 (A)  
Q86 117-117 (A)  Q87 118-118 (A)  Q88 119-119 (A)  
Q89 120-120 (A)  Q90 121-121 (A)  Q91 122-122 (A)  
Q92 123-123 (A)  Q93 124-124 (A)  Q94 125-125 (A)  
Q95 126-126 (A)  Q96 127-127 (A)  Q97 128-128 (A)
Q98 129-129 (A)  
QN8 130 -130 QN9 131 -131 QN10 132 -132 
QN11 133 -133 QN12 134 -134 QN13 135 -135
QN14 136 -136 QN15 137 -137 QN16 138 -138
QN17 139 -139 QN18 140 -140 QN19 141 -141
QN20 142 -142 QN21 143 -143 QN22 144 -144
QN23 145 -145 QN24 146 -146 QN25 147 -147
QN26 148 -148 QN27 149 -149 QN28 150 -150
QN29 151 -151 QN30 152 -152 QN31 153 -153
QN32 154 -154 QN33 155 -155 QN34 156 -156
QN35 157 -157 QN36 158 -158 QN37 159 -159
QN38 160 -160 QN39 161 -161 QN40 162 -162
QN41 163 -163 QN42 164 -164 QN43 165 -165
QN44 166 -166 QN45 167 -167 QN46 168 -168
QN47 169 -169 QN48 170 -170 QN49 171 -171
QN50 172 -172 QN51 173 -173 QN52 174 -174
QN53 175 -175 QN54 176 -176 QN55 177 -177
QN56 178 -178 QN57 179 -179 QN58 180 -180
QN59 181 -181 QN60 182 -182 QN61 183 -183
QN62 184 -184 QN63 185 -185 QN64 186 -186
QN65 187 -187 QN66 188 -188 QN67 189 -189
QN68 190 -190 QN69 191 -191 QN70 192 -192
QN71 193 -193 QN72 194 -194 QN73 195 -195
QN74 196 -196 QN75 197 -197 QN76 198 -198
QN77 199 -199 QN78 200 -200 QN79 201 -201
QN80 202 -202 QN81 203 -203 QN82 204 -204
QN83 205 -205 QN84 206 -206 QN85 207 -207
QN86 208 -208 QN87 209 -209 QN88 210 -210
QN89 211 -211 QN90 212 -212 QN91 213 -213
QN92 214 -214 QN93 215 -215 QN94 216 -216
QN95 217 -217 QN96 218 -218 QN97 219 -219
QN98 220 -220 QNFRVG 221 -221 QNFRCIG 222 -222
QNDLYPE 223 -223 QNANYTOB 224 -224
QNROVWGT 225 -225 QNOVWGT 226 -226
site 1-3 (A) 
weight 358-369 psu 370-374 stratum 375-378    
bmipct 379-383 raceeth 384-385 (A).
EXECUTE.
 
VARIABLE LABELS
Q1 "How old are you"
Q2 "What is your sex"
Q3 "In what grade are you"
Q4 "Are you Hispanic/Latino"
Q5 "What is your race"
Q6 "How tall are you"
Q7 "How much do you weigh"
Q8 "How often wear bicycle helmet"
Q9 "How often wore  a seat belt"
Q10 "How often ride w/drinking driver 30 days"
Q11 "How often drive while drinking 30 days"
Q12 "Carried weapon 30 days"
Q13 "Carried gun 30 days"
Q14 "Carried weapon at school  30 days"
Q15 "How many days feel unsafe@school 30 days"
Q16 "How  many times threatened@school 12 mos"
Q17 "Property stolen at school"
Q18 "How many times in fight 12 mos"
Q19 "How many times injured in fight 12 mos"
Q20 "How many times in fight @ school  12 mos"
Q21 "Did  boyfriend/girlfriend hit/slap 12 mo"
Q22 "Have you been forced to have sex"
Q23 "Ever feel sad or hopeless 12 mos"
Q24 "Ever considered suicide 12 mos"
Q25 "Ever make suicide plan 12 mos"
Q26 "Ever attempt suicide 12 mos"
Q27 "Ever injured from suicide attempt 12 mos"
Q28 "Ever smoked"
Q29 "How old when first smoked"
Q30 "How many days smoked 30 days"
Q31 "How many cigarettes/day 30 days"
Q32 "How did you get cigarettes past 30 days"
Q33 "How many days smoke @ school 30 days"
Q34 "Have you ever smoked daily"
Q35 "Tried to quit smoking past 12 months"
Q36 "How many days use snuff past 30 days"
Q37 "Days use snuff school property 30 days"
Q38 "How many days smoke cigars 30 days"
Q39 "How many days drink alcohol"
Q40 "How old when first drank alcohol"
Q41 "How many days drink alcohol 30 days"
Q42 "How many days have 5+ drinks 30 days"
Q43 "How did you get alcohol past 30 days"
Q44 "How many days drink @ school 30 days"
Q45 "How many times smoke marijuana"
Q46 "How old when first tried marijuana"
Q47 "How many times use marijuana 30 days"
Q48 "How many times marijuana@school 30 days"
Q49 "How many times use cocaine"
Q50 "How many times use cocaine 30 days"
Q51 "How many times sniffed glue"
Q52 "How many times used heroin"
Q53 "How many times used methamphetamines"
Q54 "Ecstacy one or more time"
Q55 "How many times used steroids"
Q56 "How many times injected drugs"
Q57 "Offered drugs @ school 12 mos"
Q58 "Ever had sex"
Q59 "How old at first sex"
Q60 "How many sex partners"
Q61 "How many sex partners 3 mos"
Q62 "Did you use alcohol/drugs @ last sex"
Q63 "Did you use condom @ last sex"
Q64 "What birth control @ last sex"
Q65 "How do you describe your weight"
Q66 "What are you trying to do about weight"
Q67 "Did you exercise to lose weight 30 days"
Q68 "Did you eat less to lose weight 30 days"
Q69 "Did you fast to lose weight 30 days"
Q70 "Did you take pill to lose weight 30 days"
Q71 "Did you vomit to lose weight 30 days"
Q72 "How many times fruit juice 7 days"
Q73 "How many times fruit 7 days"
Q74 "How many time green salad 7 days"
Q75 "How many times potatoes 7 days"
Q76 "How many times carrots 7 days"
Q77 "How many times other vegetables 7 days"
Q78 "How many times drink soda past 7 days"
Q79 "How many glass of milk 7 days"
Q80 "Days active 60 min plus past 7 days"
Q81 "How many hours watch TV"
Q82 "How many hours/day play video games"
Q83 "How many days go to PE class"
Q84 "On how many sports team 12 mos"
Q85 "Ever taught about AIDS/HIV @ school"
Q86 "Ever been told you have asthma"
Q87 "Do you still have asthma"
Q88 "How often wear motorcycle helmet"
Q89 "Ever used LSD"
Q90 "Did you do vigorous exercise 7 days"
Q91 "Did you do moderate exercise 7 days"
Q92 "How many minutes exercise in PE class"
Q93 "Injured while playing sports"
Q94 "Ever tested for HIV"
Q95 "Sunscreen use outside"
Q96 "Protection from the sun"
Q97 "Hours of sleep on school night"
Q98 "How do you describe your health"
QN8 "Never/rarely wore bicycle helmet"
QN9 "Never/rarely wore seat belt"
QN10 "Rode 1+ times with drinking driver"
QN11 "Drove 1+ times when drinking"
QN12 "Carried weapon 1+ times past 30 days"
QN13 "Carried gun 1+ past 30 days"
QN14 "Carried weapon school 1+ past 30 days"
QN15 "Missed school b/c unsafe 1+ 30 days"
QN16 "Threatened at school 1+ times 12 mos"
QN17 "Prop stolen at school 12 mos"
QN18 "Fought 1+ times 12 mos"
QN19 "Injured/treated 1+ times 12 mos"
QN20 "Fought school 1+ times 12 mos"
QN21 "Hit by bf/gf 12 mos"
QN22 "Forced to have sex"
QN23 "Sad 2 wks past 12 mos"
QN24 "Considered suicide 12 mos"
QN25 "Made suicide plan 12 mos"
QN26 "Attempted suicide 1+ times 12 mos"
QN27 "Suicide attempt w/injury 12 mos"
QN28 "Ever tried cigarettes"
QN29 "Smoked cigarette before 13"
QN30 "Smoked 1+ past 30 days"
QN31 "10+ cigarettes/day past 30 days"
QN32 "Got cigarettes in store 30 days"
QN33 "Smoked at school 1+ past 30 days"
QN34 "Smoked daily for 30 days"
QN35 "Among smokers, tried to quit smoking"
QN36 "Used snuff/dip 1+ past 30 days"
QN37 "Used snuff/dip at school 1+ 30 days"
QN38 "Smoked cigars 1+ past 30 days"
QN39 "Had 1 drink on 1+ days in life"
QN40 "Had first drink before 13"
QN41 "Had 1+ drinks past 30 days"
QN42 "Five+ drinks 1+ past 30 days"
QN43 "Bought alcohol in store past 30 days"
QN44 "Had 1+ drinks at school 1+ 30 days"
QN45 "Tried marijuana 1+ times in life"
QN46 "Tried marijuana before 13"
QN47 "Used marijuana 1+ times past 30 days"
QN48 "Used marijuana school 1+ times 30 day"
QN49 "Used cocaine 1+ times in life"
QN50 "Used cocaine 1+ times past 30 days"
QN51 "Sniffed glue 1+ times in life"
QN52 "Used heroin 1+ times in life"
QN53 "Used meth 1+ times in life"
QN54 "Used ecstasy 1+ times in life"
QN55 "Took steroids 1+ times in life"
QN56 "Injected drugs 1+ times in life"
QN57 "Offered/sold drugs at school 12 mos"
QN58 "Had sex ever"
QN59 "Had sex before 13"
QN60 "Had sex with 4+ people in life"
QN61 "Had sex with 1+ people 3 mos"
QN62 "Of current sex, used alcohol last time"
QN63 "Of current sex, used condom last time"
QN64 "Of current sex, used birth ctl last sx"
QN65 "Slightly/very overweight"
QN66 "Trying to lose weight"
QN67 "Exercised to lose weight past 30 days"
QN68 "Ate less to lose weight past 30 days"
QN69 "Fasted to lose weight past 30 days"
QN70 "Took pills to lose weight past 30 days"
QN71 "Vomited to lose weight past 30 days"
QN72 "Drank fruit juice past 7 days"
QN73 "Ate fruit past 7 days"
QN74 "Ate green salad past 7 days"
QN75 "Ate potatoes past 7 days"
QN76 "Ate carrots past 7 days"
QN77 "Ate vegetables past 7 days"
QN78 "Drank soda 1+ times/day past 7 days"
QN79 "Drank 3+ glasses milk past 7 days"
QN80 "Active 60 min on 5+ past 7 days"
QN81 "Watched 3+ hours of TV average day"
QN82 "Played video games 3+ hours/day"
QN83 "Got to PE class 1+ days average week"
QN84 "Played on 1+ sports teams 12 mos"
QN85 "Taught about AIDS in school"
QN86 "Told by doctor/nurse they had asthma"
QN87 "With current asthma"
QN88 "Never/rarely wear helmet"
QN89 "Used LSD 1+ times"
QN90 "Vigorous exercise past 7 days"
QN91 "Moderate exercise past 7 days"
QN92 "Exercised in PE 21+ minutes"
QN93 "Injured while exercising"
QN94 "Tested for HIV"
QN95 "Mostly or always wear sunscreen"
QN96 "Mostly or always protect from sun"
QN97 "Get 8+ hours sleep"
QN98 "Describe health as fair or poor"
qnfrcig "Smoked on 20 past 30 days"
qnfrvg "Ate 5+ fruits/vegetables 7 days"
qndlype "Attended PE class daily"
qnrovwgt "At risk for becoming overweight"
qnovwgt "Overweight"
qnanytob "Used any tobacco past 30 days"
weight "Analysis weight"
stratum "Stratum"
psu "PSU"
bmipct "Body Mass Index Percentage"
raceeth "Race/Ethnicity"
site "Site Code"
.
 
VALUE LABELS
Q1
1 "12 years old or younger"
2 "13 years old"
3 "14 years old"
4 "15 years old"
5 "16 years old"
6 "17 years old"
7 "18 years old or older"
/
Q2
1 "Female"
2 "Male"
/
Q3
1 "9th grade"
2 "10th grade"
3 "11th grade"
4 "12th grade"
5 "Ungraded or other grade"
/
Q4
1 "Yes"
2 "No"
/
Q8
1 "Did not ride a bicycle"
2 "Never wore a helmet"
3 "Rarely wore a helmet"
4 "Sometimes wore a helmet"
5 "Most of the time wore a helmet"
6 "Always wore a helmet"
/
Q9
1 "Never"
2 "Rarely"
3 "Sometimes"
4 "Most of the time"
5 "Always"
/
Q10
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or more times"
/
Q11
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or more times"
/
Q12
1 "0 days"
2 "1 day"
3 "2 or 3 days"
4 "4 or 5 days"
5 "6 or more days"
/
Q13
1 "0 days"
2 "1 day"
3 "2 or 3 days"
4 "4 or 5 days"
5 "6 or more days"
/
Q14
1 "0 days"
2 "1 day"
3 "2 or 3 days"
4 "4 or 5 days"
5 "6 or more days"
/
Q15
1 "0 days"
2 "1 day"
3 "2 or 3 days"
4 "4 or 5 days"
5 "6 or more days"
/
Q16
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or 7 times"
6 "8 or 9 times"
7 "10 or 11 times"
8 "12 or more times"
/
Q17
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or 7 times"
6 "8 or 9 times"
7 "10 or 11 times"
8 "12 or more times"
/
Q18
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or more times"
/
Q19
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or 7 times"
6 "8 or 9 times"
7 "10 or 11 times"
8 "12 or more times"
/
Q20
1 "Yes"
2 "No"
/
Q21
1 "Yes"
2 "No"
/
Q22
1 "Yes"
2 "No"
/
Q23
1 "Yes"
2 "No"
/
Q24
1 "Yes"
2 "No"
/
Q25
1 "Yes"
2 "No"
/
Q26
1 "Yes"
2 "No"
/
Q27
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or more times"
/
Q28
1 "Did not attempt suicide"
2 "Yes"
3 "No"
/
Q29
1 "Yes"
2 "No"
/
Q30
1 "Never smoked a cigarette"
2 "8 years old or younger"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 years old or older"
/
Q31
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q32
1 "Did not smoke cigarettes"
2 "Less than 1 cigarette"
3 "1 cigarette"
4 "2 to 5 cigarettes"
5 "6 to 10 cigarettes"
6 "11 to 20 cigarettes"
7 "More than 20 cigarettes"
/
Q33
1 "Did not smoke cigarettes"
2 "Store or gas station"
3 "Vending machine"
4 "Someone else bought them"
5 "Borrowed/bummed them"
6 "A person 18 or older"
7 "Took them from store/family "
8 "Some other way"
/
Q34
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q35
1 "Yes"
2 "No"
/
Q36
1 "Did not smoke in past 12 mos."
2 "Yes"
3 "No"
/
Q37
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q38
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q39
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q40
1 "0 days"
2 "1 or 2 days"
3 "3 to 9 days"
4 "10 to 19 days"
5 "20 to 39 days"
6 "40 to 99 days"
7 "100 or more days"
/
Q41
1 "Never drank alcohol"
2 "8 years old or younger"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 years old or older"
/
Q42
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q43
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 to 5 days"
5 "6 to 9 days"
6 "10 to 19 days"
7 "20 or more days"
/
Q44
1 "Did not drink in past 30 days"
2 "Bought in store"
3 "Bought in restaurant"
4 "Bought at public event"
5 "I gave someone money to buy"
6 "Someone gave it to me"
7 "Took from store/family"
8 "I got it some other way"
/
Q45
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q46
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 to 99 times"
7 "100 or more times"
/
Q47
1 "Never tried marijuana"
2 "8 years old or younger"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 years old or older"
/
Q48
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q49
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q50
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q51
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q52
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q53
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q54
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q55
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q56
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q57
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q58
1 "0 times"
2 "1 time"
3 "2 or more times"
/
Q59
1 "Yes"
2 "No"
/
Q60
1 "Yes"
2 "No"
/
Q61
1 "Never had sex"
2 "11 years old or younger"
3 "12 years old"
4 "13 years old"
5 "14 years old"
6 "15 years old"
7 "16 years old"
8 "17 years old or older"
/
Q62
1 "Never had sex"
2 "1 person"
3 "2 people"
4 "3 people"
5 "4 people"
6 "5 people"
7 "6 or more people"
/
Q63
1 "Never had sex"
2 "None during past 3 months"
3 "1 person"
4 "2 people"
5 "3 people"
6 "4 people"
7 "5 people"
8 "6 or more people"
/
Q64
1 "Never had sex"
2 "Yes"
3 "No"
/
Q65
1 "Never had sex"
2 "Yes"
3 "No"
/
Q66
1 "Never had sex"
2 "No method was used"
3 "Birth control pills"
4 "Condoms"
5 "Depo-Provera"
6 "Withdrawal"
7 "Some other method"
8 "Not sure"
/
Q67
1 "Very underweight"
2 "Slightly underweight"
3 "About the right weight"
4 "Slightly overweight"
5 "Very overweight"
/
Q68
1 "Lose weight"
2 "Gain weight"
3 "Stay the same weight"
4 "Not trying to do anything"
/
Q69
1 "Yes"
2 "No"
/
Q70
1 "Yes"
2 "No"
/
Q71
1 "Yes"
2 "No"
/
Q72
1 "Did not drink fruit juice"
2 "1 to 3 times past 7 days"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q73
1 "Did not eat fruit"
2 "1 to 3 times past 7 days"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q74
1 "Did not eat green salad"
2 "1 to 3 times past 7 days"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q75
1 "Did not eat potatoes"
2 "1 to 3 times past 7 days"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q76
1 "Did not eat carrots"
2 "1 to 3 times past 7 days"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q77
1 "Did not eat other vegetables "
2 "1 to 3 times past 7 days"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q78
1 "Did not drink soda or pop"
2 "1 to 3 times past 7 days"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q79
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 days"
5 "4 days"
6 "5 days"
7 "6 days"
8 "7 days"
/
Q80
1 "No TV on average school day"
2 "Less than 1 hour per day"
3 "1 hour per day"
4 "2 hours per day"
5 "3 hours per day"
6 "4 hours per day"
7 "5 or more hours per day"
/
Q81
1 "No playing video/computer game"
2 "Less than 1 hour per day"
3 "1 hour per day"
4 "2 hours per day"
5 "3 hours per day"
6 "4 hours per day"
7 "5 or more hours per day"
/
Q82
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 days"
5 "4 days"
6 "5 days"
/
Q83
1 "0 teams"
2 "1 team"
3 "2 teams"
4 "3 or more teams"
/
Q84
1 "Yes"
2 "No"
3 "Not sure"
/
Q85
1 "Yes"
2 "No"
3 "Not sure"
/
Q86
1 "I have never had asthma"
2 "Yes"
3 "No"
4 "Not sure"
/
Q87
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q88
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or 7 times"
6 "8 or 9 times"
7 "10 or 11 times"
8 "12 or more times"
/
Q89
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q90
1 "Did not drink milk"
2 "1 to 3 glasses"
3 "4 to 6 glasses"
4 "1 glass per day"
5 "2 glasses per day"
6 "3 glasses per day"
7 "4 or more glasses per day"
/
Q91
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 days"
5 "4 days"
6 "5 days"
7 "6 days"
8 "7 days"
/
Q92
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 days"
5 "4 days"
6 "5 days"
7 "6 days"
8 "7 days"
/
Q93
1 "Yes"
2 "No"
3 "Not sure"
/
Q94
1 "Never"
2 "Rarely"
3 "Sometimes"
4 "Most of the time"
5 "Always"
/
Q95
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q96
1 "4 or less hours"
2 "5 hours"
3 "6 hours"
4 "7 hours"
5 "8 hours"
6 "9 hours"
7 "10 or more hours"
/
Q97
1 "Yes"
2 "No"
/
RACEETH
1 "Am Indian / Alaska Native"
2 "Asian"
3 "Black or African American"
4 "Native Hawaiian/other PI"
5 "White"
6 "Hispanic / Latino"
7 "Multiple - Hispanic"
8 "Multiple - Non-Hispanic"
/.

MISSING VALUES
Q1 (" ")
Q2 (" ") Q3 (" ") Q4 (" ")
Q5 ("        ") Q6 ("    ") Q7 ("      ")
Q8 (" ") Q9 (" ") Q10 (" ")
Q11 (" ") Q12 (" ") Q13 (" ")
Q14 (" ") Q15 (" ") Q16 (" ")
Q17 (" ") Q18 (" ") Q19 (" ")
Q20 (" ") Q21 (" ") Q22 (" ")
Q23 (" ") Q24 (" ") Q25 (" ")
Q26 (" ") Q27 (" ") Q28 (" ")
Q29 (" ") Q30 (" ") Q31 (" ")
Q32 (" ") Q33 (" ") Q34 (" ")
Q35 (" ") Q36 (" ") Q37 (" ")
Q38 (" ") Q39 (" ") Q40 (" ")
Q41 (" ") Q42 (" ") Q43 (" ")
Q44 (" ") Q45 (" ") Q46 (" ")
Q47 (" ") Q48 (" ") Q49 (" ")
Q50 (" ") Q51 (" ") Q52 (" ")
Q53 (" ") Q54 (" ") Q55 (" ")
Q56 (" ") Q57 (" ") Q58 (" ")
Q59 (" ") Q60 (" ") Q61 (" ")
Q62 (" ") Q63 (" ") Q64 (" ")
Q65 (" ") Q66 (" ") Q67 (" ")
Q68 (" ") Q69 (" ") Q70 (" ")
Q71 (" ") Q72 (" ") Q73 (" ")
Q74 (" ") Q75 (" ") Q76 (" ")
Q77 (" ") Q78 (" ") Q79 (" ")
Q80 (" ") Q81 (" ") Q82 (" ")
Q83 (" ") Q84 (" ") Q85 (" ")
Q86 (" ") Q87 (" ") Q88 (" ")
Q89 (" ") Q90 (" ") Q91 (" ")
Q92 (" ") Q93 (" ") Q94 (" ")
Q95 (" ") Q96 (" ") Q97 (" ")
Q98 (" ")
QN8 (" ") QN9 (" ") QN10 (" ")
QN11 (" ") QN12 (" ") QN13 (" ")
QN14 (" ") QN15 (" ") QN16 (" ")
QN17 (" ") QN18 (" ") QN19 (" ")
QN20 (" ") QN21 (" ") QN22 (" ")
QN23 (" ") QN24 (" ") QN25 (" ")
QN26 (" ") QN27 (" ") QN28 (" ")
QN29 (" ") QN30 (" ") QN31 (" ")
QN32 (" ") QN33 (" ") QN34 (" ")
QN35 (" ") QN36 (" ") QN37 (" ")
QN38 (" ") QN39 (" ") QN40 (" ")
QN41 (" ") QN42 (" ") QN43 (" ")
QN44 (" ") QN45 (" ") QN46 (" ")
QN47 (" ") QN48 (" ") QN49 (" ")
QN50 (" ") QN51 (" ") QN52 (" ")
QN53 (" ") QN54 (" ") QN55 (" ")
QN56 (" ") QN57 (" ") QN58 (" ")
QN59 (" ") QN60 (" ") QN61 (" ")
QN62 (" ") QN63 (" ") QN64 (" ")
QN65 (" ") QN66 (" ") QN67 (" ")
QN68 (" ") QN69 (" ") QN70 (" ")
QN71 (" ") QN72 (" ") QN73 (" ")
QN74 (" ") QN75 (" ") QN76 (" ")
QN77 (" ") QN78 (" ") QN79 (" ")
QN80 (" ") QN81 (" ") QN82 (" ")
QN83 (" ") QN84 (" ") QN85 (" ")
QN86 (" ") QN87 (" ") QN88 (" ")
QN89 (" ") QN90 (" ") QN91 (" ")
QN92 (" ") QN93 (" ") QN94 (" ")
QN95 (" ") QN96 (" ") QN97 (" ")
QN98 (" ")
site ("   ")
qnfrcig (" ")
qnanytob (" ")
qndepo (" ")
qndepopl (" ")
qndual (" ")
qnfrvg (" ")
qnfrvg2 (" ")
qnfruit (" ")
qnveg (" ")
qndlype (" ")
qnpa0day (" ")
qnpa7day (" ")
qnowt (" ")
qnobese (" ")
weight ("          ")
stratum ("   ")
psu ("      ")
bmipct ("     ")
raceeth ("  ").

Formats q6 q7 (F5.2) weight (F12.7) .

EXECUTE.

SAVE OUTFILE='c:\yrbs2007\yrbs2007.sav'
/COMPRESSED.
EXECUTE.

GET FILE='c:\yrbs2007\yrbs2007.sav'.
EXECUTE.
