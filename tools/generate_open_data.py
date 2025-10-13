#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv, datetime as dt, hashlib, json, re
from pathlib import Path

# ── KONFIG ────────────────────────────────────
# info -> # albo "" jeśli brak
DEVELOPER_NAME_PL = "ALU-CONSTRUCTION Zbigniew Wąsik"
DEVELOPER_LEGAL_FORM = ""
KRS   = ""
CEIDG = "5470124989"
NIP   = "5470124989"
REGON = "070851723"
TEL   = "660751199"
EMAIL = "alucons@interia.pl"
FAX   = ""
WWW_DEVELOPER = "https://ustron-mieszkania.pl"
PROSPEKT_URL  = "https://ustron-mieszkania.pl"

# Adres siedziby
HQ = dict(woj="śląskie", powiat="Bielsko-Biała", gmina="Bielsko-Biała", miejsc="Bielsko-Biała",
          ulica="ul. Tadeusza", nr_nier="58", nr_lok="", kod="43-382")

# Adres sprzedaży
SALES = dict(woj=HQ["woj"], powiat=HQ["powiat"], gmina=HQ["gmina"], miejsc=HQ["miejsc"],
             ulica=HQ["ulica"], nr_nier=HQ["nr_nier"], nr_lok=HQ["nr_lok"], kod=HQ["kod"])
DODATKOWE_LOKALIZACJE = ""
SPOSOB_KONTAKTU = "telefon; e-mail"

# Lokalizacja przedsięwzięcia
PROJECT = dict(woj="śląskie", powiat="cieszyński", gmina="Ustroń", miejsc="Ustroń",
               ulica="ul. Skoczowska", nr_nier="56", kod="43-450")

# Publikacja
DOMAIN_BASE_URL   = "https://ustron-mieszkania.pl/open-data"
DATA_JSON_PATH    = "data.json"
OUT_DIR_DAILY     = Path("open-data/daily")
OUT_DIR_MANIFEST  = Path("open-data/manifest")
# 36 znakow dataset extident
DATASET_EXTIDENT  = "USTRONMIESZKANIADATASETALUCONS000001"
KEEP_LAST_N_DAYS  = 60
CSV_DELIMITER     = ";"
RODZAJ_NIERUCH    = "Lokal mieszkalny"
# ───────────────────────────────────────────────────────────────────────────────

