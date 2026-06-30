# data_source.py - Fuente de datos CSV para LigaBot  (Fase 2)
#
# Carga LaLigaBot-LFP.csv y expone metodos de consulta.
# Columnas del CSV: Fecha | Temporada | Jornada | Equipo1 | Equipo2 | Goles1 | Goles2
#   Equipo1 = local   Goles1 = goles locales
#   Equipo2 = visitante  Goles2 = goles visitantes
#
# Las comparaciones de equipo son case-insensitive y toleran variaciones de
# acentuacion (normalizacion NFD -> ASCII).

import csv
import os
import unicodedata

_CSV_DEFAULT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            'LaLigaBot-LFP.csv')


def _norm(text):
    """Normaliza a minúsculas sin acentos para comparación tolerante."""
    return unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode().lower()


class DataSource:
    """
    Carga el CSV y proporciona todos los métodos de consulta requeridos.

    Atributos públicos:
        loaded  - True si el CSV fue cargado correctamente.
        error   - Mensaje de error si la carga fallo (None en caso de exito).
        path    - Ruta del archivo CSV.
    """

    def __init__(self, csv_path=None):
        self.path   = csv_path or _CSV_DEFAULT
        self.rows   = []        # lista de dicts con las columnas del CSV
        self.loaded = False
        self.error  = None
        self._load()

    # -- Carga ------------------------------------------------------------------

    def _load(self):
        try:
            with open(self.path, encoding='latin-1', newline='') as f:
                reader = csv.DictReader(f)
                self.rows = list(reader)
            self.loaded = True
        except FileNotFoundError:
            self.error  = f"Archivo no encontrado: {self.path}"
        except Exception as exc:
            self.error  = str(exc)

    # -- Helpers internos -------------------------------------------------------

    def _rows_temporada(self, temporada):
        return [r for r in self.rows if r['Temporada'] == temporada]

    def _match_equipo(self, row_eq, equipo_norm):
        return _norm(row_eq) == equipo_norm

    def _equipo_en_fila(self, row, equipo_norm):
        return (self._match_equipo(row['Equipo1'], equipo_norm) or
                self._match_equipo(row['Equipo2'], equipo_norm))

    # -- Consultas --------------------------------------------------------------

    def get_resultado(self, local, visitante, temporada):
        """
        Retorna la fila del partido exacto (local vs visitante en la temporada)
        o None si no se encontró.
        """
        ln = _norm(local)
        vn = _norm(visitante)
        for r in self._rows_temporada(temporada):
            if (self._match_equipo(r['Equipo1'], ln) and
                    self._match_equipo(r['Equipo2'], vn)):
                return r
        return None

    def get_goles_local(self, equipo, temporada):
        """Suma de goles anotados por el equipo actuando como local."""
        en = _norm(equipo)
        return sum(int(r['Goles1']) for r in self._rows_temporada(temporada)
                   if self._match_equipo(r['Equipo1'], en))

    def get_goles_visitante(self, equipo, temporada):
        """Suma de goles anotados por el equipo actuando como visitante."""
        en = _norm(equipo)
        return sum(int(r['Goles2']) for r in self._rows_temporada(temporada)
                   if self._match_equipo(r['Equipo2'], en))

    def get_goles_total(self, equipo, temporada):
        """Suma total de goles (local + visitante)."""
        return (self.get_goles_local(equipo, temporada) +
                self.get_goles_visitante(equipo, temporada))

    def get_jornada(self, jornada, temporada):
        """Lista de partidos de una jornada específica."""
        return [r for r in self._rows_temporada(temporada)
                if int(r['Jornada']) == jornada]

    def get_tabla(self, temporada):
        """
        Calcula la tabla de posiciones de la temporada.
        Puntuación: Victoria = 3 pts, Empate = 1 pt, Derrota = 0 pts.
        Orden: puntos desc, diferencia de goles desc, goles a favor desc.
        Retorna lista de dicts con: equipo, pj, g, e, p, gf, gc, dg, pts.
        """
        stats = {}
        for r in self._rows_temporada(temporada):
            e1, e2 = r['Equipo1'], r['Equipo2']
            g1, g2 = int(r['Goles1']), int(r['Goles2'])
            for eq in (e1, e2):
                if eq not in stats:
                    stats[eq] = {'equipo': eq, 'pj': 0, 'g': 0, 'e': 0,
                                 'p': 0, 'gf': 0, 'gc': 0, 'pts': 0}
            # actualizar estadísticas
            stats[e1]['pj'] += 1;  stats[e2]['pj'] += 1
            stats[e1]['gf'] += g1; stats[e1]['gc'] += g2
            stats[e2]['gf'] += g2; stats[e2]['gc'] += g1
            if g1 > g2:
                stats[e1]['g']   += 1; stats[e1]['pts'] += 3
                stats[e2]['p']   += 1
            elif g2 > g1:
                stats[e2]['g']   += 1; stats[e2]['pts'] += 3
                stats[e1]['p']   += 1
            else:
                stats[e1]['e']   += 1; stats[e1]['pts'] += 1
                stats[e2]['e']   += 1; stats[e2]['pts'] += 1

        tabla = sorted(stats.values(),
                       key=lambda x: (-x['pts'],
                                      -(x['gf'] - x['gc']),
                                      -x['gf']))
        for i, row in enumerate(tabla, 1):
            row['pos'] = i
            row['dg']  = row['gf'] - row['gc']
        return tabla

    def get_partidos(self, equipo, temporada, ji=None, jf=None):
        """
        Lista de partidos del equipo en la temporada.
        ji / jf: jornada inicial / final (inclusivo).
        Retorna cada fila enriquecida con 'resultado_equipo':
          'Victoria', 'Derrota' o 'Empate' desde la perspectiva del equipo.
        """
        en = _norm(equipo)
        rows = []
        for r in self._rows_temporada(temporada):
            jornada = int(r['Jornada'])
            if ji is not None and jornada < ji:
                continue
            if jf is not None and jornada > jf:
                continue
            if not self._equipo_en_fila(r, en):
                continue
            g1, g2 = int(r['Goles1']), int(r['Goles2'])
            es_local = self._match_equipo(r['Equipo1'], en)
            if g1 == g2:
                res = 'Empate'
            elif es_local and g1 > g2:
                res = 'Victoria'
            elif not es_local and g2 > g1:
                res = 'Victoria'
            else:
                res = 'Derrota'
            rows.append({**r, 'resultado_equipo': res})
        return sorted(rows, key=lambda x: int(x['Jornada']))

    def get_top_superior(self, temporada, n=5):
        """Primeros N equipos de la tabla (mayor puntaje)."""
        return self.get_tabla(temporada)[:n]

    def get_top_inferior(self, temporada, n=5):
        """Últimos N equipos de la tabla (menor puntaje), orden ascendente a partir del fondo."""
        tabla = self.get_tabla(temporada)
        return list(reversed(tabla[-n:]))

    def get_seasons(self):
        """Lista de temporadas disponibles en el CSV."""
        return sorted(set(r['Temporada'] for r in self.rows))

    def exists_temporada(self, temporada):
        return any(r['Temporada'] == temporada for r in self.rows)

    def exists_equipo(self, equipo, temporada):
        en = _norm(equipo)
        return any(self._equipo_en_fila(r, en)
                   for r in self._rows_temporada(temporada))
