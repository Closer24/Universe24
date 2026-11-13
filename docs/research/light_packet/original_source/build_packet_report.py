"""Render the saved experiment; this script does not advance any states."""
from pathlib import Path
import base64
import hashlib
import io
import json
import zipfile

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.lines import Line2D
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'runs/light-packet-clicks-v2'
OUT=ROOT/'light_packet_results'
OUT.mkdir(exist_ok=True)
NAMES=('flat','fast','step')
OBS={n:json.loads((BASE/n/'observations.json').read_text()) for n in NAMES}
AGG=json.loads((BASE/'aggregate.json').read_text())
CHECK=json.loads((BASE/'post_validation.json').read_text())
WIDE=json.loads((BASE/'wide_packet_exploratory/summary.json').read_text())
TITLES=['Uniform background · q = 1','Uniform background · q = 2','Optical step · q = 1 → 2']
COLORS=['#2369ba','#a23d86','#128777']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,
                     'axes.spines.right':False,'axes.titleweight':'bold','figure.facecolor':'#f7f9fc',
                     'savefig.facecolor':'#f7f9fc'})
times=np.asarray(OBS['flat']['times']);x=np.arange(41)
E={n:np.array(o['energy'])/sum(o['energy'][0]) for n,o in OBS.items()}
K={n:np.asarray(o['clicks_per_node_per_tick']).reshape(12,2,41).sum(1) for n,o in OBS.items()}

fig=plt.figure(figsize=(17,10.6))
grid=fig.add_gridspec(2,4,left=.065,right=.95,top=.85,bottom=.13,
                      width_ratios=[1,1,1,.045],height_ratios=[1.2,1],wspace=.16,hspace=.26)
fig.text(.065,.956,'A moving pulse. The same raw click map.',fontsize=25,weight='bold',color='#142a43')
fig.text(.065,.913,'Universe24 Engine · 18-channel research candidate · 41³ sites · 24 ticks · same tensor in all runs',fontsize=12,color='#4d6175')
clickcmap=ListedColormap(['#f1eff5','#c9beda','#a38bbc','#7b519a','#3f205f'])
clicknorm=BoundaryNorm(np.arange(-.5,5.5),5)
top_axes=[];bottom_axes=[]
for j,n in enumerate(NAMES):
    o=OBS[n];ax=fig.add_subplot(grid[0,j]);top_axes.append(ax)
    im=ax.pcolormesh(np.arange(-.5,41.5),np.r_[times-1/3,times[-1]+1/3],E[n],
                     cmap='magma',vmin=0,vmax=.36,shading='flat')
    ax.plot(o['centroids'],times,color='white',lw=1.8)
    c0=o['centroids'][0]
    if n=='step':
        arrival=14-c0
        target=np.where(times<=arrival,c0+times,14+2*(times-arrival))
        ax.axvline(14,color='#64e8c3',ls=':',lw=1.5)
    else: target=c0+times*(1 if n=='flat' else 2)
    ax.plot(target,times,color='#59def4',ls='--',lw=1.5)
    ax.set(xlim=(-.5,40.5),ylim=(0,8),xticks=[0,10,20,30,40],yticks=[0,2,4,6,8])
    ax.set_title(TITLES[j],fontsize=13,pad=12)
    if j==0:ax.set_ylabel('Field energy proxy\nCoordinate time t = tick / 3',labelpad=12)
    else:ax.set_yticklabels([])
    ax=fig.add_subplot(grid[1,j]);bottom_axes.append(ax)
    cm=ax.pcolormesh(np.arange(-.5,41.5),np.arange(13)*2/3,K[n],cmap=clickcmap,norm=clicknorm,shading='flat')
    if n=='flat':
        ax.plot(18+times,times,ls='--',color='#d34a24',lw=1.6)
        ax.plot(2-times,times,ls='--',color='#d34a24',lw=1.6)
        wrapped=times>=2
        ax.plot(43-times[wrapped],times[wrapped],ls='--',color='#d34a24',lw=1.6)
        ax.scatter([30],[14/3],s=66,facecolors='none',edgecolors='#d34a24',lw=1.8,zorder=5)
        ax.annotate('x = 30: first click',xy=(30,14/3),xytext=(20.2,6.45),color='#ffd6ad',fontsize=9,
                    arrowprops={'arrowstyle':'-','color':'#ffd6ad'})
    ax.set(xlim=(-.5,40.5),ylim=(0,8),xlabel='Coordinate x',xticks=[0,10,20,30,40],yticks=[0,2,4,6,8])
    if j==0:ax.set_ylabel('Raw canonical clicks\nCoordinate time t = tick / 3',labelpad=12)
    else:ax.set_yticklabels([])
    ax.text(.5,1.025,'2,649,256 clicks · all C0',transform=ax.transAxes,ha='center',fontsize=11,color='#493260')