HEADERS = [
"Nazwa dewelopera","Forma prawna dewelopera","Nr KRS","Nr wpisu do CEiDG","Nr NIP","Nr REGON",
"Nr telefonu","Adres poczty elektronicznej","Nr faxu","Adres strony internetowej dewelopera",
"Województwo adresu siedziby/głównego miejsca wykonywania działalności gospodarczej dewelopera",
"Powiat adresu siedziby/głównego miejsca wykonywania działalności gospodarczej dewelopera ",
"Gmina adresu siedziby/głównego miejsca wykonywania działalności gospodarczej dewelopera",
"Miejscowość adresu siedziby/głównego miejsca wykonywania działalności gospodarczej dewelopera",
"Ulica adresu siedziby/głównego miejsca wykonywania działalności gospodarczej dewelopera",
"Nr nieruchomości adresu siedziby/głównego miejsca wykonywania działalności gospodarczej dewelopera",
"Nr lokalu adresu siedziby/głównego miejsca wykonywania działalności gospodarczej dewelopera",
"Kod pocztowy adresu siedziby/głównego miejsca wykonywania działalności gospodarczej dewelopera",
"Województwo adresu lokalu, w którym prowadzona jest sprzedaż",
"Powiat adresu lokalu, w którym prowadzona jest sprzedaż",
"Gmina adresu lokalu, w którym prowadzona jest sprzedaż",
"Miejscowość adresu lokalu, w którym prowadzona jest sprzedaż",
"Ulica adresu lokalu, w którym prowadzona jest sprzedaż",
"Nr nieruchomości adresu lokalu, w którym prowadzona jest sprzedaż",
"Nr lokalu adresu lokalu, w którym prowadzona jest sprzedaż",
"Kod pocztowy adresu lokalu, w którym prowadzona jest sprzedaż",
"Dodatkowe lokalizacje, w których prowadzona jest sprzedaż",
"Sposób kontaktu nabywcy z deweloperem",
"Województwo lokalizacji przedsięwzięcia deweloperskiego lub zadania inwestycyjnego",
"Powiat lokalizacji przedsięwzięcia deweloperskiego lub zadania inwestycyjnego",
"Gmina lokalizacji przedsięwzięcia deweloperskiego lub zadania inwestycyjnego",
"Miejscowość lokalizacji przedsięwzięcia deweloperskiego lub zadania inwestycyjnego",
"Ulica lokalizacji przedsięwzięcia deweloperskiego lub zadania inwestycyjnego",
"Nr nieruchomości lokalizacji przedsięwzięcia deweloperskiego lub zadania inwestycyjnego",
"Kod pocztowy lokalizacji przedsięwzięcia deweloperskiego lub zadania inwestycyjnego",
"Rodzaj nieruchomości: lokal mieszkalny, dom jednorodzinny ",
"Nr lokalu lub domu jednorodzinnego nadany przez dewelopera",
"Cena m 2 powierzchni użytkowej lokalu mieszkalnego / domu jednorodzinnego [zł]",
"Data od której cena obowiązuje cena m 2 powierzchni użytkowej lokalu mieszkalnego / domu jednorodzinnego",
"Cena lokalu mieszkalnego lub domu jednorodzinnego będących przedmiotem umowy stanowiąca iloczyn ceny m2 oraz powierzchni [zł]",
"Data od której cena obowiązuje cena lokalu mieszkalnego lub domu jednorodzinnego będących przedmiotem umowy stanowiąca iloczyn ceny m2 oraz powierzchni",
"Cena lokalu mieszkalnego lub domu jednorodzinnego uwzględniająca cenę lokalu stanowiącą iloczyn powierzchni oraz metrażu i innych składowych ceny, o których mowa w art. 19a ust. 1 pkt 1), 2) lub 3) [zł]",
"Data od której obowiązuje cena lokalu mieszkalnego lub domu jednorodzinnego uwzględniająca cenę lokalu stanowiącą iloczyn powierzchni oraz metrażu i innych składowych ceny, o których mowa w art. 19a ust. 1 pkt 1), 2) lub 3)",
"Rodzaj części nieruchomości będących przedmiotem umowy",
"Oznaczenie części nieruchomości nadane przez dewelopera",
"Cena części nieruchomości, będących przedmiotem umowy [zł]",
"Data od której obowiązuje cena części nieruchomości, będących przedmiotem umowy",
"Rodzaj pomieszczeń przynależnych, o których mowa w art. 2 ust. 4 ustawy z dnia 24 czerwca 1994 r. o własności lokali",
"Oznaczenie pomieszczeń przynależnych, o których mowa w art. 2 ust. 4 ustawy z dnia 24 czerwca 1994 r. o własności lokali",
"Wyszczególnienie cen pomieszczeń przynależnych, o których mowa w art. 2 ust. 4 ustawy z dnia 24 czerwca 1994 r. o własności lokali [zł]",
"Data od której obowiązuje cena wyszczególnionych pomieszczeń przynależnych, o których mowa w art. 2 ust. 4 ustawy z dnia 24 czerwca 1994 r. o własności lokali",
"Wyszczególnienie praw niezbędnych do korzystania z lokalu mieszkalnego lub domu jednorodzinnego",
"Wartość praw niezbędnych do korzystania z lokalu mieszkalnego lub domu jednorodzinnego [zł]",
"Data od której obowiązuje cena wartości praw niezbędnych do korzystania z lokalu mieszkalnego lub domu jednorodzinnego",
"Wyszczególnienie rodzajów innych świadczeń pieniężnych, które nabywca zobowiązany jest spełnić na rzecz dewelopera w wykonaniu umowy przenoszącej własność",
"Wartość innych świadczeń pieniężnych, które nabywca zobowiązany jest spełnić na rzecz dewelopera w wykonaniu umowy przenoszącej własność [zł]",
"Data od której obowiązuje cena wartości innych świadczeń pieniężnych, które nabywca zobowiązany jest spełnić na rzecz dewelopera w wykonaniu umowy przenoszącej własność",
"Adres strony internetowej, pod którym dostępny jest prospekt informacyjny"
]

