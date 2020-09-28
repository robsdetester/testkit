import unittest, os

from tests.shared import *
from tests.stub.shared import *
from nutkit.frontend import Driver, AuthorizationToken
import nutkit.protocol as types


class TxRun(unittest.TestCase):
    def setUp(self):
        self._backend = new_backend()
        self._server = StubServer(9001)
        self._driverName = get_driver_name()
        uri = "bolt://%s" % self._server.address
        self._driver = Driver(self._backend, uri, AuthorizationToken(scheme="basic"))

    def tearDown(self):
        self._driver.close()
        self._backend.close()
        # If test raised an exception this will make sure that the stub server
        # is killed and it's output is dumped for analys.
        self._server.reset()

    # Tests that a committed transaction can return the last bookmark
    def test_last_bookmark(self):
        script = "txrun_commit.script"
        if self._driverName in ["go"]:
            script = "txrun_commit_all.script"
        elif self._driverName not in ["dotnet"]:
            self.skipTest("session.lastBookmark not implemented in backend")

        self._server.start(path=os.path.join(scripts_path, script))
        session = self._driver.session("w")
        tx = session.beginTransaction()
        tx.run("RETURN 1 as n")
        tx.commit()
        bookmarks = session.lastBookmarks()
        session.close()

        self.assertEqual(bookmarks, ["bm"])