cb=fig.colorbar(im,cax=fig.add_subplot(grid[0,3]));cb.set_label('u(x,t) / Σ u(x,0)',labelpad=8)
cb=fig.colorbar(cm,cax=fig.add_subplot(grid[1,3]),ticks=range(5));cb.set_label('Clicks / site / two ticks',labelpad=8)
legend=[Line2D([0],[0],color='#51606c',lw=2,label='Measured energy centroid'),
        Line2D([0],[0],color='#27a8c3',ls='--',lw=2,label='Continuum target ray'),
        Line2D([0],[0],color='#d34a24',ls='--',lw=2,label='Flat target cone from full initial support')]
fig.legend(handles=legend,loc='lower left',bbox_to_anchor=(.061,.058),ncol=3,frameon=False,fontsize=10)
fig.text(.065,.027,'Static prescribed geometry; coordinate units. Raw clicks are arithmetic events, not photon detections. Periodic boundaries.',fontsize=10,color='#526579')
PNG=OUT/'Universe24_light_clicks.png';fig.savefig(PNG,dpi=130);plt.close(fig)

# Actual complete-field snapshots, one frame per two Engine ticks.
frames=[]
for frame,t in enumerate(times):
    fig,axs=plt.subplots(2,3,figsize=(13.8,5.8),gridspec_kw={'height_ratios':[3,1]},sharex=True)
    fig.subplots_adjust(left=.065,right=.975,top=.78,bottom=.13,hspace=.18,wspace=.16)
    fig.text(.065,.92,'Pulse energy and unfiltered arithmetic clicks',fontsize=20,weight='bold',color='#142a43')
    fig.text(.065,.854,f'Coordinate time {t:4.2f}  ·  Engine tick {2*frame:02d} / 24  ·  exact saved states',fontsize=12,color='#526579')
    for j,n in enumerate(NAMES):
        ax=axs[0,j];ax.plot(x,E[n][frame],color=COLORS[j],lw=2)
        ax.fill_between(x,E[n][frame],color=COLORS[j],alpha=.15)
        ax.axvline(OBS[n]['centroids'][frame],color=COLORS[j],ls='--',lw=1)
        if n=='step':ax.axvline(14,color='#748b94',ls=':',lw=1)
        ax.set(ylim=(0,.37),xlim=(-.5,40.5),title=TITLES[j],yticks=[0,.1,.2,.3])
        ax.grid(axis='y',alpha=.15)
        ax.text(.97,.91,f"centroid {OBS[n]['centroids'][frame]:.2f}",ha='right',transform=ax.transAxes,color=COLORS[j],fontsize=10)
        counts=np.zeros(41) if frame==0 else K[n][frame-1]
        axs[1,j].bar(x,counts,color='#69418c',width=.94)
        axs[1,j].set(ylim=(0,4.5),xlabel='Coordinate x',yticks=[0,2,4])
        if j:
            ax.set_yticklabels([]);axs[1,j].set_yticklabels([])
    axs[0,0].set_ylabel('Field energy proxy / initial total')
    axs[1,0].set_ylabel('Clicks / site\nlast 2 ticks')
    fig.text(.065,.025,'Same tensor in all panels. The wave moves differently; the count/location/class maps are identical.',fontsize=10,color='#526579')
    b=io.BytesIO();fig.savefig(b,format='png',dpi=100);plt.close(fig)
    frames.append(Image.open(io.BytesIO(b.getvalue())).convert('RGB').quantize(colors=128))
