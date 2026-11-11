#!/usr/bin/env python3
"""Builds presentation/review.html (複習版) from ideas/chapters.json and presentation/report.html (報告版)."""
import json, sys, pathlib, html, re

ROOT = pathlib.Path(sys.argv[1])
chapters = json.loads((ROOT / "ideas" / "chapters.json").read_text(encoding="utf-8"))
A = "../assets/"
CAST = ["cat_professor", "cat_settlor", "cat_trustee", "cat_beneficiary", "cat_supervisor"]

def page(title, slides, deck_label):
    return f"""<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="deck.css">
</head><body>
<div id="progress"></div>
<button id="menu-btn" title="目錄 (M)">目錄</button>
<div id="menu"></div>
<div id="viewport"><div id="stage">
{slides}
</div></div>
<div id="nav"><button id="prev">← 上一頁</button><button id="next">下一頁 →</button></div>
<script src="deck.js"></script>
</body></html>
"""

def hd(title, chip="", mascot="cat_professor"):
    cls = ""
    n = len(re.sub(r"<[^>]+>", "", title))
    size = "" if n <= 17 else ' style="font-size:30px"' if n <= 24 else ' style="font-size:26px"'
    chip_html = f'<span class="chip">{chip}</span>' if chip else ""
    return (f'<div class="hd"><img class="mascot" src="{A}{mascot}.svg" alt="">'
            f'<h2{size}>{title}</h2>{chip_html}</div>')

def foot(label):
    return f'<div class="foot"><span>{label}</span><span class="pg"></span></div>'

def slide(inner, cls="", menu=None):
    m = f' data-menu="{html.escape(menu)}"' if menu else ""
    return f'<section class="slide {cls}"{m}>\n{inner}\n</section>'

def content(title, body, label, chip="", mascot="cat_professor", menu=False, scroll=True, cls="", zoom=None):
    bd = "bd" if scroll else "bd noscroll"
    if zoom: body = f'<div style="zoom:{zoom}">{body}</div>'
    return slide(f'{hd(title, chip, mascot)}<div class="{bd}">{body}</div>{foot(label)}', cls,
                 menu=re.sub(r"<[^>]+>", "", title) if menu else None)

# =========================================================== 複習版
OUTLINE = []
def build_review():
    L = "信託法規與實務｜複習版"
    S = []
    S.append(slide(f'''<div class="cover">
<h1>信託法規與實務<br>三色重點複習</h1>
<div class="sub">21 章逐章複習：重點 ＋ 紅藍綠筆 ＋ 試題</div>
<img src="{A}scene_cast.svg" alt="貓咪角色全員">
<div class="meta">複習版｜依「三色互動筆記」整理｜←/→ 換頁 · M 目錄 · F 全螢幕</div></div>''', menu="封面"))
    S.append(content("三色筆記怎麼讀？", f'''
<div class="cols3" style="margin-top:6px">
<div class="card red"><h3>🔴 紅筆</h3><p>高頻考點、必背數字、考場陷阱。看到紅色就是「會考」。</p></div>
<div class="card blue"><h3>🔵 藍筆</h3><p>核心定義與法條重點。先懂藍色，才看得懂紅色。</p></div>
<div class="card green"><h3>🟢 綠筆</h3><p>譬喻、圖解、速記口訣與答題心法，幫你記得住。</p></div>
</div>
<div class="cols2" style="margin-top:22px;align-items:center">
<div class="card"><h3>每章的節奏</h3><p>① 章節標題頁（命題趨勢）<br>② 重點頁（逐節複習）<br>③ 試題頁（點題目顯示答案）</p></div>
<div class="card"><h3>操作小抄</h3><p><b>← →</b> 換頁　<b>M</b> 目錄　<b>F</b> 全螢幕<br>內容較多的頁面可以<b>上下捲動</b></p></div>
</div>''', L, chip="使用說明", menu=True))

    for idx, c in enumerate(chapters):
        n = int(re.search(r"\d+", c["number"]).group())
        cat = CAST[idx % len(CAST)]
        first = len(S) + 1
        t = c["title"]
        fs = 54 if len(t) <= 24 else 42 if len(t) <= 36 else 34
        S.append(slide(f'''<div class="ch-title">
<div class="num">{n:02d}</div>
<div class="badge">{html.escape(c["badge"])}</div>
<h1 style="font-size:{fs}px">{html.escape(t)}</h1>
<div class="bubble"><b>命題趨勢：</b>{html.escape(c["analysis"])}</div>
<img class="big" src="{A}{cat}.svg" alt="">
{foot(L)}</div>''', menu=f'{c["number"]} {t}'))
        quiz_secs = []
        for s in c["sections"]:
            if "quiz-item" in s["content"]:
                quiz_secs.append(s)
                continue
            S.append(content(html.escape(s["sub_title"]), s["content"], L, chip=c["number"], mascot=cat))
        _nq = len(quiz_secs)
        for s in quiz_secs:
            body = '<div class="quiz-hint">點題目（或按 → ）顯示答案</div>' + s["content"]
            S.append(content("本章精選試題", body, L, chip=c["number"], mascot=cat, cls="quiz-slide"))
        OUTLINE.append((c, first, len(S)))
    OUTLINE.append((None,None,None))
    S.append(slide(f'''<div class="cover">
<h1>複習完成！</h1>
<div class="sub">考前最後十分鐘：回到第 17、18、20、21 章再掃一遍</div>
<img src="{A}scene_cast.svg" alt="">
<div class="meta">條文與數字以最新法規為準 ｜ {L}</div></div>''', menu="結語"))
    return page("信託法規與實務｜複習版", "\n".join(S), L)

