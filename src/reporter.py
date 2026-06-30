import os
import webbrowser
from datetime import datetime

REPORTES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'reportes')


def _ensure_dir():
    os.makedirs(REPORTES_DIR, exist_ok=True)


def _escape(text):
    return (str(text)
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))


def _base_html(title, body_content):
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{font-family:'Segoe UI',Arial,sans-serif;background:#edf3ee;color:#222}}
  header{{background:#0d3b2e;color:#fff;padding:16px 28px;display:flex;align-items:center;gap:16px}}
  header h1{{font-size:1.2rem;font-weight:600}}
  header span{{font-size:.85rem;color:#7fc4a0}}
  main{{padding:28px;max-width:1100px;margin:0 auto}}
  h2{{color:#0d3b2e;margin-bottom:6px;font-size:1.3rem}}
  .meta{{color:#888;font-size:.85rem;margin-bottom:20px}}
  table{{width:100%;border-collapse:collapse;background:#fff;border-radius:8px;
         overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.08);margin-top:12px}}
  thead tr{{background:#0d3b2e;color:#fff}}
  th,td{{padding:11px 15px;text-align:left;border-bottom:1px solid #cde3d4;font-size:.9rem}}
  tbody tr:hover{{background:#f0f6f2}}
  tbody tr:last-child td{{border-bottom:none}}
  .lex{{font-family:'Consolas',monospace;color:#c0392b;font-size:.88rem}}
  .tok{{font-family:'Consolas',monospace;color:#2e7d8c;font-weight:600;font-size:.88rem}}
  .desc{{color:#922b21;font-size:.88rem}}
  .num{{color:#555;text-align:center;width:48px}}
  .pos{{color:#555;text-align:center}}
  .empty{{background:#fff;border-radius:8px;padding:24px;color:#27ae60;font-size:1rem;
          box-shadow:0 2px 8px rgba(0,0,0,.08);margin-top:12px}}
</style>
</head>
<body>
<header>
  <h1>LigaBot</h1>
  <span>Analisis Lexico - Fase 1</span>
</header>
<main>{body_content}</main>
</body>
</html>"""


def generate_token_report(tokens):
    _ensure_dir()
    path = os.path.join(REPORTES_DIR, 'Reporte_Token.html')
    now  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rows = ''.join(
        f"<tr>"
        f"<td class='num'>{i}</td>"
        f"<td class='lex'>{_escape(t.lexema)}</td>"
        f"<td class='tok'>{_escape(t.token_type)}</td>"
        f"<td class='pos'>{t.fila}</td>"
        f"<td class='pos'>{t.columna}</td>"
        f"</tr>"
        for i, t in enumerate(tokens, 1)
    )

    body = f"""
    <h2>Reporte de Tokens</h2>
    <p class="meta">Generado: {now} &nbsp;|&nbsp; Total de tokens: <strong>{len(tokens)}</strong></p>
    <table>
      <thead>
        <tr><th>#</th><th>Lexema</th><th>Token</th><th>Fila</th><th>Columna</th></tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>"""

    with open(path, 'w', encoding='utf-8') as f:
        f.write(_base_html('Reporte de Tokens - LigaBot', body))
    return path


def generate_error_report(errors):
    _ensure_dir()
    path = os.path.join(REPORTES_DIR, 'Reporte_Errores.html')
    now  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not errors:
        body = f"""
        <h2>Reporte de Errores Léxicos</h2>
        <p class="meta">Generado: {now}</p>
        <div class="empty">No se encontraron errores lexicos.</div>"""
    else:
        rows = ''.join(
            f"<tr>"
            f"<td class='num'>{i}</td>"
            f"<td class='lex'>{_escape(e.lexema)}</td>"
            f"<td class='desc'>{_escape(e.descripcion)}</td>"
            f"<td class='pos'>{e.fila}</td>"
            f"<td class='pos'>{e.columna}</td>"
            f"</tr>"
            for i, e in enumerate(errors, 1)
        )
        body = f"""
        <h2>Reporte de Errores Léxicos</h2>
        <p class="meta">Generado: {now} &nbsp;|&nbsp; Total de errores: <strong>{len(errors)}</strong></p>
        <table>
          <thead>
            <tr><th>#</th><th>Lexema</th><th>Descripción del error</th><th>Fila</th><th>Columna</th></tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>"""

    with open(path, 'w', encoding='utf-8') as f:
        f.write(_base_html('Reporte de Errores Lexicos - LigaBot', body))
    return path


def open_report(path):
    webbrowser.open(f'file:///{os.path.abspath(path).replace(chr(92), "/")}')



def _base_html_f2(title, body_content):
    """Plantilla HTML para reportes de Fase 2."""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{font-family:'Segoe UI',Arial,sans-serif;background:#edf3ee;color:#222}}
  header{{background:#0d3b2e;color:#fff;padding:16px 28px;display:flex;
          align-items:center;gap:16px;justify-content:space-between}}
  header h1{{font-size:1.2rem;font-weight:600}}
  header span{{font-size:.85rem;color:#7fc4a0}}
  main{{padding:28px;max-width:1200px;margin:0 auto}}
  h2{{color:#0d3b2e;margin-bottom:6px;font-size:1.3rem}}
  .meta{{color:#888;font-size:.85rem;margin-bottom:20px}}
  table{{width:100%;border-collapse:collapse;background:#fff;border-radius:8px;
         overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.08);margin-top:12px}}
  thead tr{{background:#0d3b2e;color:#fff}}
  th,td{{padding:11px 15px;text-align:left;border-bottom:1px solid #cde3d4;font-size:.9rem}}
  tbody tr:hover{{background:#f0f6f2}}
  tbody tr:last-child td{{border-bottom:none}}
  .num{{color:#555;text-align:center;width:52px}}
  .center{{text-align:center}}
  .pts{{font-weight:700;color:#0d3b2e;text-align:center}}
  .victoria{{color:#1a6b3c;font-weight:600}}
  .derrota{{color:#c0392b;font-weight:600}}
  .empate{{color:#e67e22;font-weight:600}}
  .lex{{font-family:'Consolas',monospace;color:#c0392b;font-size:.88rem}}
  .tok{{font-family:'Consolas',monospace;color:#2e7d8c;font-weight:600}}
  .empty{{background:#fff;border-radius:8px;padding:24px;color:#27ae60;
          box-shadow:0 2px 8px rgba(0,0,0,.08);margin-top:12px}}
  .badge{{display:inline-block;padding:2px 8px;border-radius:12px;
          font-size:.78rem;font-weight:600}}
  .badge-ok{{background:#d4edda;color:#155724}}
  .badge-err{{background:#f8d7da;color:#721c24}}
</style>
</head>
<body>
<header>
  <div>
    <h1>LigaBot</h1>
    <span>Analisis Sintactico y Chatbot - Fase 2</span>
  </div>
</header>
<main>{body_content}</main>
</body>
</html>"""


def generate_syntax_error_report(errors):
    """Genera Reporte_Errores_S.html con los errores sintácticos acumulados."""
    _ensure_dir()
    path = os.path.join(REPORTES_DIR, 'Reporte_Errores_S.html')
    now  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not errors:
        body = f"""
        <h2>Reporte de Errores Sintácticos</h2>
        <p class="meta">Generado: {now}</p>
        <div class="empty">No se encontraron errores sintacticos.</div>"""
    else:
        rows = ''
        for i, e in enumerate(errors, 1):
            recv = (f"'{_escape(e.received.lexema)}' ({_escape(e.received.token_type)})"
                    if e.received else 'EOF')
            rows += (f"<tr><td class='num'>{i}</td>"
                     f"<td class='lex'>{recv}</td>"
                     f"<td class='tok'>{_escape(e.expected)}</td>"
                     f"<td class='center'>{e.fila}</td>"
                     f"<td class='center'>{e.col}</td></tr>")
        body = f"""
        <h2>Reporte de Errores Sintácticos</h2>
        <p class="meta">Generado: {now} &nbsp;|&nbsp;
           Total de errores: <strong>{len(errors)}</strong></p>
        <table>
          <thead>
            <tr><th>#</th><th>Token recibido</th><th>Token esperado</th>
                <th>Fila</th><th>Columna</th></tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>"""

    with open(path, 'w', encoding='utf-8') as f:
        f.write(_base_html_f2('Reporte de Errores Sintacticos - LigaBot', body))
    return path


def generate_jornada_report(partidos, jornada, temporada, nombre):
    """Genera {nombre}.html con los partidos de una jornada."""
    _ensure_dir()
    safe = nombre.replace('/', '_').replace('\\', '_')
    path = os.path.join(REPORTES_DIR, f'{safe}.html')
    now  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rows = ''
    for i, r in enumerate(partidos, 1):
        g1, g2 = int(r['Goles1']), int(r['Goles2'])
        if g1 > g2:
            res = f"<span class='victoria'>{_escape(r['Equipo1'])}</span>"
        elif g2 > g1:
            res = f"<span class='victoria'>{_escape(r['Equipo2'])}</span>"
        else:
            res = "<span class='empate'>Empate</span>"
        rows += (f"<tr><td class='num'>{i}</td>"
                 f"<td>{_escape(r['Equipo1'])}</td>"
                 f"<td>{_escape(r['Equipo2'])}</td>"
                 f"<td class='center'>{g1}</td>"
                 f"<td class='center'>{g2}</td>"
                 f"<td>{res}</td></tr>")

    body = f"""
    <h2>Jornada {jornada} - Temporada {_escape(temporada)}</h2>
    <p class="meta">Generado: {now} &nbsp;|&nbsp; Partidos: <strong>{len(partidos)}</strong></p>
    <table>
      <thead>
        <tr><th>#</th><th>Equipo Local</th><th>Equipo Visitante</th>
            <th>Goles Local</th><th>Goles Visitante</th><th>Ganador</th></tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>"""

    with open(path, 'w', encoding='utf-8') as f:
        f.write(_base_html_f2(f'Jornada {jornada} - LigaBot', body))
    return path


def generate_tabla_report(tabla, temporada, nombre):
    """Genera {nombre}.html con la tabla de posiciones."""
    _ensure_dir()
    safe = nombre.replace('/', '_').replace('\\', '_')
    path = os.path.join(REPORTES_DIR, f'{safe}.html')
    now  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rows = ''
    for r in tabla:
        dg_str = f"+{r['dg']}" if r['dg'] > 0 else str(r['dg'])
        rows += (f"<tr><td class='num'>{r['pos']}</td>"
                 f"<td><strong>{_escape(r['equipo'])}</strong></td>"
                 f"<td class='center'>{r['pj']}</td>"
                 f"<td class='center'>{r['g']}</td>"
                 f"<td class='center'>{r['e']}</td>"
                 f"<td class='center'>{r['p']}</td>"
                 f"<td class='center'>{r['gf']}</td>"
                 f"<td class='center'>{r['gc']}</td>"
                 f"<td class='center'>{dg_str}</td>"
                 f"<td class='pts'>{r['pts']}</td></tr>")

    body = f"""
    <h2>Tabla de Posiciones - Temporada {_escape(temporada)}</h2>
    <p class="meta">Generado: {now} &nbsp;|&nbsp; Equipos: <strong>{len(tabla)}</strong></p>
    <table>
      <thead>
        <tr><th>Pos</th><th>Equipo</th><th>PJ</th><th>G</th><th>E</th>
            <th>P</th><th>GF</th><th>GC</th><th>DG</th><th>Pts</th></tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>"""

    with open(path, 'w', encoding='utf-8') as f:
        f.write(_base_html_f2(f'Tabla {temporada} - LigaBot', body))
    return path


def generate_partidos_report(partidos, equipo, temporada, nombre):
    """Genera {nombre}.html con los partidos de un equipo."""
    _ensure_dir()
    safe = nombre.replace('/', '_').replace('\\', '_')
    path = os.path.join(REPORTES_DIR, f'{safe}.html')
    now  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rows = ''
    for r in partidos:
        res = r.get('resultado_equipo', '')
        cls = {'Victoria': 'victoria', 'Derrota': 'derrota', 'Empate': 'empate'}.get(res, '')
        rows += (f"<tr><td class='num'>{r['Jornada']}</td>"
                 f"<td>{_escape(r['Equipo1'])}</td>"
                 f"<td>{_escape(r['Equipo2'])}</td>"
                 f"<td class='center'>{r['Goles1']} - {r['Goles2']}</td>"
                 f"<td class='{cls}'>{_escape(res)}</td></tr>")

    body = f"""
    <h2>Partidos de {_escape(equipo)} - Temporada {_escape(temporada)}</h2>
    <p class="meta">Generado: {now} &nbsp;|&nbsp; Partidos: <strong>{len(partidos)}</strong></p>
    <table>
      <thead>
        <tr><th>Jornada</th><th>Local</th><th>Visitante</th>
            <th>Marcador</th><th>Resultado para {_escape(equipo)}</th></tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>"""

    with open(path, 'w', encoding='utf-8') as f:
        f.write(_base_html_f2(f'Partidos {equipo} - LigaBot', body))
    return path
