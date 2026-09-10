# Universe24 — סימולטור אירועים תלת־ממדי

מקור האמת: [Closer24/Universe24](https://github.com/Closer24/Universe24), ענף `main`.
שם חבילת Python נשאר `event_universe`.

**מתחילים כאן:** [AGENTS.md](AGENTS.md) — הוראות משותפות, מקור האמת ומפת הכללים.
זהו פרויקט אחד; הקוד הפעיל נמצא רק ב־`src/event_universe/`.

חבילת Python מסודרת למחקר של שדה ואירועים מקומיים. המנוע, החוקים המועמדים,
המדידות והבדיקות מופרדים. גרסת המודל היא `scalar-field-v10-contact`.
החבילה משמרת את חוק השדה ואת חוק הפנייה של הגרסה שנבדקה לפני הארגון מחדש.

להבנת הרעיון לפני הפרטים הטכניים, מתחילים ב־`POSTULATES_HE.md`. הוא מסביר
בעברית פשוטה מה מחייב, מהו רק חוק מועמד ומה עדיין שאלה פתוחה.

## התקנה והרצה

נדרש Python 3.11 ומעלה. מתוך תיקיית הפרויקט:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[render,dev]'
python -m event_universe --scenario contact --output artifacts/contact
```

ב־Windows מפעילים את הסביבה באמצעות `.venv\Scripts\activate`.
לכל הרצה דרך כלי ההרצה נוצרים:

| קובץ | תוכן |
| --- | --- |
| `run.html` | HTML עצמאי עם ההנפשה, המישור והפרמטרים |
| `run.gif` | ההנפשה שמוטמעת ב־HTML |
| `run.json` | מצב סיום, תנאי התחלה, גרסת קוד ותוצאות בדיקות ההרצה |
| `events.jsonl` | אירועי תנועה, חילופי תנע ומעברים חסומים, הנכתבים בהדרגה |

תרחישים נוספים:

```bash
python -m event_universe --scenario turning --output artifacts/turning
python -m event_universe --scenario contact --view-3d --output artifacts/contact-3d
python -m event_universe --scenario stationary --frame-stride 4 --output artifacts/stationary
```

`--ticks` משנה את משך ההרצה. `--plane XY|XZ|YZ` ו־`--slice` בוחרים חתך לצפייה;
בחירת החתך אינה משנה את הפיזיקה התלת־ממדית.
`--frame-stride` מדלל תמונות בלבד ואינו מדלג על צעדים פיזיקליים.

תצוגת תלת־ממד משופרת באיכות 1500×1275 היא ברירת המחדל בכל הרצה, גם בדוחות הבדיקות.
לבחירת חתך השתמש ב־`--view-2d --plane XY --slice 12`.
הכלל המלא כתוב ב־[דף ההגדרות](SIMULATOR_DEFINITIONS.md#ברירת-המחדל-להצגת-הרצות).

הרצה לאותה תיקיית פלט מחליפה את קובצי התוצאה;
להשוואת ניסויים יש לבחור תיקיות פלט שונות.

## בדיקת הפרויקט בפקודה אחת

```bash
python tools/check.py
```

הפקודה בודקת סגנון, עיצוב, טיפוסים ובדיקות התנהגות, ומפיקה
`artifacts/test-runs.html` עם כל הרצות הבדיקה, כולל גרסת ההשוואה הישנה.
אפשר להפעיל את הבדיקות בנפרד:

```bash
python -m ruff check .
python -m ruff format --check .
python -m mypy
python -m pytest --junitxml=artifacts/junit.xml
```

הגדרת GitHub Actions מצורפת ב־`.github/workflows/check.yml`. היא מיועדת לרוץ
על push ועל pull request לאחר העלאת הפרויקט למאגר GitHub. אין תלות ב־GitHub
להרצה ולבדיקה מקומית.

## איפה כל דבר נמצא

| נתיב | אחריות |
| --- | --- |
| `src/event_universe/core/state.py` | רשומות קבועות, פרמטרים וחשבון שלמים חסום |
| `src/event_universe/core/contracts.py` | ממשקי החוקים והאירועים המקומיים |
| `src/event_universe/core/lattice.py` | כתובות מחזוריות ושכנים, במימוש משותף לקריאה ולתנועה |
| `src/event_universe/core/engine.py` | אחסון דליל, זמן, שכנים, תפוסה ומעבר בין תאים |
| `src/event_universe/fields/scalar.py` | חישוב כללי של שדה סקלרי והגרדיאנט שלו |
| `src/event_universe/fields/policies.py` | חישוב מקור ומדיניות טווח ופעילות שנבחרות במודל |
| `src/event_universe/dynamics/turning.py` | פנייה כללית: בחירת כיוון, צבירת שאריות וחילופי תנע |
| `src/event_universe/dynamics/movement.py` | תקציב תנועה ובחירת צעד לשכן |
| `src/event_universe/models/current_field.py` | הבחירות של המודל שלנו וחיבור הרכיבים למצב התא והחלקיק |
| `src/event_universe/models/local_field.py` | תאימות לייבואים קודמים, ללא עותק של הלוגיקה |
| `src/event_universe/diagnostics/` | מדידות, ביקורת מצב, תיעוד ו־HTML |
| `src/event_universe/scenarios.py` | תרחישים ותנאי התחלה מפורשים |
| `src/event_universe/runner.py` | חיבור הריצה לתיעוד ולתצוגה |
| `tests/` | בדיקות יחידה, כללים מחייבים, רגרסיה והשוואת מצב מלאה |
| `tests/reference/` | עותק קפוא של המקור, המשמש לבדיקה בלבד |
| `POSTULATES_HE.md` | הפוסטולטים והרעיונות המחייבים בעברית פשוטה |
| `SIMULATOR_DEFINITIONS.md` | ההגדרות המחייבות המעודכנות |
| `docs/ARCHITECTURE.md` | גבולות אחריות וסדר העדכון |
| `docs/FIELDS_HE.md` | איך מחליפים שדה או כלל פנייה, בשפה פשוטה |
| `docs/TEST_EXPECTATIONS_HE.md` | בדיקות לפי אחריות, קלטים ותוצאות צפויות מדויקות |
| `docs/MIGRATION.md` | מעבר מקוד וממחברות ישנים |

## שדה כללי ושימוש פרטני

`ScalarField` מחשב שדה לפי משקלים לשישה שכנים, משקל לערך המקומי ומקור נתון.
`FieldTurning` מקבל וקטור מקומי ופונקציה שבוחרת לאילו רכיבים להגיב; הוא מרכז
את חישוב הדחף, השאריות וחילופי התנע. שני הרכיבים אינם מכירים עולם או חלקיק.

`CurrentFieldModel` מחבר אותם לשימוש שלנו: מקור לפי תפוסה, שדה שאינו שלילי
ופנייה לפי הגרדיאנט הרוחבי לציר התנועה הדומיננטי. אפשר להחליף כל רכיב בנפרד
באמצעות `Simulation(field=..., turning=...)`. ההסבר והדוגמאות נמצאים
ב־`docs/FIELDS_HE.md`. הבדיקות לשדה שלנו נמצאות ב־`tests/test_current_field.py`;
בדיקות נפרדות מאמתות את הרכיבים הכלליים ואת החלפתם בתוך סימולציה.

## כללים שנשמרים

- פיזיקה ב־3D עם שישה שכנים קרדינליים.
- מצב פיזיקלי בשלמים בלבד: חמישה רגיסטרים לתא ו־12 לחלקיק.
- רגיסטרים פיזיקליים חסומים; חישובי ביניים חסומים; גלישה נעצרת בשגיאה.
- עבודה מקומית חסומה לפי שישה שכנים ו־K מקומות קבועים בתא.
- מקור מתמיד נקבע על ידי תפוסה; שאריות חלוקה נשמרות בשלמים.
- חילופי תנע מקומיים בין חומר לשדה; אין תיקון תנע גלובלי.
- חוק מהירות אחד, ועד מעבר אחד לשכן בכל tick.
- המדידות וההנפשה אינן מזינות מידע חזרה למנוע.

זו מסגרת למחקר של מודל בדיד. חוק השדה וחוק הפנייה הם חוקים מועמדים מפורשים.
בדיקות התוכנה אינן הוכחה לשימור אנרגיה או לנכונות פיזיקלית כללית.
הנחות קיימות, ובהן סדר התנועה והעדפת ציר בשוויון, מתועדות ב־ARCHITECTURE.


### Local stretched-link candidate

```bash
PYTHONPATH=src python -m event_universe --scenario links --output artifacts/local-links --frame-stride 12
```

This selects `scalar-field-v11-local-links`: local six-port mailboxes, integer
lengths, symmetric edge proposals and frozen travel times. Its dedicated tests
are `test_link_geometry.py`, `test_link_transport.py` and `test_linked_engine.py`.
The example uses base length 10 for shorter replay; `LinkConfig()` defaults to
100. See the extension in `POSTULATES_HE.md`, `SIMULATOR_DEFINITIONS.md` and
`docs/ARCHITECTURE.md`. Existing baseline scenarios keep their old behavior.
