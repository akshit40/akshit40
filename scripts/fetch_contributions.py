import os,re,json,requests
from pathlib import Path
from datetime import datetime,timezone
from bs4 import BeautifulSoup

u=os.getenv("GITHUB_USERNAME","akshit40")
r=requests.get(f"https://github.com/users/{u}/contributions",headers={"User-Agent":"akshit40-profile"},timeout=30)
r.raise_for_status()
s=BeautifulSoup(r.text,"html.parser")
days=[]
for c in s.select("td.ContributionCalendar-day"):
    d=c.get("data-date"); level=int(c.get("data-level") or 0); a=c.get("aria-label","")
    m=re.search(r"([\d,]+) contribution",a)
    n=int(m.group(1).replace(",","")) if m else 0
    if d: days.append({"date":d,"count":n,"level":level})
if not days: raise SystemExit("No contribution cells found; GitHub may have changed its HTML.")
days.sort(key=lambda x:x["date"])
cur=0
for x in reversed(days):
    if x["count"]>0: cur+=1
    else: break
best=max(days,key=lambda x:x["count"])
longest=streak=0
for x in days:
    if x["count"]>0: streak+=1; longest=max(longest,streak)
    else: streak=0
payload={"username":u,"fetched_at":datetime.now(timezone.utc).isoformat(),"days":days,"stats":{"total":sum(x["count"] for x in days),"current_streak":cur,"longest_streak":longest,"best_day":best}}
Path("data").mkdir(exist_ok=True)
Path("data/contributions.json").write_text(json.dumps(payload,indent=2),encoding="utf-8")
print(f"Fetched {len(days)} days for @{u}; total={payload['stats']['total']}")
