* 
This SPSS syntax reads ASCII format (text format) 2005 YRBS data and creates a formatted 
and labeled SPSS data file that you can analyze in SPSS;

*
Change the file location specifications from "c:\yrbs2005" to the location where you have 
stored the SPSS syntax and the YRBS ASCII data file before you run this syntax;  
Change the location specification in three places - in the "data list" statement at the top 
of the syntax and in the "save" and "get" statements at the end of the syntax;.

DATA LIST FILE="c:\yrbs2005\yrbs2005.dat"/
Q1 17-17 (A) Q2 18-18 (A) Q3 19-19 (A)
Q4 20-21 (A) Q5 22-25  Q6 26-31
Q7 32-32 (A) Q8 33-33 (A) Q9 34-34 (A)
Q10 35-35 (A) Q11 36-36 (A) Q12 37-37 (A)
Q13 38-38 (A) Q14 39-39 (A) Q15 40-40 (A)
Q16 41-41 (A) Q17 42-42 (A) Q18 43-43 (A)
Q19 44-44 (A) Q20 45-45 (A) Q21 46-46 (A)
Q22 47-47 (A) Q23 48-48 (A) Q24 49-49 (A)
Q25 50-50 (A) Q26 51-51 (A) Q27 52-52 (A)
Q28 53-53 (A) Q29 54-54 (A) Q30 55-55 (A)
Q31 56-56 (A) Q32 57-57 (A) Q33 58-58 (A)
Q34 59-59 (A) Q35 60-60 (A) Q36 61-61 (A)
Q37 62-62 (A) Q38 63-63 (A) Q39 64-64 (A)
Q40 65-65 (A) Q41 66-66 (A) Q42 67-67 (A)
Q43 68-68 (A) Q44 69-69 (A) Q45 70-70 (A)
Q46 71-71 (A) Q47 72-72 (A) Q48 73-73 (A)
Q49 74-74 (A) Q50 75-75 (A) Q51 76-76 (A)
Q52 77-77 (A) Q53 78-78 (A) Q54 79-79 (A)
Q55 80-80 (A) Q56 81-81 (A) Q57 82-82 (A)
Q58 83-83 (A) Q59 84-84 (A) Q60 85-85 (A)
Q61 86-86 (A) Q62 87-87 (A) Q63 88-88 (A)
Q64 89-89 (A) Q65 90-90 (A) Q66 91-91 (A)
Q67 92-92 (A) Q68 93-93 (A) Q69 94-94 (A)
Q70 95-95 (A) Q71 96-96 (A) Q72 97-97 (A)
Q73 98-98 (A) Q74 99-99 (A) Q75 100-100 (A)
Q76 101-101 (A) Q77 102-102 (A) Q78 103-103 (A)
Q79 104-104 (A) Q80 105-105 (A) Q81 106-106 (A)
Q82 107-107 (A) Q83 108-108 (A) Q84 109-109 (A)
Q85 110-110 (A) Q86 111-111 (A) Q87 112-112 (A)
Q88 113-113 (A) Q89 114-114 (A) Q90 115-115 (A)
Q91 116-116 (A) Q92 117-117 (A) Q93 118-118 (A)
Q94 119-119 (A) Q95 120-120 (A) Q96 121-121 (A)
Q97 122-122 (A) 
QN7 123-123 QN8 124-124 QN9 125-125
QN10 126-126 QN11 127-127 QN12 128-128
QN13 129-129 QN14 130-130 QN15 131-131
QN16 132-132 QN17 133-133 QN18 134-134
QN19 135-135 QN20 136-136 QN21 137-137
QN22 138-138 QN23 139-139 QN24 140-140
QN25 141-141 QN26 142-142 QN27 143-143
QN28 144-144 QN29 145-145 QN30 146-146
QN31 147-147 QN32 148-148 QN33 149-149
QN34 150-150 QN35 151-151 QN36 152-152
QN37 153-153 QN38 154-154 QN39 155-155
QN40 156-156 QN41 157-157 QN42 158-158
QN43 159-159 QN44 160-160 QN45 161-161
QN46 162-162 QN47 163-163 QN48 164-164
QN49 165-165 QN50 166-166 QN51 167-167
QN52 168-168 QN53 169-169 QN54 170-170
QN55 171-171 QN56 172-172 QN57 173-173
QN58 174-174 QN59 175-175 QN60 176-176
QN61 177-177 QN62 178-178 QN63 179-179
QN64 180-180 QN65 181-181 QN66 182-182
QN67 183-183 QN68 184-184 QN69 185-185
QN70 186-186 QN71 187-187 QN72 188-188
QN73 189-189 QN74 190-190 QN75 191-191
QN76 192-192 QN77 193-193 QN78 194-194
QN79 195-195 QN80 196-196 QN81 197-197
QN82 198-198 QN83 199-199 QN84 200-200
QN85 201-201 QN86 202-202 QN87 203-203
QN88 204-204 QN89 205-205 QN90 206-206
QN91 207-207 QN92 208-208 QN93 209-209
QN94 210-210 QN95 211-211 QN96 212-212
QN97 213-213 QNFRCIG 214-214 QNFRVG 215-215
QNDLYPE 216-216 QNROVWGT 217-217 QNOVWGT 218-218 
QNANYTOB 219-219 QNMINPA 220-220 QNNOPA 221-221
QNASATCK 222-222 Q4ORIG 350-357 (A)
Weight 358-369 PSU 370-374 Stratum 375-378
BMIPct 379-383 ETHORIG 384-384 (A) RACEORIG 385-389 (A).
EXECUTE.
 