def ensure_dirs():
    OUT_DIR_DAILY.mkdir(parents=True, exist_ok=True)
    OUT_DIR_MANIFEST.mkdir(parents=True, exist_ok=True)

def now_with_time():
    return dt.datetime.now().strftime("%Y-%m-%d 16:00:00").replace(" 16:00:00", " 16:00:00")

def iso_day(d: dt.date): return d.isoformat()

def load_json():
    with open(DATA_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def money(x): return str(int(round(float(x))))

def build_rows(data):
    rows = []
    now_dt = now_with_time()
    for r in data:
        pow_m2 = float(r["powierzchnia_m2"])
        cena_m2 = float(r["cena_m2"])
        cena_iloczyn = pow_m2 * cena_m2
        cena_z_innymi = cena_iloczyn

        row = [
            DEVELOPER_NAME_PL, DEVELOPER_LEGAL_FORM, KRS, CEIDG, NIP, REGON,
            TEL, EMAIL, FAX, WWW_DEVELOPER,
            HQ["woj"], HQ["powiat"], HQ["gmina"], HQ["miejsc"], HQ["ulica"], HQ["nr_nier"], HQ["nr_lok"], HQ["kod"],
            SALES["woj"], SALES["powiat"], SALES["gmina"], SALES["miejsc"], SALES["ulica"], SALES["nr_nier"], SALES["nr_lok"], SALES["kod"],
            "",
            SPOSOB_KONTAKTU,
            PROJECT["woj"], PROJECT["powiat"], PROJECT["gmina"], PROJECT["miejsc"], PROJECT["ulica"], PROJECT["nr_nier"], PROJECT["kod"],
            RODZAJ_NIERUCH,
            r["id"],
            money(cena_m2),
            now_dt,
            money(cena_iloczyn),
            now_dt,
            money(cena_z_innymi),
            now_dt,
            "X","X","0",now_dt,
            "X","X","0",now_dt,
            "X","0",now_dt,
            "X","0",now_dt,
            PROSPEKT_URL
        ]
        rows.append(row)
    return rows

def csv_name_for(date: dt.date): return f"cennik_{date.strftime('%Y_%m_%d')}.csv"

def write_csv(rows, date: dt.date):
    out = OUT_DIR_DAILY / csv_name_for(date)
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=CSV_DELIMITER)
        w.writerow(HEADERS)
        w.writerows(rows)
    return out

def discover_daily_files(limit_days:int):
    files=[]
    for p in sorted(OUT_DIR_DAILY.glob("cennik_*.csv")):
        m = re.search(r"cennik_(\d{4})_(\d{2})_(\d{2})\.csv$", p.name)
        if m:
            y,mo,d = map(int, m.groups()); files.append((dt.date(y,mo,d), p))
    return sorted(files, key=lambda x:x[0])[-limit_days:]

def to36(s:str):
    s = re.sub(r"[^A-Za-z0-9]","",s)
    return (s + "0"*36)[:36]

def res_extident(date: dt.date): return to36(f"USTRONRES{date.strftime('%Y%m%d')}")