# =========================================================== 報告版
def build_report():
    L = "信託法規與實務｜報告版"
    S = []
    S.append(slide(f'''<div class="cover">
<h1>信託法規與實務<br>三色重點精讀</h1>
<div class="sub">一次看懂：關係人 · 財產獨立 · 關鍵數字</div>
<img src="{A}scene_cast.svg" alt="貓咪角色全員">
<div class="meta">報告版｜依「三色互動筆記」整理｜←/→ 換頁 · M 目錄 · F 全螢幕</div></div>''', menu="封面"))

    S.append(content("這份簡報要帶走 3 件事", f'''
<div class="cols3" style="margin-top:10px">
<div class="card blue" style="text-align:center"><img class="imgc" src="{A}scene_cast.svg" style="height:0;display:none"><img class="imgc" src="{A}cat_settlor.svg" height="190" alt=""><h3>① 誰是誰</h3><p>委託人、受託人、受益人<br>各自的名義與權責</p></div>
<div class="card red" style="text-align:center"><img class="imgc" src="{A}icon_shield.svg" height="190" alt=""><h3>② 財產獨立</h3><p>信託財產有四道護盾<br>債權人不能亂碰</p></div>
<div class="card green" style="text-align:center"><img class="imgc" src="{A}icon_calendar.svg" height="190" alt=""><h3>③ 數字不混淆</h3><p>期限、金額、比例<br>用一張表記牢</p></div>
</div>''', L, menu=True, scroll=False, zoom=1.2))

    S.append(content("什麼是信託？", f'''
<div style="display:grid;grid-template-columns:690px 1fr;gap:22px;align-items:center">
<img class="imgc" src="{A}scene_trust_triangle.svg" style="width:690px" alt="信託三方關係">
<div class="card blue"><h3>信託法第 1 條</h3>
<p>委託人把財產權移轉出去，受託人<b>依信託本旨</b>，為受益人的利益或特定目的，管理或處分信託財產。</p></div>
</div>
<div class="cols2" style="margin-top:16px">
<div class="card red"><h3>🔴 第一必考點</h3><p>受託人是以<b>「自己名義」</b>管理處分，不是委託人或受益人名義。</p></div>
<div class="card green"><h3>🟢 房屋出租的譬喻</h3><p>承租人只認受託人的名義簽約、收租；租金交給受益人當生活費。</p></div>
</div>''', L, chip="信託法第 1 條", menu=True, scroll=False))

    S.append(content("信託怎麼成立？四種型態", f'''
<table class="data-table"><thead><tr><th>型態</th><th>成立時點</th><th>生效時點</th><th>考場陷阱</th></tr></thead><tbody>
<tr><td><b>契約信託</b></td><td>雙方意思表示合致時</td><td>原則上成立即生效</td><td>最常見，實務上佔 90% 以上</td></tr>
<tr><td><b>遺囑信託</b></td><td>遺囑依法作成時</td><td><span class="hl-red">立遺囑人死亡時</span></td><td><span class="hl-red">成立與生效不同步</span>（必考時間差）</td></tr>
<tr><td><b>宣言信託</b></td><td>作成宣言時</td><td>經主管機關許可並作成宣言時</td><td><span class="hl-red">法人專屬</span>，自然人不得辦理</td></tr>
<tr><td><b>法定信託</b></td><td>法定事由發生時</td><td>法定事由發生時</td><td>直接基於法律強制規定而成立</td></tr>
</tbody></table>
<div class="cols2" style="margin-top:10px;align-items:center">
<div class="card red"><h3>🔴 無效情事（信託法第 5 條）</h3><p>違反強制禁止規定、違反公序良俗、<b>以訴訟為主要目的</b>、以不得受讓財產權之人為受益人。</p></div>
<div class="center"><img src="{A}cat_professor.svg" height="200" alt=""></div></div>''', L, chip="成立與生效", menu=True, scroll=False, zoom=1.1))

    S.append(content("分類：自益／他益與「交付時判定」", f'''
<div class="cols2">
<div>
<div class="card blue" style="margin-bottom:16px"><h3>自益信託</h3><p>委託人＝受益人。可<b>隨時終止</b>，成立時<b>不課贈與稅</b>。</p></div>
<div class="card red"><h3>他益信託</h3><p>第三人享有利益。契約成立時課<b>贈與稅</b>；非經全體同意不得任意終止。</p></div>
</div>
<div>
<div class="card yellow" style="margin-bottom:16px"><h3>🔴 交付時判定原則</h3><p>以<b>交付當時的財產型態</b>分類。甲交付 5,000 萬現金給銀行，指示全數買商辦大樓出租，仍是<b>金錢信託</b>。</p></div>
<div class="card green"><h3>🟢 不指定營運範圍</h3><p>不得投資未上市股票、期貨與不動產。</p></div>
</div>
</div>''', L, chip="分類", menu=True, mascot="cat_settlor", scroll=False, zoom=1.35))

    S.append(content("受託人四大義務：善管、忠實、分開、親自", f'''
<div class="cols4">
<div class="card blue"><h3>善管</h3><p>善良管理人注意義務（§22）。<b>無償也一樣</b>。</p></div>
<div class="card blue"><h3>忠實</h3><p>完全為受益人著想，不准圖利自己。違反所得<b>歸入信託財產</b>（§35）。</p></div>
<div class="card blue"><h3>分開</h3><p>與自有財產、其他信託財產分別管理，金錢分別記帳（§24）。</p></div>
<div class="card blue"><h3>親自</h3><p>原則上自己處理信託事務；信託行為另有訂定或有不得已事由才可複委託（§25）。</p></div>
</div>
<div style="display:grid;grid-template-columns:170px 1fr 1fr;gap:18px;margin-top:16px;align-items:center">
<img class="imgc" src="{A}cat_trustee.svg" height="210" alt="">
<div class="card green"><h3>🟢 口訣</h3><p class="big-cap" style="font-size:30px">善管、忠實、<br>分開、親自！</p></div>
<div class="card red"><h3>🔴 不得擔任受託人</h3><p>未成年人、受監護或輔助宣告之人、受破產宣告之人；存續期間發生者<b>當然解任</b>。</p></div>
</div>''', L, chip="受託人", menu=True, mascot="cat_trustee", scroll=False, zoom=1.0))

    S.append(content("信託財產的四道護盾", f'''
<div style="display:grid;grid-template-columns:230px 1fr;gap:24px;align-items:center">
<img class="imgc" src="{A}icon_shield.svg" style="width:220px" alt="">
<div class="cols2">
<div class="card blue"><h3>① 破產隔離</h3><p>受託人破產，信託財產不入破產財團；受託人死亡，也不是遺產。</p></div>
<div class="card blue"><h3>② 抵銷禁止（§14）</h3><p>受託人個人的債，不能拿來和信託財產的債權抵銷。</p></div>
<div class="card blue"><h3>③ 混同例外（§13）</h3><p>債權債務或物權同歸受託人，也不因混同而消滅。</p></div>
<div class="card red"><h3>④ 禁止強制執行（§12）</h3><p>委託人個人的債權人，不得查封拍賣信託財產。</p></div>
</div></div>
<div class="card green" style="margin-top:18px"><h3>🟢 同一性（物上代位）</h3><p>信託房屋火災領的保險金、土地徵收補償費、賣股票的價款，<b>仍屬信託財產</b>。純粹的債務不能單獨成立信託。</p></div>''',
                       L, chip="獨立性", menu=True, scroll=False))

    S.append(content("例外：哪些債權人可以強制執行？", f'''
<div class="cols3">
<div class="card red"><h3>① 信託前已存在</h3><p>該財產上原有的權利。<br><span class="sub-cap">例：早已設定的第一順位抵押權</span></p></div>
<div class="card red"><h3>② 處理信託事務所生</h3><p>為管理信託而產生的債務。<br><span class="sub-cap">例：修繕房屋的工程款、仲介費</span></p></div>
<div class="card red"><h3>③ 依法律規定的稅捐</h3><p>信託財產本身產生的稅。<br><span class="sub-cap">例：地價稅、房屋稅</span></p></div>
</div>
<p style="margin:10px 4px" class="sub-cap">④ 其他法律有特別規定者。</p>
<div style="display:grid;grid-template-columns:170px 1fr;gap:20px;align-items:center;margin-top:6px">
<img class="imgc" src="{A}cat_settlor.svg" height="200" alt="">
<div class="card yellow"><h3>情境題</h3><p>甲把土地信託給乙，之後甲<b>個人</b>欠丙民間借款 200 萬。丙可以聲請查封該信託土地嗎？<br><b class="hl-green">不行。</b>不是信託前的權利，也不是處理信託事務所生，受獨立性保護（§12）。</p></div>
</div>''', L, chip="強制執行", menu=True, scroll=False, zoom=1.08))

    S.append(content("時間與公示：知一做十、對抗要件", f'''
<div class="cols2">
<div class="card red" style="text-align:center"><img class="imgc" src="{A}icon_calendar.svg" height="200" alt="">
<h3>債權人撤銷詐害信託（§6、§7）</h3><p>知有撤銷原因起 <b>1 年</b>不行使就消滅；信託成立逾 <b>10 年</b>也消滅。</p></div>
<div class="card blue"><h3>公示制度（§4）</h3>
<p>土地、房屋：要<b>信託登記</b>。<br>有價證券：證券上載明信託財產；記名股票要通知公司載入股東名簿。</p>
<h3 style="margin-top:8px;color:var(--red)">🔴 對抗要件，不是生效要件</h3>
<p>沒登記，契約在雙方之間<b>照樣有效</b>，只是不能對抗善意第三人。</p></div>
</div>
<p class="sub-cap" style="margin-top:12px">🟢 口訣：「知悉起算一年，成立逾期十年失效」</p>''', L, chip="期限與公示", menu=True, scroll=False, zoom=1.2))

    def nc(n, l, s):
        return f'<div class="card numcard" style="padding:26px 10px 22px"><div class="n">{n}</div><div class="l">{l}</div><div class="s">{s}</div></div>'
    S.append(content("信託業的設立與投資紅線", f'''
<div class="cols4">
{nc("20 億","最低實收資本額","考場常誤導成 30 億")}
{nc("5,000 萬","賠償準備金","限現金或政府債券，繳存央行")}
{nc("25%","同一人持股上限","同一關係人合併計算")}
{nc("6 個月","領照後須開業","逾期廢止許可，得展延 6 個月一次")}
{nc("20%","發起人現金出資","不得低於實收資本額")}
{nc("5%","大股東（利害關係人）","持股 5% 以上")}
{nc("40%","轉投資金融相關事業","不得超過淨值")}
{nc("100%","自用不動產","不得超過淨值")}
</div>''', L, chip="信託業法", menu=True, mascot="cat_supervisor", scroll=False))

    S.append(content("行為規範紅綠燈", f'''
<div style="display:grid;grid-template-columns:150px 1fr;gap:20px;align-items:center">
<img class="imgc" src="{A}icon_traffic.svg" height="400" alt="">
<div>
<div class="card red" style="margin-bottom:16px"><h3>🔴 紅燈：絕對禁止（委託人同意也無效）</h3>
<ul><li>承諾擔保本金或最低收益</li><li>自易行為：信託財產與自有財產互相買賣</li><li>購買信託業本身發行的股票或債券</li><li>提供信託財產為他人借款設擔保</li></ul></div>
<div class="card green"><h3>🟢 黃綠燈：相對禁止（兩把鑰匙缺一不可）</h3>
<p>① <b>信託契約有明確約定</b>　② <b>事先取得委託人書面同意</b></p>
<ul><li>信託資金存放該信託業銀行部門收息</li><li>購買利害關係人發行的標的、代理利害關係人交易</li></ul></div>
</div></div>''', L, chip="第 6、19 章", menu=True, mascot="cat_supervisor", scroll=False))

    S.append(content("信託稅法：導管原則", f'''
<div class="cols2">
<div class="card blue"><h3>導管原則</h3><p>信託財產只是流經受託人；稅<b>穿透受託人</b>，向實質受益人課。</p></div>
<div class="card red"><h3>🔴 所得發生年度課稅</h3><p>不是等到「實際分配」才課，避免把獲利留在信託專戶遞延。</p></div>
</div>
<table class="data-table"><thead><tr><th>階段</th><th>自益信託</th><th>他益信託</th></tr></thead><tbody>
<tr><td><b>成立時</b></td><td>形式移轉，免稅</td><td>課委託人<b class="hl-red">贈與稅</b>（契約成立時）</td></tr>
<tr><td><b>存續中</b></td><td colspan="2">依所得發生年度，課受益人綜合所得稅</td></tr>
<tr><td><b>消滅時</b></td><td>返還委託人，免稅</td><td>實質移轉，履行約定</td></tr>
</tbody></table>
<div class="card yellow"><b>受託人要當納稅人的四種情形：</b>
<span class="tag r">受益人不特定</span><span class="tag r">受益人尚未存在</span><span class="tag r">非境內居住者</span><span class="tag r">集合管理帳戶／共同信託基金</span></div>''',
                       L, chip="稅法", menu=True, scroll=False))

    S.append(content("不動產證券化：REITs vs REATs", f'''
<div style="display:grid;grid-template-columns:190px 1fr;gap:20px;align-items:center">
<img class="imgc" src="{A}icon_building.svg" style="width:180px" alt="">
<table class="data-table" style="margin:0"><thead><tr><th>比較</th><th>REITs（基金型）</th><th>REATs（資產型）</th></tr></thead><tbody>
<tr><td><b>本質</b></td><td>資金運用型</td><td>資產流動型（融資）</td></tr>
<tr><td><b>順序</b></td><td><b>先有錢</b>，再買樓收租</td><td><b>先有樓</b>，切塊換現</td></tr>
<tr><td><b>型態</b></td><td>開放型或封閉型</td><td>通常為封閉型</td></tr>
<tr><td><b>租稅</b></td><td colspan="2">收益分配採<b class="hl-red">分離課稅 10%</b></td></tr>
</tbody></table></div>
<div class="cols3" style="margin-top:18px">
{nc("35 人","私募人數上限","金融機構除外")}
{nc("3 億","強制雙估價","單筆達 3 億須 2 家以上估價")}
{nc("6 個月","估價報告時效","出具日至簽約日")}
</div>''', L, chip="第 11 章", menu=True, scroll=False, zoom=1.15))

    S.append(content("金融資產證券化：SPT vs SPC", f'''
<div style="display:grid;grid-template-columns:190px 1fr;gap:20px;align-items:center">
<img class="imgc" src="{A}icon_vault.svg" style="width:180px" alt="">
<table class="data-table" style="margin:0"><thead><tr><th>比較</th><th>SPT（特殊目的信託）</th><th>SPC（特殊目的公司）</th></tr></thead><tbody>
<tr><td><b>組織</b></td><td>契約信託關係</td><td>股份有限公司法人</td></tr>
<tr><td><b>最低資本額</b></td><td><span class="hl-red">受託機構 20 億</span></td><td><span class="hl-red">10 萬</span></td></tr>
<tr><td><b>發行證券</b></td><td><span class="hl-red">受益證券</span></td><td><span class="hl-red">資產基礎證券</span></td></tr>
</tbody></table></div>
<div class="cols2" style="margin-top:18px">
<div class="card red"><h3>🔴 真實出售（True Sale）</h3><p>資產賣斷給 SPV，創始銀行倒閉，其債權人<b>也不能查封</b>該批資產 ＝ 破產隔離。</p></div>
<div class="card blue"><h3>內部信用增強</h3><p>優先／次順位證券、超額擔保、備償準備金。次順位先吸收損失。</p></div>
</div>''', L, chip="第 12 章", menu=True, scroll=False, zoom=1.22))

    S.append(content("考前救命數字速查", f'''
<div class="cols4">
{nc("35 人","私募上限","")}
{nc("20 億","信託業資本額","")}
{nc("5,000 萬","賠償準備金","專業投資人法人淨資產亦同")}
{nc("3 億","不動產雙估價","")}
{nc("3 日","退票通報","通報金管會與公會")}
{nc("2 年","董監主管連帶責任","自卸職日起算，不是 5 年")}
{nc("3～10 年","非信託業營業刑期","最重刑責")}
{nc("15 日","新種信託商品備查","")}
</div>''', L, chip="第 17 章", menu=True, mascot="cat_beneficiary", scroll=False, zoom=1.15))

    def trick(q, a):
        return f'<div class="card" style="display:flex;align-items:center;gap:14px;padding:12px 18px"><span style="flex:1;font-size:22px;font-weight:700">{q}</span><span class="tag g" style="white-space:nowrap;font-size:20px">{a}</span></div>'
    S.append(content("考場秒殺心法", f'''
<div style="display:grid;grid-template-columns:200px 1fr;gap:20px;align-items:center">
<img class="imgc" src="{A}icon_fish_coin.svg" style="width:190px" alt="">
<div style="display:grid;gap:12px">
{trick("看到「計算淨值週期」","每一營業日")}
{trick("看到「不指定營運範圍」","排除未上市股票、期貨、不動產")}
{trick("看到「非信託業營業刑期」","三年以上十年以下")}
{trick("看到「受益人尚未出生，誰納稅」","受託人")}
{trick("看到「員工持股名義登記」","受託銀行信託專戶")}
{trick("看到「交付時判定」","拿錢買大樓，仍是金錢信託")}
</div></div>''', L, chip="第 21 章", menu=True, mascot="cat_professor", scroll=False, zoom=1.15))

    S.append(slide(f'''<div class="cover">
<h1>謝謝聆聽！<br>Q &amp; A</h1>
<div class="sub">善管、忠實、分開、親自 ‧ 財產獨立 ‧ 數字不混淆</div>
<img src="{A}scene_cast.svg" alt="">
<div class="meta">內容依「三色互動筆記」整理，條文與數字以最新法規為準 ｜ {L}</div></div>''', menu="結語"))
    return page("信託法規與實務｜報告版", "\n".join(S), L)

def write_outline():
    rows = ["# 複習版逐頁大綱（自動產生）", "",
            "複習版 = 每章「標題頁（命題趨勢）→ 逐節重點頁 → 試題頁」。內容直接取自 `ideas/` 的筆記，不改寫、不增刪數字。", "",
            "| 章節 | 標籤 | 頁碼範圍 | 重點頁 | 試題頁 |", "|---|---|---|---|---|"]
    for c, a, z in OUTLINE:
        if c is None: continue
        secs = [s["sub_title"] for s in c["sections"] if "quiz-item" not in s["content"]]
        q = sum(1 for s in c["sections"] if "quiz-item" in s["content"])
        rows.append(f"| {c['number']} {c['title']} | {c['badge']} | {a}–{z} | {'；'.join(secs)} | {q} 頁 |")
    (ROOT / "slide_notes" / "outline_review.md").write_text("\n".join(rows) + "\n", encoding="utf-8")

def main():
    pres = ROOT / "presentation"
    (pres / "review.html").write_text(build_review(), encoding="utf-8")
    (pres / "report.html").write_text(build_report(), encoding="utf-8")
    write_outline()
    print("ok")

main()
