import os
import webbrowser
from datetime import datetime

REPORTES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reportes')


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
  <span>Análisis Léxico — Fase 1</span>
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
        f.write(_base_html('Reporte de Tokens — LigaBot', body))
    return path


def generate_error_report(errors):
    _ensure_dir()
    path = os.path.join(REPORTES_DIR, 'Reporte_Errores.html')
    now  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not errors:
        body = f"""
        <h2>Reporte de Errores Léxicos</h2>
        <p class="meta">Generado: {now}</p>
        <div class="empty">&#10003; No se encontraron errores léxicos.</div>"""
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
        f.write(_base_html('Reporte de Errores Léxicos — LigaBot', body))
    return path


def open_report(path):
    webbrowser.open(f'file:///{os.path.abspath(path).replace(chr(92), "/")}')
