"""User-group request values must reach MySQL as bound values or checked ids, never as SQL text.

POST /user_group takes `name` (a string) and POST/DELETE /user_group/<id>/staff take `user_ids` (a list whose items
are not type-checked). db/user_group/db_group_mgr.py formatted the name into "name = '%s'" and each user id, after
eval(str(list)), into "user_id =%s" unquoted. The test runs DBGroupMgr with the real db/base.py SQL builders and a
recording connection, and checks: the group name never appears in a SELECT's text and is passed as an argument; a user
id that is not an integer never reaches any statement; ordinary values still produce the same statements.

Run from the repository root: python -m unittest tests/test_group_sql_values.py
"""
import importlib.util, sys, types, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = []


class Cur:
    def __init__(self): self.rows = []
    def execute(self, sql, args=None): LOG.append((sql, args)); return 1
    def fetchone(self): return {"id": 5} if LOG and LOG[-1][0].startswith("select id") else None
    def fetchall(self): return []


class Conn:
    def __init__(self): self.cur = Cur(); self.conn = types.SimpleNamespace(commit=lambda: None, rollback=lambda: None)
    def close(self): pass


def load():
    def mod(name, **attrs):
        m = types.ModuleType(name); m.__dict__.update(attrs); m.__path__ = []; sys.modules[name] = m; return m
    for n in ("common", "db", "db.user", "db.user_group", "utils"):
        mod(n)
    mod("common.common_time", get_system_datetime=lambda: "2026-11-23 00:00:00")
    mod("config", configuration=types.SimpleNamespace(get_database_name=lambda: "app"))
    mod("db.connection_pool", MysqlConn=Conn)
    mod("db.user.db_user_mgr", user_mgr=None)
    mod("utils.log_helper", lg=types.SimpleNamespace(error=lambda *a: None, info=lambda *a: None))
    mod("utils.status_code", response_code=types.SimpleNamespace(
        **{k: k for k in ("SUCCESS", "RECORD_EXIST", "ADD_DATA_FAIL", "DELETE_DATA_FAIL", "GET_DATA_FAIL",
                          "UPDATE_DATA_FAIL")}))
    for name, path in (("db.base", "db/base.py"), ("db.user_group.db_group_mgr", "db/user_group/db_group_mgr.py")):
        spec = importlib.util.spec_from_file_location(name, ROOT / path)
        m = importlib.util.module_from_spec(spec); sys.modules[name] = m; spec.loader.exec_module(m)
    return m.DBGroupMgr()


class GroupSqlTest(unittest.TestCase):
    def setUp(self):
        LOG.clear(); self.mgr = load()

    def test_group_name_is_bound(self):
        name = "ops' or '1'='1"
        self.mgr.get_user_group_by_name(name)
        self.mgr.add_group(name, "d", [])
        selects = [(s, a) for s, a in LOG if s.lower().startswith("select")]
        self.assertTrue(selects)
        for sql, args in selects:
            self.assertNotIn(name, sql, "group name written into the SQL text")
            self.assertIn(name, tuple(args or ()), "group name not passed as an argument")

    def test_user_ids_must_be_integers(self):
        bad = str(["1 or 1=1"])
        self.mgr.add_user_to_group(7, bad)
        self.mgr.remove_group_users(7, bad)
        for sql, args in LOG:
            self.assertNotIn("1=1", sql, "user id written into the SQL text")

    def test_ordinary_ids_still_work(self):
        self.mgr.remove_group_users(7, str([3, "4"]))
        sqls = [s for s, a in LOG]
        self.assertIn("select * from app.user_user_group where user_id =3 and group_id=7", sqls)
        self.assertIn("select * from app.user_user_group where user_id =4 and group_id=7", sqls)


if __name__ == "__main__":
    unittest.main()
