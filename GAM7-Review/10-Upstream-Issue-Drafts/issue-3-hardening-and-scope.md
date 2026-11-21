Title: Small hardening items: parameterized SQL in gcloud reauth, md5 on FIPS, Cloud Channel readonly scope

1. runSqliteQuery builds its SQL with an f-string containing admin_email, and
   never closes the connection. Suggest binding the value:
       runSqliteQuery(token_file,
           'SELECT rapt_token FROM access_tokens WHERE account_id = ?', (admin_email,))
   with params passed to curr.execute(query, params) and conn.close() in a
   finally block. Low practical risk, but easy to remove.

2. md5MatchesFile uses hashlib.md5(), which raises ValueError on FIPS-enabled
   systems. It only compares a file with Drive's md5Checksum, so
   hashlib.md5(usedforsecurity=False) is correct and avoids the crash.

3. Question: the Cloud Channel entry in _CLIENT_SCOPES has 'subscopes': READONLY,
   so GAM can request https://www.googleapis.com/auth/apps.order.readonly. The
   Cloud Channel discovery document lists only apps.order and
   apps.reports.usage.readonly. Does Google accept apps.order.readonly for this
   API? If not, choosing the readonly option in `gam oauth create` may be
   rejected. (I could not test this without a tenant.)
