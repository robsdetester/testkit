from nutkit.frontend import Driver
import nutkit.protocol as types
from tests.shared import (
    get_driver_name,
    TestkitTestCase,
)
from tests.stub.shared import StubServer


class TestIterationTxRun(TestkitTestCase):
    def setUp(self):
        super().setUp()
        self._server = StubServer(9001)

    def tearDown(self):
        self._server.reset()
        super().tearDown()

    def _iterate(self, n, script_fn, expected_sequence, expected_error=False):
        uri = "bolt://%s" % self._server.address
        driver = Driver(self._backend, uri,
                        types.AuthorizationToken(scheme="basic"))
        self._server.start(path=self.script_path(script_fn))
        session = driver.session("w", fetchSize=n)
        tx = session.beginTransaction()
        result = tx.run("CYPHER")
        got_error = False
        sequence = []
        while True:
            try:
                next_ = result.next()
            except types.DriverError:
                got_error = True
                break
            if isinstance(next_, types.NullRecord):
                break
            sequence.append(next_.values[0].value)
        tx.commit()
        driver.close()
        self._server.done()
        self.assertEqual(expected_sequence, sequence)
        self.assertEqual(expected_error, got_error)

    def test_all(self):
        self._iterate(2, "tx_pull_2.script", [1, 2, 3])

    def test_nested(self):
        # ex JAVA - java completely pulls the first query before running the second
        if get_driver_name() in ["java"]:
            self.skipTest(
                "completely pulls the first query before running the second"
            )
        uri = "bolt://%s" % self._server.address
        driver = Driver(self._backend, uri,
                        types.AuthorizationToken(scheme="basic"))
        self._server.start(path=self.script_path("tx_pull_1_nested.script"))
        session = driver.session("w", fetchSize=1)
        tx = session.beginTransaction()
        res1 = tx.run("CYPHER")
        seq = []
        seqs = []
        while True:
            rec1 = res1.next()
            if isinstance(rec1, types.NullRecord):
                break
            seq.append(rec1.values[0].value)
            seq2 = []
            res2 = tx.run("CYPHER")
            while True:
                rec2 = res2.next()
                if isinstance(rec2, types.NullRecord):
                    break
                seq2.append(rec2.values[0].value)
            seqs.append(seq2)

        tx.commit()
        driver.close()
        self._server.done()
        self.assertEqual(["1_1", "1_2"], seq)
        self.assertEqual([["2_1", "2_2"], ["3_1"]], seqs)

