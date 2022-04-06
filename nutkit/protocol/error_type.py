"""Enumerate all the error types in the drivers."""
from enum import Enum


class ErrorType(Enum):
    # routing
    # - interrupting nodes
    # - no writers available
    # - connectivity issues
    SESSION_EXPIRED_ERROR = "SessionExpiredError"

    # discovery
    # - procedure not found on discovery
    # - unknown code
    # - no readers in routing table (to be checked in "go", "java", "dotnet")
    # - unreachable db discovery
    # direct
    # - connectivity issues
    SERVICE_UNAVAILABLE_ERROR = "ServiceUnavailableError"

    # TO BE DISCUSSED
    # java wraps it into SESSION_EXPIRED_ERROR to signify that it is retryable
    # python seems to expose it directly
    # routing
    # - Neo.ClientError.Cluster.NotALeader
    NOT_LEADER_ERROR = "NotLeaderError"

    # TO BE DISCUSSED
    # java wraps it into SESSION_EXPIRED_ERROR to signify that it is retryable
    # python seems to expose it directly
    # routing
    # - Neo.ClientError.General.ForbiddenOnReadOnlyDatabase
    FORBIDDEN_ON_RO_DB_ERROR = "ForbiddenOnReadOnlyDatabaseError"

    # routing
    # - Neo.ClientError.General.DatabaseUnavailable
    # - Neo.ClientError.Transaction.InvalidBookmark during discovery on run
    # - Neo.ClientError.Transaction.InvalidBookmarkMixture during discovery on
    #       run
    # - no available connections in pool
    # - invalid bookmark
    CLIENT_ERROR = "ClientError"

    # TO BE DISCUSSED
    # java has a dedicated subtype of client error
    # python seems to expose it as client error
    # discovery
    # - Neo.ClientError.Database.DatabaseNotFound
    FATAL_DISCOVERY_ERROR = "FatalDiscoveryError"

    # TO BE DISCUSSED
    # java exposes this a security exception subtype of client exception
    # python seems to expose it as client error
    # discovery
    # - Neo.ClientError.Security.Forbidden
    # - Neo.ClientError.Security.MadeUpSecurityError (any security error)
    SECURITY_ERROR = "SecurityError"

    # TO BE DISCUSSED
    # see above
    FORBIDDEN_ERROR = "SecurityError"

    # general usage
    # - driver closed
    # - id access when numeric id is not available
    ILLEGAL_STATE_ERROR = "IllegalStateError"

    # no routing
    # - Neo.TransientError.General.DatabaseUnavailable
    # - Neo.TransientError.Transaction.LockClientStopped
    TRANSIENT_ERROR = "TransientError"

    # TO BE DISCUSSED
    # python seems to return TransientError
    # auth
    # - Neo.ClientError.Security.AuthorizationExpired
    AUTH_EXPIRED_ERROR = "AuthorizationExpiredError"

    # TO BE DISCUSSED
    # dotnet seems to return ClientError
    # auth
    # - Neo.ClientError.Security.TokenExpired
    TOKEN_EXPIRED_ERROR = "TokenExpiredError"

    # when result is not a single entry
    NOT_SINGLE_ERROR = "NotSingleError"

    # TO BE DISCUSSED
    # python throws ConfigurationError when db name is used over Bolt 3.0
    # also throws when impersonation is used on Bolt < 4.4
    # java throws client exception
    INVALID_CONF_ERROR = "InvalidConfigurationError"

    # TO BE DISCUSSED
    # direct
    # dotnet throws this on read timeout
    # others seems to throw session expired WHEN in routing mode
    # in direct mode python throws service unavailable
    # dotnet and java throw read timeout, in java it extends service
    # unavailable
    CONNECTION_READ_TIMEOUT_ERROR = "ConnectionReadTimeoutError"

    # TO BE DISCUSSED
    # direct
    # python throws when connection drops after commit
    # java throws service unavailable error
    # there is a test that expects retry to be interrupted, java and dotnet
    # keep trying
    INCOMPLETE_COMMIT_ERROR = "IncompleteCommitError"

    # TO BE DISCUSSED
    # direct
    # go throws this
    # others seems to throw service unavailable
    CONNECTIVITY_ERROR = "ConnectivityError"

    # direct
    # - when result has been consumed
    RESULT_CONSUMED_ERROR = "ResultConsumedError"

    # configuration
    # - illegal argument value
    ILLEGAL_ARGUMENT_ERROR = "IllegalArgumentError"

    # protocol violations
    PROTOCOL_ERROR = "ProtocolError"

    # TO BE DISCUSSED
    # python throws when transaction has been closed
    # java throws client exception
    TRANSACTION_ERROR = "TransactionError"

    # unexpected agent string returned by server
    UNTRUSTED_SERVER_ERROR = "UntrustedServerError"