GIF=OUT/'Universe24_light_clicks.gif'
frames[0].save(GIF,save_all=True,append_images=frames[1:],duration=[1000]+[650]*11+[2000],loop=0,optimize=True,disposal=2)

def embed(path,mime):return f'data:{mime};base64,'+base64.b64encode(path.read_bytes()).decode()
rows=''.join(f'<tr><td>{label}</td><td>{target}</td><td>{OBS[n]["summary"][key]:.6f}</td><td>{OBS[n]["summary"]["clicks"]:,}</td><td>C0 בלבד</td></tr>'
    for n,label,target,key in [('flat','רקע אחיד q=1','1','coordinate_centroid_speed_fit'),
                             ('fast','רקע אחיד q=2','2','coordinate_centroid_speed_fit'),
                             ('step','מדרגה q=1 → 2','2 באזור השני','late_coordinate_speed_fit')])
html='''<!doctype html><html lang="he" dir="rtl"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Universe24 — ניסוי התקדמות אור וקליקים</title>
<style>body{margin:0;background:#f3f6fa;color:#1d3045;font:17px/1.8 Arial,sans-serif}main{max-width:1120px;margin:auto;padding:48px 28px 70px}h1{font-size:38px;line-height:1.25;margin:12px 0 22px}h2{font-size:25px;margin:42px 0 12px}p{max-width:1000px}a{color:#2166aa}img{width:100%;height:auto;border-radius:12px;background:white}figure{margin:26px 0}figcaption{font-size:14px;color:#53657b;margin-top:8px}table{border-collapse:collapse;width:100%;background:white;margin:24px 0;font-variant-numeric:tabular-nums}th,td{padding:12px 15px;border-bottom:1px solid #dfe6ef;text-align:right}th{background:#e6eef7}pre{direction:ltr;text-align:left;white-space:pre-wrap;background:#e9eff5;padding:20px;border-radius:8px;font-size:14px;line-height:1.7;overflow-wrap:anywhere}.kicker{font-size:13px;letter-spacing:1px;color:#52687b}.callout{border-right:4px solid #955025;padding:14px 22px;background:#fff5e9;border-radius:8px}.lead{font-size:21px}.muted{color:#526579;font-size:15px}code{direction:ltr;unicode-bidi:embed}details{background:#fff;padding:18px 24px;margin:18px 0;border-radius:10px}summary{font-weight:bold;cursor:pointer}li{margin:8px 0}.cards{display:flex;gap:14px;flex-wrap:wrap}.card{flex:1;min-width:200px;background:white;padding:20px;border-radius:12px}.big{font-size:28px;font-weight:bold;display:block;color:#245d9b}@media(max-width:650px){main{padding:26px 16px}h1{font-size:29px}th,td{padding:8px;font-size:14px}}</style>
<main><div class="kicker">UNIVERSE24 · ניסוי מספרי משוחזר · 13 בנובמבר 2026</div>
<h1>החבילה מתקדמת; הקליקים אינם מפת גילוי של האור</h1>
<p class="lead">המועמד בן 18 הערוצים מייצר חבילת שדה נעה, וקצב תנועתה משתנה עם הרקע האופטי. אבל מיקומי הקליקים, זמניהם וסוגיהם היו זהים בשלושת הרקעים — למרות תנועת האנרגיה השונה.</p>
<div class="callout"><strong>תחום המסקנה:</strong> זהו ניסוי במועמד חדש לשדה מקסוול קלאסי בתוך כללי Universe24, עם גאומטריה קבועה מראש. הוא אינו הוכחה שכבר קיים במאגר אור פיזיקלי מלא, פוטונים, גלאי או פתרון מצומד של משוואות איינשטיין.</div>
<div class="cards"><div class="card"><span class="big">68,921</span>צמתים בכל ריצה עיקרית: 41³</div><div class="card"><span class="big">24</span>טיקים של מנוע המקור; 12 צעדים פיזיקליים מפוענחים</div><div class="card"><span class="big">2,649,256</span>קליקים בכל רקע; כולם C0</div></div>
<figure><img src="__PNG__" alt="מפות מרחב זמן של אנרגיית השדה ושל הקליקים בשלושה רקעים"><figcaption>למעלה: חבילת השדה נעה באופן שונה בכל רקע. למטה: מספר הקליקים בכל צומת בשני טיקים עוקבים — שלוש המפות זהות בדיוק. הכתום מציג את חרוט היעד ברקע השטוח, מתחום התמיכה המלא של מצב ההתחלה.</figcaption></figure>
<h2>מה הרצתי בפועל</h2>
<p>הרצתי את <code>Engine.step</code> המקורי על מערכים תלת־ממדיים מלאים. הטנסור זהה בכל הריצות: 18 ערוצים, 162 איברים פולינומיים ממעלה לכל היותר 2, וקישוריות של שכני פאה. רק מצבי ההתחלה והרקע השתנו. השדה אחיד בכיווני y,z ומקומי בכיוון x; זאת חבילה מישורית, לא קרן ממוקדת בשלושה ממדים.</p>
<p>בתחילה D מכוון לאורך y ו־B לאורך z, והחבילה מתקדמת בעיקר בכיוון +x. מעטפת D נבנתה ממקדמי בינום מסדר 12. B וההיסטוריה a הוכנו בהתאם לפיצול הזמני, ולכן הכנת B תלויה גם ברקע. תנאי השפה מחזוריים. מצב המקור נלקח מההתחייבות המקובעת <a href="https://github.com/Closer24/Universe24/tree/e582960f6c9d2d134d3d6b28c08494e8bfafa86a">e582960</a>; לא נערך שינוי ב־GitHub.</p>
<pre>C = diag(1, q, q)
flat: q = 1
fast: q = 2
step: q = 1 for x &lt; 14, q = 2 for x ≥ 14

h = 1;  t = Engine tick / 3;  Δt per complete field update = 2/3
g_target = Ω² diag(-1, 1/q², 1/q, 1/q)
Target coordinate null speed in x: |dx/dt| = q</pre>
<p class="muted">זהו כיול זמן ואורך של המועמד, לא מדידה באמצעות שעון וסרגל פנימיים שנגזרו מהמאגר. מהירות קואורדינטית 2 ברקע השני אינה כשלעצמה מהירות מקומית כפולה ממהירות האור: גם רכיב המרחק במטריקת היעד משתנה.</p>
<h2>איך החבילה התקדמה</h2>
<table><thead><tr><th>ריצה</th><th>מהירות קואורדינטית רציפה צפויה</th><th>מהירות מרכז אנרגיה נמדדת</th><th>סך קליקים</th><th>מחלקות</th></tr></thead><tbody>__ROWS__</tbody></table>
<p>המהירויות בשני הרקעים האחידים הן שיפועי התאמה למרכז האנרגיה לאורך כל 13 התצלומים. במדרגה מוצג השיפוע בחמשת התצלומים האחרונים; השיפוע לאורך הריצה כולה הוא 1.438734. מרכז החבילה השטוחה עבר מ־9.8473 ל־17.2721 בזמן 8; ברקע השני מ־9.7014 ל־24.8359; ובמדרגה מ־9.8539 ל־21.3544. במדרגה החבילה גם התרחבה: סטיית התקן המרחבית גדלה מ־1.2622 ל־3.2659.</p>
<p>הפער ממהירות היעד נשאר גלוי: ברקע השטוח מדובר בכ־7.2%. בניסוי המשך חוקר, עם מעטפת רחבה יותר (בינום מסדר 32, תיבה 61³ ו־12 טיקים), נמדדה מהירות 0.972049. זה מתאים להפחתת השפעת הדיספרסיה של הסריג באורכי גל ארוכים; זו אינה סדרת עידון מסודרת באותו תחום פיזיקלי, ואינה הוכחת התכנסות לבדה.</p>
<figure><img src="__GIF__" alt="אנימציה מתוך המצבים המדויקים שנשמרו"><figcaption>כל פריים הוא מצב שנשמר אחרי שני טיקים אמיתיים של המנוע. הקו המקווקו מציין את מרכז האנרגיה; העמודות למטה סופרות קליקים בשני הטיקים האחרונים.</figcaption></figure>
<h2>מה הקליקים אומרים — ומה הם עדיין אינם אומרים</h2>
<p>השתמשתי בהגדרה הקנונית של המאגר, ללא סף עוצמה או סינון:</p>
<pre>(ell, r_next) = divmod(2u + r, 6)
a_next = b;  b_next = ell - a
click ⇔ ell ≠ 0 AND (a_next,b_next,r_next) ≠ (a,b,r)
δ = (r_next - r) mod 6
C0: δ ∈ {0,3};  C1: δ ∈ {1,2};  C2: δ ∈ {4,5}</pre>
<p>במגזר שהוכן כאן השארית נשמרת בכל צעד, לכן δ=0 וכל הקליקים C0. היעדר C1 ו־C2 אינו היעדר התקדמות: החבילה נעה גם כך. ערוצי הגאומטריה הקבועה אינם מקליקים, מפני שהשלשה שלהם אינה משתנה.</p>
<p><strong>המפות הזהות הן של עצם הקליק, מיקומו, זמנו ומחלקתו.</strong> גודל המנה ell שונה בין הרקעים, ולכן רשומות הקליק המלאות אינן זהות. המידע הגלי נשאר בערכי השדות והמנות; ספירת קליקים לבדה אינה מציגה את חבילת האנרגיה.</p>
<ul><li>בבקרת הכפלת המשרעת, אנרגיית השדה גדלה פי 4 והמנות גדלו פי 2, אבל מספר הקליקים נשאר 16,848 ומפת מיקומיהם ומחלקותיהם לא השתנתה.</li><li>בשדה ריק נמדדו 0 קליקים במשך 6 טיקים, והרקע נשאר קבוע.</li><li>בבקרת דיוק התחלתי נמוך, Q=3, הופיעו 7,371 קליקי C0, עוד 4,374 מסוג C1 ועוד 4,941 מסוג C2. באותה ריצה השאריות השתנו וההתאמה המדויקת לעדכון מקסוול שהוכן נשברה. לכן מחלקות אלה מתארות כאן את חשבון השאריות; הניסוי אינו מעניק להן פירוש של פוטונים.</li></ul>
<p class="muted">בקרות המשרעת והדיוק רצו בתיבה קטנה של 9³. אין להשתמש במהירות או בצורת החבילה בהן להשוואת התקדמות: גלישת השדה דרך השפה המחזורית משמעותית, במיוחד בבקרת הדיוק. הספירות הכוללות בריצות העיקריות כוללות את כל 41² הצמתים השקולים בכל מישור; אלה אינם מיליוני ניסויי גילוי בלתי תלויים.</p>
<h2>בדיקת חרוט האור חשפה בעיה ממשית בזיהוי הקליקים</h2>
<p>בחנתי את הרקע השטוח מול התמיכה של <strong>שתי ההיסטוריות המלאות</strong>, a וגם b. התמיכה ההתחלתית של השדה היא x=2…18. לכן נקודה x=30 מרוחקת לפחות 12 תאים, גם כשמביאים בחשבון את המחזוריות. בחרוט היעד, עם c=1, השפעה מהתמיכה הזאת לא אמורה להגיע לפני t=12.</p>
<div class="callout">ב־x=30 הופיע קליק כבר בטיק 14, כלומר <strong>t=4.6667</strong>. באותו רגע חלק האנרגיה במישור הזה היה רק <strong>2.00×10⁻²¹</strong> מסך אנרגיית השדה. הבדל זה נובע מזנב זעיר של העדכון הבדיד ומכך שהגדרת הקליק אינה דורשת אנרגיה מינימלית.</div>
<p>כל הריצות כיבדו את חרוט התלות החישובי של המנוע — לכל היותר קשת שכנות אחת בטיק. אבל החרוט הזה רחב מחרוט האור הרציף המיועד בכיול הזמן שנבחר. בריצה השטוחה חלק האנרגיה הכולל המרבי שנמדד מחוץ לחרוט היעד היה 2.153×10⁻⁷. הוא זעיר, אך אינו אפס.</p>
<p>לכן אין כאן תוצאה של גילוי אור על־אורי בטבע. זו מגבלה של המועמד על סריג סופי ושל הניסיון לפרש כל קליק חשבוני כאירוע גילוי פיזיקלי. גם אם קירוב השדה משתפר באורכי גל ארוכים, אסור להחליף בדיעבד את הגדרת הקליק בסף נוח כדי לטעון שכבר התקבל חרוט אור מדויק.</p>
<h2>מה הניסוי קובע לגבי המודל</h2>
<p>יש כאן מנגנון בדיד שמקדם הפרעה רוחבית כמו שדה מקסוול בקירוב של אורכי גל ארוכים, ושמגיב למקדמי הרקע האופטי. הניסוי אינו מצדיק עדיין את הטענה <strong>״קליק הוא פוטון״</strong>, או שכל הקליקים נעים על חרוט האור של איינשטיין.</p>
<p>כדי לקשור את התיאור לאור פיזיקלי במרחב־הזמן של המודל, עדיין צריך לגזור מדידה באמצעות גלאי ושעון פנימיים, לקשור את הקליקים להעברת אנרגיה בתהליך גילוי, ולבדוק סיבתיות והתכנסות בלי להשמיט אירועים. בנוסף חסרות גאומטריה דינמית ומשוואות שדה מצומדות: C בניסוי הזה אינו מגיב לאנרגיית האור. פירוש קוונטי מצריך יותר מכך, כולל סטטיסטיקת גילוי וכימות אנרגיה שלא נבדקו כאן.</p>
<details><summary>פרטי אימות וגבולות מספריים</summary>
<ul><li>כל צעד הושווה לאורקל אלגברי עצמאי של ההגבלה המישורית; האורקל לא שימש לקידום המצבים.</li><li>בכל ריצה נבדקו היפוך של כל צעד וחזרה מלאה למצב ההתחלה.</li><li>העקבות השמורים של שלוש הריצות העיקריות נקראו שוב, הורחבו למערכים המלאים, וכל המעברים שוחזרו באמצעות המנוע. גם כל רשומות הקליקים נבדקו בפענוח סקלרי עצמאי, והצעד הראשון בכל תיבה הושווה למפענח המערכתי הקנוני.</li><li>כל a,b,r נשמרו בדחיסה מישורית חסרת אובדן. האחידות הרוחבית נבדקה מול כל רכיבי המערכים המלאים בכל מצב. אין חיתוך, סף או השמטת רשומות.</li><li>השדה הוכן בסקלה Q=3²⁵, והערכים המאוחסנים הגיעו ל־53 סיביות. קידום המצב הוא בשלמים מדויקים; חלוקה ב־Q והמרה למספרים ממשיים משמשות רק לתצפית. Q קבוע אינו מעניק הוכחה לתקפות המגזר המדויק במשך זמן בלתי מוגבל.</li><li>נשמר בדיוק ספר האנרגיה המתוקן J=3Σ(DᵀCD+BᵀCB)−ΣDᵀC R_C(B). הצבעים והמרכזים משתמשים באומדן u=½(DᵀCD+BᵀCB); אין טענה שאומדן זה עצמו נשמר בדיוק.</li><li>חלק האנרגיה המרבי בשתי השכבות הקיצוניות מכל צד היה כ־0.000265% ברקע השטוח, 0.0396% ברקע q=2, ו־0.000242% במדרגה. השפה המחזורית נכללה במפורש בחישובי המרחק.</li><li>האנימציה והתרשימים הופקו מן התצלומים שנשמרו, ללא הרצת מודל חלופי.</li></ul></details>
<details><summary>הטנסור והקשר למשוואות השדה</summary>
<p>R_C הוא curl מרכזי לא מנורמל של CV, עם הפרשים בין שכני הפאה. X,Y הם שתי קבוצות בתוך 18 הערוצים הנספרים; ששת הערוצים הנוספים מחזיקים את C הסימטרי. בכל טיק נשמרות גם שלשות a,b,r של כל הערוצים.</p>
<pre>u_DX = 6 D_Y + R_C(B_Y)
u_BX = 6 B_Y + R_C(D_Y)
u_DY = 6 D_X - R_C(B_X)
u_BY = 6 B_X - R_C(D_X)
u_C  = 6 C

On the prepared sector, one complete update (two ticks):
B_new = B - R_C(D)/3
D_new = D + R_C(B_new)/3

Long-wave target: ∂t D = curl(CB); ∂t B = -curl(CD)
Tensor SHA-256: __TENSOR__</pre>
<p>מטריקת היעד נקבעת כאן עד כדי גורם קונפורמי Ω. הניסוי אינו מזהה גורם זה באמצעות סרגלים או שעונים פנימיים.</p></details>
<p class="muted">חבילת השחזור המצורפת כוללת את קוד הניסוי, רכיבי מנוע המקור שנקראו, הטנסור, כל המצבים והקליקים בדחיסה חסרת אובדן, פרוטוקולים, תוצאות האימות ותרשימים. אין צורך בשירות חיצוני כדי לקרוא את הדוח הזה.</p>
</main></html>'''
html=html.replace('__PNG__',embed(PNG,'image/png')).replace('__GIF__',embed(GIF,'image/gif')).replace('__ROWS__',rows).replace('__TENSOR__',AGG['tensor_hash'])
HTML=OUT/'Universe24_light_clicks_report_he.html';HTML.write_text(html)

