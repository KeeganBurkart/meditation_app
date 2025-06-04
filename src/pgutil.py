class PGConnectionWrapper:
    """Wrap a psycopg2 connection to expose a SQLite-like execute() method."""
    def __init__(self, conn):
        self._conn = conn

    def execute(self, query, params=None):
        query = query.replace("?", "%s")
        cur = self._conn.cursor()
        if params is None:
            cur.execute(query)
        else:
            cur.execute(query, params)
        return cur

    def executemany(self, query, seq):
        query = query.replace("?", "%s")
        cur = self._conn.cursor()
        cur.executemany(query, seq)
        return cur

    def __getattr__(self, name):
        return getattr(self._conn, name)