def build_manifest_xml(resources, dev_name):
    L=[]
    L.append('<?xml version="1.0" encoding="UTF-8"?>')
    L.append('<ns2:datasets xmlns:ns2="urn:otwarte-dane:harvester:1.13" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">')
    L.append('  <dataset status="published">')
    L.append(f'    <extIdent>{DATASET_EXTIDENT}</extIdent>')
    L.append('    <title>')
    L.append(f'      <polish>Ceny ofertowe mieszkań dewelopera {dev_name}</polish>')
    L.append(f'      <english>Offer prices of apartments of developer {dev_name}</english>')
    L.append('    </title>')
    L.append('    <description>')
    L.append('      <polish>Zbiór danych zawiera informacje o cenach ofertowych mieszkań udostępniane zgodnie z art. 19b ustawy z dnia 20 maja 2021 r. (Dz. U. z 2024 r. poz. 695).</polish>')
    L.append('      <english>The dataset contains information on offer prices made available pursuant to Art. 19b.</english>')
    L.append('    </description>')
    L.append('    <updateFrequency>daily</updateFrequency>')
    L.append('    <hasDynamicData>false</hasDynamicData>')
    L.append('    <hasHighValueData>true</hasHighValueData>')
    L.append('    <hasHighValueDataFromEuropeanCommissionList>false</hasHighValueDataFromEuropeanCommissionList>')
    L.append('    <hasResearchData>false</hasResearchData>')
    L.append('    <categories><category>ECON</category></categories>')
    L.append('    <resources>')
    for r in resources:
        L.append('      <resource status="published">')
        L.append(f'        <extIdent>{r["extident"]}</extIdent>')
        L.append(f'        <url>{r["url"]}</url>')
        L.append('        <title>')
        L.append(f'          <polish>{r["title_pl"]}</polish>')
        L.append(f'          <english>{r["title_en"]}</english>')
        L.append('        </title>')
        L.append('        <description>')
        L.append(f'          <polish>{r["desc_pl"]}</polish>')
        L.append(f'          <english>{r["desc_en"]}</english>')
        L.append('        </description>')
        L.append('        <availability>local</availability>')
        L.append(f'        <dataDate>{r["dataDate"]}</dataDate>')
        L.append('        <specialSigns><specialSign>X</specialSign></specialSigns>')
        L.append('        <hasDynamicData>false</hasDynamicData>')
        L.append('        <hasHighValueData>true</hasHighValueData>')
        L.append('        <hasHighValueDataFromEuropeanCommissionList>false</hasHighValueDataFromEuropeanCommissionList>')
        L.append('        <hasResearchData>false</hasResearchData>')
        L.append('        <containsProtectedData>false</containsProtectedData>')
        L.append('      </resource>')
    L.append('    </resources>')
    L.append('    <tags><tag lang="pl">Deweloper</tag></tags>')
    L.append('  </dataset>')
    L.append('</ns2:datasets>')
    return "\n".join(L)

def write_manifest_and_md5(resources):
    xml = build_manifest_xml(resources, DEVELOPER_NAME_PL)
    xml_path = OUT_DIR_MANIFEST / "manifest.xml"
    xml_path.write_text(xml, encoding="utf-8")
    md5 = hashlib.md5(xml.encode("utf-8")).hexdigest()
    (OUT_DIR_MANIFEST / "manifest.md5").write_text(md5 + "\n", encoding="utf-8")

def main():
    OUT_DIR_DAILY.mkdir(parents=True, exist_ok=True)
    OUT_DIR_MANIFEST.mkdir(parents=True, exist_ok=True)

    today = dt.date.today()
    data = load_json()
    rows = build_rows(data)
    write_csv(rows, today)

    files = discover_daily_files(KEEP_LAST_N_DAYS)
    resources=[]
    for date, path in files:
        resources.append({
            "extident": res_extident(date),
            "url": f"{DOMAIN_BASE_URL}/daily/{path.name}",
            "title_pl": f"Ceny ofertowe mieszkań {DEVELOPER_NAME_PL} {iso_day(date)}",
            "title_en": f"Offer prices {DEVELOPER_NAME_PL} {iso_day(date)}",
            "desc_pl": f"Dane dotyczące cen ofertowych mieszkań udostępnione {iso_day(date)} zgodnie z art. 19b.",
            "desc_en": f"Data on offer prices made available on {iso_day(date)} pursuant to Art. 19b.",
            "dataDate": iso_day(date)
        })
    write_manifest_and_md5(resources)
    print("✔ CSV + manifest gotowe.")

if __name__ == "__main__":
    main()