readme='''Universe24 light-packet / canonical-click experiment
==================================================
New research candidate, not an accepted coupled Einstein model.
Source pin: e582960f6c9d2d134d3d6b28c08494e8bfafa86a
Source: https://github.com/Closer24/Universe24

The package includes the unchanged Python modules used from the pinned source,
not a complete checkout. source_manifest.json records their hashes.

Python dependencies: numpy, sympy; matplotlib and Pillow for rendering.
Work from the extracted archive root. No network is needed with these installed.

Replay and verify the included saved main traces and canonical click records:
  PYTHONPATH=repo_review python light_derivation/verify_packet_evidence.py

Repeat all main cases and controls into a NEW output directory:
  PYTHONPATH=repo_review python light_derivation/packet_click_experiment.py --out runs/reproduced
  PYTHONPATH=repo_review python light_derivation/verify_packet_evidence.py --base runs/reproduced

Repeat the exploratory broad packet (new output directory required):
  PYTHONPATH=repo_review:light_derivation python -c "from pathlib import Path; from packet_click_experiment import run_case; run_case(Path('runs/wide_reproduced'), 'wide_packet_exploratory', L=61, H=12, order=32, center=20)"

Render the included evidence again:
  python light_derivation/build_packet_report.py

Trace encoding: each row stores a,b,r with shape (18,L). Repeat each x column
L² times in y,z order to recover the actual full cubic state. This symmetry was
verified on every array value at each time; the Engine was run on FULL arrays.
Click encoding: [x, channel, class, exact quotient], multiplicity L² for every
line. No filtering or amplitude threshold. Class 0/1/2 means C0/C1/C2.

The flat/fast/step count, location, class, and first-arrival maps are identical;
their quotient values and field-energy trajectories are not.
Raw arithmetic events must not be equated with photon detections.
The intended metric cone is violated by tiny finite-grid tails; the wider
computational dependence cone is respected. See the report for all limitations.

The packet script hash is also recorded in aggregate.json. The optional wide
packet was run after the primary cases and is exploratory, not preregistered
or a matched fixed-domain mesh-refinement study.
'''
(OUT/'README.txt').write_text(readme)
sources=[p for p in (ROOT/'repo_review/universe24').rglob('*.py') if 'tests' not in p.parts]
manifest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(sources)}
(OUT/'source_manifest.json').write_text(json.dumps({'source_pin':AGG['source_pin'],'files':manifest},indent=2))
archive=OUT/'Universe24_light_clicks_reproducible.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    files=list(BASE.rglob('*'))+sources
    files += [ROOT/'light_derivation'/n for n in ('packet_click_experiment.py','verify_packet_evidence.py','light_tensor_audit.py','build_packet_report.py')]
    files += [PNG,GIF,HTML,OUT/'README.txt',OUT/'source_manifest.json']
    for p in files:
        if p.is_file():z.write(p,str(p.relative_to(ROOT)))
    z.writestr('README.txt',readme)
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
assert AGG['script_sha256']==hashlib.sha256((ROOT/'light_derivation/packet_click_experiment.py').read_bytes()).hexdigest()
print(json.dumps({'files':[{'name':p.name,'bytes':p.stat().st_size} for p in (PNG,GIF,HTML,archive)],
                  'source_modules':len(sources),'script_hash_verified':True,'zip_integrity':'passed'},indent=2))
