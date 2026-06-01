import json
import os
from datetime import datetime

# ── CONFIG ────────────────────────────────────────────────────────
API_KEY  = os.environ.get('METABASE_API_KEY', '')
CARD_URL = 'https://bia.metabaseapp.com/api/card/14059/query/json'

ES_SIGLAS = ['PREA','PRET','PREM','PRCE','VPNT','PVIC','PREB','PREC',
             'AMCA','TERM','MANT','CAEN','ISNT','ISIC','BICH','COND']

PREVIAS_CAT = [
    {'sigla':'PREA','desc':'Previa Aumento de Carga'},
    {'sigla':'PREM','desc':'Previa Mantenimiento'},
    {'sigla':'VPNT','desc':'Visita Previa Cambio NT'},
    {'sigla':'PVIC','desc':'Previa Independización Cuentas'},
    {'sigla':'PREB','desc':'Previa BIA Monitor'},
    {'sigla':'PREC','desc':'Previa Bancos de Condensadores'},
]

EJEC_CAT = [
    {'sigla':'AMCA','desc':'Ejecución Aumento de Carga'},
    {'sigla':'MANT','desc':'Ejecución Mantenimiento'},
    {'sigla':'ISNT','desc':'Instalación Cambio NT'},
    {'sigla':'BICH','desc':'Instalación BIA Monitor'},
    {'sigla':'COND','desc':'Instalación Banco de Condensadores'},
]

def parse_date(s):
    if not s: return None
    for fmt in ['%B %d, %Y','%Y-%m-%d','%d/%m/%Y','%b %d, %Y']:
        try: return datetime.strptime(s.strip(), fmt)
        except: pass
    return None

def fetch_data():
    """Fetch data from Metabase API"""
    import urllib.request
    req = urllib.request.Request(
        CARD_URL,
        data=b'{"parameters":[]}',
        headers={
            'Content-Type': 'application/json',
            'x-api-key': API_KEY
        },
        method='POST'
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())

def process_data(raw):
    """Filter and process Energy Solutions OTs"""
    result = []
    for r in raw:
        t = r.get('Tipo de servicio', '')
        if t not in ES_SIGLAS:
            continue
        d = parse_date(r.get('Fecha de la visita', ''))
        if not d:
            continue
        result.append({
            'tipo':    t,
            'estado':  r.get('Estado', ''),
            'or':      r.get('OR', '') or 'Sin operador',
            'ciudad':  r.get('Ciudad', ''),
            'fecha':   d.strftime('%Y-%m-%d'),
            'exitoso': 1 if r.get('Estado', '') in ['Cierre Exitoso', 'Completada'] else 0
        })
    return result

def build_html(es_data, updated_at):
    """Generate the full dashboard HTML with embedded data"""
    data_js = 'const ES_RAW_DATA = ' + json.dumps(es_data, separators=(',', ':')) + ';'
    total   = len(es_data)

    # Read template
    with open('template.html', 'r', encoding='utf-8') as f:
        template = f.read()

    # Inject dynamic values
    html = template \
        .replace('__DATA_JS__', data_js) \
        .replace('__TOTAL__', str(total)) \
        .replace('__UPDATED_AT__', updated_at)

    return html

if __name__ == '__main__':
    print(f"[{datetime.now()}] Iniciando actualización...")

    if not API_KEY:
        print("ERROR: METABASE_API_KEY no configurada")
        exit(1)

    print("Consultando Metabase...")
    raw = fetch_data()
    print(f"  → {len(raw)} registros obtenidos")

    print("Procesando datos Energy Solutions...")
    es_data = process_data(raw)
    print(f"  → {len(es_data)} OTs de Energy Solutions")

    updated_at = datetime.now().strftime('%d %b %Y %H:%M UTC')
    html = build_html(es_data, updated_at)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  → index.html generado ({len(html)} chars)")
    print(f"[{datetime.now()}] ¡Listo!")
