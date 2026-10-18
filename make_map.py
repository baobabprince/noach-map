import json,html
from pathlib import Path
world=json.load(open('/home/user/world.geojson'))
# lightweight coastline polygons, approximate equirectangular canvas
W,H=1200,730
lon0,lon1=-12,68; lat0,lat1=-4,49
def xy(lon,lat):return ((lon-lon0)/(lon1-lon0)*W,(lat1-lat)/(lat1-lat0)*H)
paths=[]
for f in world['features']:
 g=f['geometry']; polys= g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']] if g['type']=='Polygon' else []
 for poly in polys:
  for ring in poly[:1]:
   pts=[p for p in ring if lon0-3<=p[0]<=lon1+3 and lat0-3<=p[1]<=lat1+3]
   if len(pts)<3:continue
   step=max(1,len(pts)//450)
   coords=[xy(*p[:2]) for p in pts[::step]]
   if len(coords)<3:continue
   paths.append('M'+'L'.join(f'{x:.1f},{y:.1f}' for x,y in coords)+'Z')
# data rows: name|branch|parent|verse|confidence|site|lon|lat|alternatives (site~lon~lat separated by ;)|note
raw='''גֹּמֶר|יפת|יפת|2|בינוני|אנטוליה הצפונית / הקימרים|36|41||זיהוי עם הקימרים; תחום נייד
מָגוֹג|יפת|יפת|2|נמוך|צפון הים השחור|38|46||זיהוי מסופק; אין אתר מוסכם
מָדַי|יפת|יפת|2|גבוה|מדי, צפון־מערב איראן|48|35||
יָוָן|יפת|יפת|2|גבוה|יוניה, מערב אנטוליה|27|38||
תֻבָל|יפת|יפת|2|בינוני|טבאל, מרכז אנטוליה|35|38||
מֶשֶׁךְ|יפת|יפת|2|בינוני|מושכי, מרכז־מזרח אנטוליה|38|39||
תִּירָס|יפת|יפת|2|נמוך|תראקיה|26|42||זיהוי מסורתי, לא ודאי
אַשְׁכְּנַז|יפת|גמר|3|בינוני|אזור ארמניה / סקיתים|44|40||לא גרמניה של ימי הביניים
רִיפַת|יפת|גמר|3|נמוך|פפלגוניה, צפון אנטוליה|33|41||הצעה בלבד
תֹּגַרְמָה|יפת|גמר|3|בינוני|טיל־גרימו / מזרח אנטוליה|39|39||
אֱלִישָׁה|יפת|יון|4|נמוך|קפריסין|33|35|אליס ביוון~22~38|שני זיהויים מוצעים
תַּרְשִׁישׁ|יפת|יון|4|נמוך|טרטסוס, דרום ספרד|−6.3|37|סרדיניה~9~40;טרסוס, קיליקיה~34.9~37|שנוי במחלוקת
כִּתִּים|יפת|יון|4|גבוה|כִּתִּיוֹן, קפריסין|33.6|34.9||
דֹּדָנִים|יפת|יון|4|נמוך|דודונה, יוון|20.8|39.5|רודוס (נוסח רודנים)~28~36.2|בדברי הימים א א:ז: רודנים
כּוּשׁ|חם|חם|6|גבוה|נוביה, סודאן|32|18|קרן אפריקה~40~9|תחום גאוגרפי רחב
מִצְרַיִם|חם|חם|6|גבוה|מצרים|30|27||
פּוּט|חם|חם|6|נמוך|לוב|20|27|פונט, קרן אפריקה~42~12|שתי הצעות שונות
כְּנַעַן|חם|חם|6|גבוה|כנען / הלבנט הדרומי|35|32||
סְבָא|חם|כוש|7|נמוך|אזור מרואה, סודאן|33.7|16.9|קרן אפריקה~40~12|אין ודאות בזהות
חֲוִילָה|חם|כוש|7|נמוך|חצי האי ערב, צפון־מערב|38|27|דרום חצי האי ערב~44~17|מופיע גם בבני יקטן
סַבְתָּה|חם|כוש|7|נמוך|דרום חצי האי ערב|46|16||הצעה גאוגרפית כללית בלבד
רַעְמָה|חם|כוש|7|נמוך|דרום־מערב חצי האי ערב|43|16||
סַבְתְּכָא|חם|כוש|7|נמוך|דרום חצי האי ערב|49|15||הצעה גאוגרפית כללית בלבד
שְׁבָא|חם|רעמה|7|בינוני|סבא, תימן|44.2|15.4||מופיע גם בבני יקטן
דְּדָן|חם|רעמה|7|בינוני|דדן / אל־עולא, צפון־מערב ערב|37.9|26.6||
נִמְרֹד|חם|כוש|8–12|בינוני|שנער / דרום מסופוטמיה|44.5|32.5||פס׳ י–יב מתארים ממלכה וערים, לא צאצאים נוספים
לוּדִים|חם|מצרים|13|נמוך|צפון אפריקה / מצרים|28|30||אין לזהות בהכרח עם לוד בן שם
עֲנָמִים|חם|מצרים|13|נמוך|||||זיהוי גאוגרפי לא מבוסס
לְהָבִים|חם|מצרים|13|נמוך|לוב / צפון אפריקה|23|31||זיהוי משוער
נַפְתֻּחִים|חם|מצרים|13|נמוך|דלתת הנילוס|31|31||זיהוי משוער
פַּתְרֻסִים|חם|מצרים|14|בינוני|פתרוס / מצרים העליונה|32|25||
כַּסְלֻחִים|חם|מצרים|14|נמוך|||||מוצא הפלשתים בנוסח הפרק; מקום הקבוצה אינו ודאי
פְּלִשְׁתִּים|חם|כסלחים|14|גבוה|מישור החוף הדרומי, פלשת|34.5|31.6||הטקסט אומר ״אשר יצאו משם״; אינם בן שנמנה כיתר הרשימה
כַּפְתֹּרִים|חם|מצרים|14|בינוני|כרתים / כפתור|25|35|חוף אנטוליה הדרומי~30~37|הזיהוי עם כרתים מקובל אך אינו מוכרע
צִידֹן|חם|כנען|15|גבוה|צידון, לבנון|35.4|33.6||
חֵת|חם|כנען|15|בינוני|אנטוליה / ארץ החתים|35|39|חִתים בדרום הלבנט~35~32|ייתכן שהשם מתייחס לקבוצות שונות
הַיְבוּסִי|חם|כנען|16|גבוה|ירושלים / יבוס|35.2|31.8||
הָאֱמֹרִי|חם|כנען|16|בינוני|סוריה והלבנט|37|35||קבוצה בעלת תפוצה רחבה
הַגִּרְגָּשִׁי|חם|כנען|16|נמוך|||||מיקומם המדויק אינו ידוע
הַחִוִּי|חם|כנען|17|נמוך|צפון כנען / לבנון|35.7|34||השערה בלבד
הָעַרְקִי|חם|כנען|17|גבוה|ערקה, צפון לבנון|36|34.5||
הַסִּינִי|חם|כנען|17|בינוני|סִין, צפון לבנון|36.1|34.3||לא סין במזרח אסיה
הָאַרְוָדִי|חם|כנען|18|גבוה|ארווד, חוף סוריה|35.9|34.9||
הַצְּמָרִי|חם|כנען|18|בינוני|צומר / חוף סוריה|35.9|34.6||
הַחֲמָתִי|חם|כנען|18|גבוה|חמת, סוריה|36.75|35.1||
עֵילָם|שם|שם|22|גבוה|עילם / דרום־מערב איראן|48.5|31.5||
אַשּׁוּר|שם|שם|22|גבוה|אשור / צפון מסופוטמיה|43.3|35.5||בפס׳ יא מופיע גם ״אשור״; פירוש התחביר שנוי במחלוקת
אַרְפַּכְשַׁד|שם|שם|22|נמוך|צפון מסופוטמיה|42|36||אין זיהוי מוסכם; הנקודה סכמטית בלבד
לוּד|שם|שם|22|בינוני|לידיה / מערב אנטוליה|28|38.5||לא זהה בהכרח ללודים בני מצרים
אֲרָם|שם|שם|22|גבוה|סוריה / ארם|37|36||
עוּץ|שם|ארם|23|נמוך|צפון־מערב ערב|38|29|אזור אדום~35~30|זיהוי שנוי במחלוקת
חוּל|שם|ארם|23|נמוך|||||אין זיהוי מבוסס
גֶּתֶר|שם|ארם|23|נמוך|||||אין זיהוי מבוסס
מַשׁ|שם|ארם|23|נמוך|||||אין זיהוי מבוסס; בדברי הימים: משך
שֶׁלַח|שם|ארפכשד|24|נמוך|||||שם בשרשרת יוחסין, ללא אתר מזוהה
עֵבֶר|שם|שלח|24|נמוך|||||אין לקבוע מקום על סמך השם בלבד
פֶּלֶג|שם|עבר|25|נמוך|||||אין מקום מוסכם; ״נפלגה הארץ״ אינו קואורדינטה
יָקְטָן|שם|עבר|25|בינוני|דרום חצי האי ערב (תחום בני יקטן)|45|17||תחום משוער לבניו, לא יישוב מזוהה
אַלְמוֹדָד|שם|יקטן|26|נמוך|||||אין זיהוי מבוסס
שָׁלֶף|שם|יקטן|26|נמוך|||||אין זיהוי מבוסס
חֲצַרְמָוֶת|שם|יקטן|26|גבוה|חצרמוות / חַדְרַמַוְת, תימן|49|16||
יָרַח|שם|יקטן|26|נמוך|||||אין זיהוי מבוסס
הֲדוֹרָם|שם|יקטן|27|נמוך|||||אין זיהוי מבוסס
אוּזָל|שם|יקטן|27|בינוני|אוזל / צנעא, תימן|44.2|15.35||זיהוי מסורתי
דִּקְלָה|שם|יקטן|27|נמוך|||||אין זיהוי מבוסס
עוֹבָל|שם|יקטן|28|נמוך|||||אין זיהוי מבוסס
אֲבִימָאֵל|שם|יקטן|28|נמוך|||||אין זיהוי מבוסס
שְׁבָא|שם|יקטן|28|בינוני|סבא / תימן|44.5|15.5||אותו שם מופיע גם בין בני רעמה
אוֹפִיר|שם|יקטן|29|נמוך|דרום חצי האי ערב|48|14|קרן אפריקה~42~11;חוף הודו (מחוץ לתחום)~73~16|האתר אינו ידוע; החלופות הן השערות בלבד
חֲוִילָה|שם|יקטן|29|נמוך|חצי האי ערב|45|23||מופיע גם בבני כוש
יוֹבָב|שם|יקטן|29|נמוך|||||אין זיהוי מבוסס'''
rows=[]
for line in raw.splitlines():
 a=line.split('|'); assert len(a)==10,(line,len(a))
 name,branch,parent,verse,confidence,place,lon,lat,alts,note=a
 loc=[]
 if lon and lat:loc.append({'label':place,'lon':float(lon.replace('−','-')),'lat':float(lat),'primary':True})
 for alt in alts.split(';'):
  if alt:
   s,x,y=alt.split('~');loc.append({'label':s,'lon':float(x),'lat':float(y),'primary':False})
 rows.append(dict(name=name,branch=branch,parent=parent,verse=verse,confidence=confidence,locations=loc,note=note))
print('entries',len(rows),'unmapped',sum(not x['locations'] for x in rows))
Path('/home/user/noah_data.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
land=''.join('<path d="'+p+'"/>' for p in paths)
jsdata=json.dumps(rows,ensure_ascii=False)
page=r'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>מפת לוח העמים | בראשית י׳</title><style>
:root{--ink:#172e3a;--muted:#64777e;--paper:#f6f2e9;--line:#d9dedb;--j:#526f9e;--h:#bd7950;--s:#5c927f}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:system-ui,'Arial',sans-serif}header{padding:22px 30px 16px;background:#102d38;color:#f7f1df;display:flex;align-items:end;justify-content:space-between;gap:16px;flex-wrap:wrap}h1{font-family:Georgia,serif;font-size:clamp(27px,3vw,42px);font-weight:500;margin:0}header p{margin:5px 0 0;color:#b9c9c5;font-size:14px}.eyebrow{font-size:11px;letter-spacing:.13em;color:#b6c8bc}main{display:grid;grid-template-columns:minmax(300px,350px) minmax(0,1fr);height:min(790px,calc(100vh - 112px));min-height:610px}.side{background:#fffdf8;border-left:1px solid var(--line);display:flex;flex-direction:column;overflow:hidden}.controls{padding:18px;border-bottom:1px solid var(--line)}.search{width:100%;padding:11px 13px;border:1px solid #cbd7d4;border-radius:8px;font:inherit;background:#fff}.filters{display:flex;gap:6px;margin:13px 0 10px}.filter{border:1px solid #d7dcda;border-radius:6px;background:white;padding:8px 9px;cursor:pointer;font:inherit;font-size:13px;flex:1}.filter.active{background:#173a45;color:white}.toggles{font-size:12px;color:#51646a;display:flex;align-items:center;gap:8px}.list{overflow:auto;flex:1;padding:4px 11px}.row{display:flex;width:100%;text-align:right;align-items:center;gap:9px;padding:10px 8px;border:0;border-bottom:1px solid #edf0ed;background:transparent;cursor:pointer;color:var(--ink);font:inherit}.row:hover,.row.selected{background:#eaf2ee;border-radius:5px}.swatch{height:10px;width:10px;border-radius:50%;flex:none}.row strong{font-size:14px;font-weight:600}.row small{font-size:11px;color:#71838a;margin-right:auto}.mapwrap{position:relative;overflow:hidden;background:#cce1e2;touch-action:none;cursor:grab}.mapwrap:active{cursor:grabbing}svg{width:100%;height:100%;display:block}.land path{fill:#eee9db;stroke:#c5c9bd;stroke-width:.65;vector-effect:non-scaling-stroke}.grid line{stroke:#ffffff80;stroke-width:.8}.grid text{fill:#698b91;font-size:11px;direction:ltr}.sea-label{fill:#6c9ba2;font-size:15px;letter-spacing:2px;opacity:.75}.pin{cursor:pointer}.pin circle.core{stroke:#fffdf7;stroke-width:1.8;filter:drop-shadow(0 1px 2px #42565a77)}.pin circle.halo{fill:none;stroke-width:2;opacity:.8}.pin.alt circle.core{opacity:.6;stroke-dasharray:2 1}.pin:hover circle.core{stroke:#172e3a;stroke-width:2.5}.maptools{position:absolute;left:16px;top:16px;display:grid;gap:4px}.maptools button{border:1px solid #b9c9c9;background:#fffcf4e8;border-radius:5px;width:34px;height:34px;font-size:20px;cursor:pointer}.legend{position:absolute;bottom:14px;left:14px;background:#fffdf4eF;border:1px solid #d8ddd4;border-radius:8px;padding:11px 14px;font-size:12px;line-height:2;box-shadow:0 3px 18px #24414a18}.legend span{display:inline-block;width:9px;height:9px;border-radius:50%;margin-left:7px}.card{position:absolute;right:16px;bottom:16px;width:min(310px,calc(100% - 32px));background:#fffdf8f5;border:1px solid #d1ddd8;border-radius:10px;padding:16px;box-shadow:0 8px 24px #18313b33;max-height:65%;overflow:auto}.card h2{font-size:22px;margin:0 0 4px}.card .meta{color:#64767a;font-size:12px;margin-bottom:12px}.card p{font-size:13px;line-height:1.6;margin:7px 0}.card .place{border-top:1px solid #e2e8e2;padding-top:8px}.close{float:left;border:0;background:transparent;font-size:20px;cursor:pointer}.badge{display:inline-block;border:1px solid #dbe0d8;border-radius:20px;padding:2px 8px;font-size:11px}.below{max-width:1120px;margin:0 auto;padding:30px 24px 55px}h3{font-family:Georgia,serif;font-size:25px;font-weight:500;margin:25px 0 8px}.below p,.below li{line-height:1.8;font-size:14px}.below a{color:#28637b}.unmapped{display:flex;flex-wrap:wrap;gap:7px}.chip{background:#fff;border:1px solid #d8e1dd;border-radius:20px;padding:6px 11px;font-size:13px}.hint{font-size:12px;color:#62787d} @media(max-width:760px){main{display:flex;flex-direction:column;height:auto}.mapwrap{height:55vh;min-height:400px;order:0}.side{height:370px;order:1;border:0}.card{width:min(280px,80%);bottom:8px;right:8px}.legend{bottom:auto;top:12px;left:55px}header{padding:18px}}
</style></head><body><header><div><div class="eyebrow">אטלס מקראי · בראשית י׳</div><h1>לוח העמים — מפת צאצאי נֹחַ</h1><p>זיהויים גאוגרפיים מוצעים, לא מפת התיישבות מדויקת · יפת / חם / שם</p></div><div id="count" class="eyebrow"></div></header><main><aside class="side"><div class="controls"><input id="search" class="search" type="search" placeholder="חיפוש שם, אב או מקום…" aria-label="חיפוש"><div class="filters"><button class="filter active" data-branch="הכול">הכול</button><button class="filter" data-branch="יפת">יפת</button><button class="filter" data-branch="חם">חם</button><button class="filter" data-branch="שם">שם</button></div><label class="toggles"><input id="alts" type="checkbox" checked> הצג גם זיהויים חלופיים</label><div class="hint" style="margin-top:8px">לחיצה על שם או נקודה לפרטים · גלילה לזום · גרירה להזזה</div></div><div class="list" id="list"></div></aside><div class="mapwrap" id="mapwrap"><svg id="svg" viewBox="0 0 1200 730" preserveAspectRatio="xMidYMid meet" role="img" aria-label="מפה אינטראקטיבית של אגן הים התיכון, צפון אפריקה, המזרח הקרוב וחצי האי ערב"><rect width="1200" height="730" fill="#cce1e2"/><g id="viewport"><g class="grid" id="grid"></g><g class="land">__LAND__</g><g id="seas"></g><g id="markers"></g></g></svg><div class="maptools"><button id="plus" aria-label="הגדל">+</button><button id="minus" aria-label="הקטן">−</button><button id="reset" aria-label="אפס תצוגה" style="font-size:14px">⌂</button></div><div class="legend"><div><span style="background:var(--j)"></span>יפת — צפון ומערב</div><div><span style="background:var(--h)"></span>חם — דרום ולבנט</div><div><span style="background:var(--s)"></span>שם — מזרח וחצי האי ערב</div><div style="color:#667;font-size:11px">עיגול מקווקו = זיהוי חלופי</div></div><div class="card" id="card" hidden></div></div></main><section class="below"><h3>איך לקרוא את המפה</h3><p>המפה מתמקדת במרחב הידוע למחבר לוח העמים — אגן הים התיכון, צפון־מזרח אפריקה, אנטוליה, מסופוטמיה וחצי האי ערב — ולא מתיימרת לשייך את כל עמי העולם לשלושת הבנים. הנקודות מייצגות מרכזים משוערים או אזורים, ולא גבולות מדיניים או מסלולי נדידה. ״בן״ בפרק עשוי לציין עם, עיר, חבל ארץ או דמות; דירוג הביטחון הוא הערכה עריכתית גסה, לא קונצנזוס מחקרי. נקודות רבות חופפות: ניתן לבחור מהרשימה כדי לאתר אותן.</p><h3>ללא זיהוי גאוגרפי מבוסס</h3><p>השמות הבאים מופיעים בפרק, אך לא הוצבה להם נקודה משום שאין מקום שאפשר להציע באחריות סבירה:</p><div id="unmapped" class="unmapped"></div><h3>מקורות והערות מתודולוגיות</h3><ol><li><a href="https://www.mechon-mamre.org/i/t/t0110.htm" target="_blank" rel="noopener">בראשית י׳, נוסח המקרא — מכון ממרא</a>: שמות, סדר יוחסין ופסוקים. הנוסח המודבק בבקשה שימש לבדיקת הרשימה.</li><li><a href="https://www.thetorah.com/article/the-table-of-nations-the-geography-of-the-world-in-genesis-10" target="_blank" rel="noopener">TheTorah.com, “The Table of Nations: The Geography of the World in Genesis 10”</a>: מסגרת גאוגרפית, כפילויות ושאלת תרשיש.</li><li><a href="https://www.thetorah.com/article/decoding-the-table-of-nations-reading-it-as-a-map" target="_blank" rel="noopener">TheTorah.com, “Decoding the Table of Nations: Reading it as a Map”</a>: חלוקת המרחב לשלושת הענפים.</li><li><a href="https://bible.usccb.org/bible/genesis/10" target="_blank" rel="noopener">USCCB, Genesis 10, הערות לפסוקים</a>: למשל כוש, פוט ונמרוד.</li><li><a href="https://www.esv.org/resources/esv-global-study-bible/map-01-03/" target="_blank" rel="noopener">ESV Global Study Bible, Table of Nations map</a>: נקודת השוואה למיקום קבוצות מרכזיות.</li><li><a href="https://github.com/datasets/geo-countries" target="_blank" rel="noopener">Natural Earth / datasets geo-countries</a>: קווי חוף וגבולות מודרניים כרקע בלבד (Public Domain). </li></ol><p class="hint">החלופות אינן בהכרח שקולות בסבירותן. שמות חוזרים (שבא, חוילה) מופיעים פעמיים, בענפים הנפרדים. אשור בפס׳ יא אינו נספר שוב כבן נפרד; הערים של נמרוד אינן צאצאים; פלשתים מוצגים בנפרד כעם הנזכר בפס׳ יד. המפה פועלת מקומית ללא חיבור רשת.</p></section><script>
const data=__DATA__, colors={'יפת':'#526f9e','חם':'#bd7950','שם':'#5c927f'};const W=1200,H=730;let branch='הכול',query='',selected=null,scale=1,tx=0,ty=0;const $=s=>document.querySelector(s), svg=$('#svg'),vp=$('#viewport');function xy(lon,lat){return [(lon+12)/80*W,(49-lat)/53*H]}function esc(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}function visible(d){return(branch==='הכול'||d.branch===branch)&&(!query||[d.name,d.parent,...d.locations.map(l=>l.label)].join(' ').includes(query))}function updateTransform(){vp.setAttribute('transform',`translate(${tx} ${ty}) scale(${scale})`)}function zoom(f,x=W/2,y=H/2){let n=Math.max(1,Math.min(8,scale*f)),r=n/scale;tx=x-(x-tx)*r;ty=y-(y-ty)*r;scale=n;updateTransform()}function focus(l){let [x,y]=xy(l.lon,l.lat);scale=2.25;tx=W/2-x*scale;ty=H/2-y*scale;updateTransform()}function select(i,move=false){selected=i;let d=data[i];if(move&&d.locations.length)focus(d.locations[0]);$('#card').hidden=false;$('#card').innerHTML=`<button class="close" aria-label="סגור" onclick="document.querySelector('#card').hidden=true">×</button><h2 style="color:${colors[d.branch]}">${esc(d.name)}</h2><div class="meta">בני ${esc(d.branch)} · אב/קבוצה: ${esc(d.parent)} · בראשית י׳:${esc(d.verse)}</div><span class="badge">רמת זיהוי: ${esc(d.confidence)}</span>${d.locations.length?d.locations.map((l,j)=>`<p class="place"><b>${j?'חלופה':'מיקום מוצע'}:</b> ${esc(l.label)}${l.lon>68?' · מחוץ לגבולות המפה':''}</p>`).join(''):'<p>לא הוצב סימון: אין זיהוי גאוגרפי מבוסס.</p>'}${d.note?`<p>${esc(d.note)}</p>`:''}<p class="hint">מקורות כלליים והסתייגויות — בתחתית העמוד</p>`;renderList();renderMarkers()}function renderList(){let matches=data.map((d,i)=>[d,i]).filter(([d])=>visible(d));$('#count').textContent=`${matches.length} רשומות · ${matches.filter(([d])=>d.locations.length).length} ממופות`;$('#list').innerHTML=matches.map(([d,i])=>`<button class="row ${selected===i?'selected':''}" data-i="${i}"><span class="swatch" style="background:${colors[d.branch]}"></span><strong>${esc(d.name)}</strong><small>${esc(d.parent)} · פס׳ ${esc(d.verse)} ${d.locations.length?'':'· ללא מיקום'}</small></button>`).join('');$('#list').querySelectorAll('.row').forEach(el=>el.onclick=()=>select(+el.dataset.i,true))}function renderMarkers(){let out=[];data.forEach((d,i)=>{if(!visible(d))return;d.locations.forEach((l,j)=>{if(j&&!$('#alts').checked)return;if(l.lon< -12||l.lon>68||l.lat< -4||l.lat>49)return;let [x,y]=xy(l.lon,l.lat),c=colors[d.branch];out.push(`<g class="pin ${j?'alt':''}" data-i="${i}" transform="translate(${x.toFixed(1)} ${y.toFixed(1)})"><title>${esc(d.name)} — ${esc(l.label)}</title>${selected===i?`<circle class="halo" r="12" stroke="${c}"/>`:''}<circle class="core" r="${selected===i?7:5}" fill="${c}"/></g>`)})});$('#markers').innerHTML=out.join('');$('#markers').querySelectorAll('.pin').forEach(el=>el.onclick=e=>{e.stopPropagation();select(+el.dataset.i)})}const grid=$('#grid');for(let lon=-10;lon<=60;lon+=10){let [x]=xy(lon,0);grid.innerHTML+=`<line x1="${x}" x2="${x}" y1="0" y2="730"/>`}for(let lat=0;lat<=40;lat+=10){let [,y]=xy(0,lat);grid.innerHTML+=`<line x1="0" x2="1200" y1="${y}" y2="${y}"/>`}$('#seas').innerHTML=[[18,36,'הים התיכון'],[40,22,'ים סוף'],[50,27,'המפרץ הפרסי'],[31,44,'הים השחור']].map(([a,b,t])=>{let [x,y]=xy(a,b);return `<text class="sea-label" x="${x}" y="${y}" text-anchor="middle">${t}</text>`}).join('');document.querySelectorAll('.filter').forEach(b=>b.onclick=()=>{branch=b.dataset.branch;document.querySelectorAll('.filter').forEach(x=>x.classList.toggle('active',x===b));renderList();renderMarkers()});$('#search').oninput=e=>{query=e.target.value.trim();renderList();renderMarkers()};$('#alts').onchange=renderMarkers;$('#plus').onclick=()=>zoom(1.5);$('#minus').onclick=()=>zoom(1/1.5);$('#reset').onclick=()=>{scale=1;tx=ty=0;updateTransform()};const wrap=$('#mapwrap');wrap.addEventListener('wheel',e=>{e.preventDefault();let rect=svg.getBoundingClientRect(),r=Math.min(rect.width/W,rect.height/H),ox=(rect.width-W*r)/2,oy=(rect.height-H*r)/2;zoom(e.deltaY<0?1.2:1/1.2,(e.clientX-rect.left-ox)/r,(e.clientY-rect.top-oy)/r)},{passive:false});let last=null;wrap.addEventListener('pointerdown',e=>{if(e.target.closest('button,.card,.legend,.pin'))return;last=[e.clientX,e.clientY];wrap.setPointerCapture(e.pointerId)});wrap.addEventListener('pointermove',e=>{if(!last)return;let rect=svg.getBoundingClientRect(),r=Math.min(rect.width/W,rect.height/H);tx+=(e.clientX-last[0])/r;ty+=(e.clientY-last[1])/r;last=[e.clientX,e.clientY];updateTransform()});wrap.addEventListener('pointerup',()=>last=null);$('#unmapped').innerHTML=data.filter(d=>!d.locations.length).map(d=>`<span class="chip" style="border-right:3px solid ${colors[d.branch]}">${esc(d.name)} <small>(${esc(d.branch)})</small></span>`).join('');renderList();renderMarkers();
</script></body></html>'''
page=page.replace('__LAND__',land).replace('__DATA__',jsdata)
Path('/home/user/noah_descendants_map.html').write_text(page)
