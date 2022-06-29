from nutkit import protocol as types
from nutkit.frontend import Driver
from tests.shared import (
    driver_feature,
    TestkitTestCase,
)
from tests.stub.shared import StubServer


class _TestTemporalTypes(TestkitTestCase):

    required_features = types.Feature.API_TYPE_TEMPORAL,
    bolt_version = None

    def setUp(self):
        super().setUp()
        self._server = StubServer(9010)
        self._session = None
        self._driver = None

    def tearDown(self):
        if self._session is not None:
            self._session.close()
        if self._driver is not None:
            self._driver.close()
        self._server.reset()
        super().tearDown()

    def _start_server(self, script):
        version_folder = "v{}".format(self.bolt_version.replace(".", "x"))
        self._server.start(path=self.script_path(version_folder, script))

    def _create_direct_driver(self):
        uri = "bolt://%s" % self._server.address
        auth = types.AuthorizationToken("basic", principal="", credentials="")
        self._driver = Driver(self._backend, uri, auth)

    def _test_date_time(self):
        self._start_server("echo_date_time.script")
        self._create_direct_driver()
        self._session = self._driver.session("w")
        result = self._session.run("RETURN $dt AS dt", params={
            "dt": types.CypherDateTime(2022, 6, 7, 11, 52, 5, 0,
                                       utc_offset_s=7200)
        })
        list(result)

    def _test_zoned_date_time(self):
        self._start_server("echo_zoned_date_time.script")
        self._create_direct_driver()
        self._session = self._driver.session("w")
        result = self._session.run("RETURN $dt AS dt", params={
            "dt": types.CypherDateTime(
                2022, 6, 7, 11, 52, 5, 0,
                utc_offset_s=7200, timezone_id="Europe/Stockholm"
            )
        })
        list(result)


class _TestTemporalTypesPatchedBolt(_TestTemporalTypes):

    @driver_feature(types.Feature.BOLT_PATCH_UTC)
    def _test_date_time_with_patch(self):
        self._start_server("echo_date_time_patched.script")
        self._create_direct_driver()
        self._session = self._driver.session("w")
        result = self._session.run("RETURN $dt AS dt", params={
            "dt": types.CypherDateTime(2022, 6, 7, 11, 52, 5, 0,
                                       utc_offset_s=7200)
        })
        list(result)

    @driver_feature(types.Feature.BOLT_PATCH_UTC)
    def _test_zoned_date_time_with_patch(self):
        self._start_server("echo_zoned_date_time_patched.script")
        self._create_direct_driver()
        self._session = self._driver.session("w")
        result = self._session.run("RETURN $dt AS dt", params={
            "dt": types.CypherDateTime(
                2022, 6, 7, 11, 52, 5, 0,
                utc_offset_s=7200, timezone_id="Europe/Stockholm"
            )
        })
        list(result)


class TestTemporalTypesV3x0(_TestTemporalTypes):

    required_features = (
        *_TestTemporalTypes.required_features,
        types.Feature.BOLT_3_0,
    )
    bolt_version = "3.0"

    def test_date_time(self):
        super()._test_date_time()

    def test_zoned_date_time(self):
        super()._test_zoned_date_time()


class TestTemporalTypesV4x1(_TestTemporalTypes):
    required_features = (
        *_TestTemporalTypes.required_features,
        types.Feature.BOLT_4_1,
    )
    bolt_version = "4.1"

    def test_date_time(self):
        super()._test_date_time()

    def test_zoned_date_time(self):
        super()._test_zoned_date_time()


class TestTemporalTypesV4x2(_TestTemporalTypes):

    required_features = (
        *_TestTemporalTypes.required_features,
        types.Feature.BOLT_4_2,
    )
    bolt_version = "4.2"

    def test_date_time(self):
        super()._test_date_time()

    def test_zoned_date_time(self):
        super()._test_zoned_date_time()


class TestTemporalTypesV4x3(_TestTemporalTypesPatchedBolt):

    required_features = (
        *_TestTemporalTypes.required_features,
        types.Feature.BOLT_4_3,
    )
    bolt_version = "4.3"

    def test_date_time(self):
        super()._test_date_time()

    def test_date_time_with_patch(self):
        super()._test_date_time_with_patch()

    def test_zoned_date_time(self):
        super()._test_zoned_date_time()

    def test_zoned_date_time_with_patch(self):
        super()._test_zoned_date_time_with_patch()


class TestTemporalTypesV4x4(_TestTemporalTypesPatchedBolt):

    required_features = (
        *_TestTemporalTypes.required_features,
        types.Feature.BOLT_4_4,
    )
    bolt_version = "4.4"

    def test_date_time(self):
        super()._test_date_time()

    def test_date_time_with_patch(self):
        super()._test_date_time_with_patch()

    def test_zoned_date_time(self):
        super()._test_zoned_date_time()

    def test_zoned_date_time_with_patch(self):
        super()._test_zoned_date_time_with_patch()


class TestTemporalTypesV5x0(_TestTemporalTypes):

    required_features = (
        *_TestTemporalTypes.required_features,
        types.Feature.BOLT_5_0,
    )
    bolt_version = "5.0"

    def test_date_time(self):
        super()._test_date_time()

    def test_zoned_date_time(self):
        super()._test_zoned_date_time()