VARIABLE LABELS
Q1 "How old are you"
Q2 "What is your sex"
Q3 "In what grade are you"
Q4 "How do you describe yourself"
Q5 "How tall are you"
Q6 "How much do you weigh"
Q7 "How do you describe your health"
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
Q43 "How many days drink @ school 30 days"
Q44 "How many times smoke marijuana"
Q45 "How old when first tried marijuana"
Q46 "How many times use marijuana 30 days"
Q47 "How many times marijuana@school 30 days"
Q48 "How many times use cocaine"
Q49 "How many times use cocaine 30 days"
Q50 "How many times sniffed glue"
Q51 "How many times used heroin"
Q52 "How many times used methamphetamines"
Q53 "Ecstacy one or more time"
Q54 "How many times used steroids"
Q55 "How many times injected drugs"
Q56 "Offered drugs @ school 12 mos"
Q57 "Ever had sex"
Q58 "How old at first sex"
Q59 "How many sex partners"
Q60 "How many sex partners 3 mos"
Q61 "Did you use alcohol/drugs @ last sex"
Q62 "Did you use condom @ last sex"
Q63 "What birth control @ last sex"
Q64 "How do you describe your weight"
Q65 "What are you trying to do about weight"
Q66 "Did you exercise to lose weight 30 days"
Q67 "Did you eat less to lose weight 30 days"
Q68 "Did you fast to lose weight 30 days"
Q69 "Did you take pill to lose weight 30 days"
Q70 "Did you vomit to lose weight 30 days"
Q71 "How many times fruit juice 7 days"
Q72 "How many times fruit 7 days"
Q73 "How many time green salad 7 days"
Q74 "How many times potatoes 7 days"
Q75 "How many times carrots 7 days"
Q76 "How many times other vegetables 7 days"
Q77 "How many glass of milk 7 days"
Q78 "Did you do vigorous exercise 7 days"
Q79 "Did you do moderate exercise 7 days"
Q80 "Days active 60 min plus past 7 days"
Q81 "How many hours watch TV"
Q82 "How many days go to PE class"
Q83 "How many minutes exercise in PE class"
Q84 "On how many sports team 12 mos"
Q85 "Ever taught about AIDS/HIV @ school"
Q86 "Ever been told you have asthma"
Q87 "Asthma attack in past 12 months"
Q88 "How often wear motorcycle helmet"
Q89 "Show age proof buying cigarettes 30 days"
Q90 "Times used hallucinogens"
Q91 "Computer use per day"
Q92 "Injured while playing sports"
Q93 "Ever tested for HIV"
Q94 "Wear sunscreen when outside"
Q95 "Protection from the sun"
Q96 "Disability/health problem"
Q97 "Days missed class w/out permission"
QN7 "Described health as fair/poor"
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
QN43 "Had 1+ drinks at school 1+ 30 days"
QN44 "Tried marijuana 1+ times in life"
QN45 "Tried marijuana before 13"
QN46 "Used marijuana 1+ times past 30 days"
QN47 "Used marijuana school 1+ times 30 day"
QN48 "Used cocaine 1+ times in life"
QN49 "Used cocaine 1+ times past 30 days"
QN50 "Sniffed glue 1+ times in life"
QN51 "Used heroin 1+ times in life"
QN52 "Used meth 1+ times in life"
QN53 "Used ecstasy 1+ times in life"
QN54 "Took steroids 1+ times in life"
QN55 "Injected drugs 1+ times in life"
QN56 "Offered/sold drugs at school 12 mos"
QN57 "Had sex ever"
QN58 "Had sex before 13"
QN59 "Had sex with 4+ people in life"
QN60 "Had sex with 1+ people 3 mos"
QN61 "Of current sex, used alcohol last time"
QN62 "Of current sex, used condom last time"
QN63 "Of current sex, used birth ctl last sx"
QN64 "Slightly/very overweight"
QN65 "Trying to lose weight"
QN66 "Exercised to lose weight past 30 days"
QN67 "Ate less to lose weight past 30 days"
QN68 "Fasted to lose weight past 30 days"
QN69 "Took pills to lose weight past 30 days"
QN70 "Vomited to lose weight past 30 days"
QN71 "Drank fruit juice past 7 days"
QN72 "Ate fruit past 7 days"
QN73 "Ate green salad past 7 days"
QN74 "Ate potatoes past 7 days"
QN75 "Ate carrots past 7 days"
QN76 "Ate vegetables past 7 days"
QN77 "Drank 3+ glasses milk past 7 days"
QN78 "Exercised vigorously past 7 days"
QN79 "Exercised moderately past 7 days"
QN80 "Active 60 min on 5+ past 7 days"
QN81 "Watched 3+ hours of TV average day"
QN82 "Got to PE class 1+ days average week"
QN83 "Of enrolled in PE, exercised 20 min"
QN84 "Played on 1+ sports teams 12 mos"
QN85 "Taught about AIDS in school"
QN86 "Told by doctor/nurse they had asthma"
QN87 "Told had asthma and current asthma"
QN88 "Never/rarely wore motorcycle helmet"
QN89 "Not asked proof age buying cigarettes"
QN90 "Used hallucinogenic drugs"
QN91 "Played video games 3+ hours per day"
QN92 "Injured playing sports seen by doctor"
QN93 "Tested for HIV"
QN94 "Most time/always wore sunscreen outside"
QN95 "Most time/always protect from sun"
QN96 "Has a disability/health problem"
QN97 "Missed class w/out permission 30 days"
qnfrcig "Smoked on 20 past 30 days"
qnfrvg "Ate 5+ fruits/vegetables 7 days"
qndlype "Attended PE class daily"
qnrovwgt "At risk for becoming overweight"
qnovwgt "Overweight"
qnanytob "Used any tobacco past 30 days"
qnminpa "Did not exercise 20 min 3+ past 7 days"
qnnopa "No exercise"
qnasatck "Had asthma attack past 12 months"
weight "Analysis weight"
stratum "Stratum"
psu "PSU"
bmipct "Body Mass Index Percentage"
q4orig "Race/ethnicity as originally scanned"
ethorig "Ethnicity as originally scanned"
raceorig "Race as originally scanned"
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
1 "Am Indian / Alaska Native"
2 "Asian"
3 "Black or African American"
4 "Hispanic or Latino"
5 "Native Hawaiian/other PI"
6 "White"
7 "Multiple - Hispanic"
8 "Multiple - Non-hispanic"
/
Q7
1 "Excellent"
2 "Very good"
3 "Good"
4 "Fair"
5 "Poor"
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
5 "6 or 7 times"
6 "8 or 9 times"
7 "10 or 11 times"
8 "12 or more times"
/
Q19
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or more times"
/
Q20
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or 7 times"
6 "8 or 9 times"
7 "10 or 11 times"
8 "12 or more times"
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
1 "0 times"
2 "1 time"
3 "2 or 3 times"
4 "4 or 5 times"
5 "6 or more times"
/
Q27
1 "Did not attempt suicide"
2 "Yes"
3 "No"
/
Q28
1 "Yes"
2 "No"
/
Q29
1 "Never smoked a cigarette"
2 "8 years old or younger"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 years old or older"
/
Q30
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q31
1 "Did not smoke cigarettes"
2 "Less than 1 cigarette"
3 "1 cigarette"
4 "2 to 5 cigarettes"
5 "6 to 10 cigarettes"
6 "11 to 20 cigarettes"
7 "More than 20 cigarettes"
/
Q32
1 "Did not smoke cigarettes"
2 "Store or gas station"
3 "Vending machine"
4 "Someone else bought them"
5 "Borrowed/bummed them"
6 "A person 18 or older"
7 "Took them from store/family "
8 "Some other way"
/
Q33
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q34
1 "Yes"
2 "No"
/
Q35
1 "Did not smoke in past 12 mos."
2 "Yes"
3 "No"
/
Q36
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
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
3 "3 to 9 days"
4 "10 to 19 days"
5 "20 to 39 days"
6 "40 to 99 days"
7 "100 or more days"
/
Q40
1 "Never drank alcohol"
2 "8 years old or younger"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 years old or older"
/
Q41
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q42
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 to 5 days"
5 "6 to 9 days"
6 "10 to 19 days"
7 "20 or more days"
/
Q43
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 to 19 days"
6 "20 to 29 days"
7 "All 30 days"
/
Q44
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 to 99 times"
7 "100 or more times"
/
Q45
1 "Never tried marijuana"
2 "8 years old or younger"
3 "9 or 10 years old"
4 "11 or 12 years old"
5 "13 or 14 years old"
6 "15 or 16 years old"
7 "17 years old or older"
/
Q46
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q47
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
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
2 "1 time"
3 "2 or more times"
/
Q56
1 "Yes"
2 "No"
/
Q57
1 "Yes"
2 "No"
/
Q58
1 "Never had sex"
2 "11 years old or younger"
3 "12 years old"
4 "13 years old"
5 "14 years old"
6 "15 years old"
7 "16 years old"
8 "17 years old or older"
/
Q59
1 "Never had sex"
2 "1 person"
3 "2 people"
4 "3 people"
5 "4 people"
6 "5 people"
7 "6 or more people"
/
Q60
1 "Never had sex"
2 "None during past 3 months"
3 "1 person"
4 "2 people"
5 "3 people"
6 "4 people"
7 "5 people"
8 "6 or more people"
/
Q61
1 "Never had sex"
2 "Yes"
3 "No"
/
Q62
1 "Never had sex"
2 "Yes"
3 "No"
/
Q63
1 "Never had sex"
2 "No method was used"
3 "Birth control pills"
4 "Condoms"
5 "Depo-Provera"
6 "Withdrawal"
7 "Some other method"
8 "Not sure"
/
Q64
1 "Very underweight"
2 "Slightly underweight"
3 "About the right weight"
4 "Slightly overweight"
5 "Very overweight"
/
Q65
1 "Lose weight"
2 "Gain weight"
3 "Stay the same weight"
4 "Not trying to do anything"
/
Q66
1 "Yes"
2 "No"
/
Q67
1 "Yes"
2 "No"
/
Q68
1 "Yes"
2 "No"
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
1 "Did not drink fruit juice"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q72
1 "Did not eat fruit"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q73
1 "Did not eat green salad"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q74
1 "Did not eat potatoes"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q75
1 "Did not eat carrots"
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q76
1 "Did not eat other vegetables "
2 "1 to 3 times"
3 "4 to 6 times"
4 "1 time per day"
5 "2 times per day"
6 "3 times per day"
7 "4 or more times per day"
/
Q77
1 "Did not drink milk"
2 "1 to 3 glasses past 7 days"
3 "4 to 6 glasses past 7 days"
4 "1 glass per day"
5 "2 glasses per day"
6 "3 glasses per day"
7 "4 or more glasses per day"
/
Q78
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 days"
5 "4 days"
6 "5 days"
7 "6 days"
8 "7 days"
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
1 "0 days"
2 "1 day"
3 "2 days"
4 "3 days"
5 "4 days"
6 "5 days"
7 "6 days"
8 "7 days"
/
Q81
1 "No TV on average school day"
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
1 "Do not take PE"
2 "Less than 10 minutes"
3 "10 to 20 minutes"
4 "21 to 30 minutes"
5 "31 to 40 minutes"
6 "41 to 50 minutes"
7 "51 to 60 minutes"
8 "More than 60 minutes"
/
Q84
1 "0 teams"
2 "1 team"
3 "2 teams"
4 "3 or more teams"
/
Q85
1 "Yes"
2 "No"
3 "Not sure"
/
Q86
1 "Yes"
2 "No"
3 "Not sure"
/
Q87
1 "I do not have asthma"
2 "Have asthma/no episode 12 mos"
3 "Had episode in the past 12 mos"
4 "Not sure"
/
Q88
1 "Did not ride a motorcycle"
2 "Never wore a helmet"
3 "Rarely wore a helmet"
4 "Sometimes wore a helmet"
5 "Most of the time wore a helmet"
6 "Always wore a helmet"
/
Q89
1 "Did not buy cigarettes"
2 "Yes"
3 "No"
/
Q90
1 "0 times"
2 "1 or 2 times"
3 "3 to 9 times"
4 "10 to 19 times"
5 "20 to 39 times"
6 "40 or more times"
/
Q91
1 "No playing video/computer game"
2 "Less than 1 hour per day"
3 "1 hour per day"
4 "2 hours per day"
5 "3 hours per day"
6 "4 hours per day"
7 "5 or more hours per day"
/
Q92
1 "No exercise in past 30 days"
2 "Yes"
3 "No"
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
1 "Never"
2 "Rarely"
3 "Sometimes"
4 "Most of the time"
5 "Always"
/
Q96
1 "Yes"
2 "No"
3 "Not sure"
/
Q97
1 "0 days"
2 "1 or 2 days"
3 "3 to 5 days"
4 "6 to 9 days"
5 "10 or more days"
/.

MISSING VALUES
Q1 (" ")
Q2 (" ") Q3 (" ") Q4 ("  ")
Q5 ("    ") Q6 ("      ") Q7 (" ")
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
qnfrcig (" ")
qnfrvg (" ")
qndlype (" ")
qnrovwgt (" ")
qnovwgt (" ")
qnanytob (" ")
qnminpa (" ")
qnnopa (" ")
qnasatck (" ")
q4orig ("        ")
weight ("            ")
psu ("     ")
stratum ("    ")
bmipct ("     ")
ethorig (" ")
raceorig ("     ").

Formats q5 (F4.2) q6 (F5.2) weight (F12.7) .

EXECUTE.

SAVE OUTFILE='c:\yrbs2005\yrbs2005.sav'
/COMPRESSED.
EXECUTE.

GET FILE='c:\yrbs2005\yrbs2005.sav'.
EXECUTE.
