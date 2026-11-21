Title: printDriveActivity user lookup uses dotted field mask `name.fullName`

GAM version: 7.52.05 (source at commit 30449fc)

In printDriveActivity._getUserInfo (line ~58642):

    result = callGAPI(cd.users(), 'get', ..., userKey=userId,
                      fields='primaryEmail,name.fullName')

Google's partial-response `fields` syntax uses `/` or parentheses for nested
fields (`name/fullName` or `name(fullName)`); a dot is not part of it. Other
places in GAM already write this lookup as `fields='name(fullName)'` (for
example near lines 24515 and 52013).

If the dotted form is rejected with a 400, the except clause that follows
(`GAPI.badRequest`) swallows it and the user is shown as `uid:<id>` / Unknown in
Drive Activity output, with no error. I could not test against a live domain,
so please treat the "rejected" part as likely rather than confirmed; the
parenthesized form is valid either way.

Suggested change:

    -  userKey=userId, fields='primaryEmail,name.fullName')
    +  userKey=userId, fields='primaryEmail,name(fullName)')

Found by a static check that parses every literal `fields=` string and walks
it through the response schema in Google's discovery document (297 strings
checked; this was the only one with an unknown name).
