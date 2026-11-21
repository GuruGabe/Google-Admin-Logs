Title: Classroom remove-items retry passes `body` to delete and aborts

GAM version: 7.52.05 (source at commit 30449fc)

In _batchRemoveItemsFromCourse, the retry that runs after a quotaExceeded or
serviceNotAvailable error calls:

    callGAPI(service, 'delete', ...,
             courseId=addCourseIdScope(ri[RI_ENTITY]), body=rbody, fields='')

where rbody is {attribute: item} and attribute is userId, alias or id.
courses.students/teachers/aliases/topics/announcements delete methods take
courseId plus userId/alias/id as parameters and have no request body, so the
retry stops GAM instead of retrying:

    ERROR: Got an unexpected keyword argument body

Verified with GAM's own callGAPI and a mocked HTTP response using Google's
current Classroom discovery document: the current call shape aborts, and the
call below returns normally.

Fix, around line 53537 of src/gam/__init__.py:

    -                 courseId=addCourseIdScope(ri[RI_ENTITY]), body=rbody, fields='')
    +                 courseId=addCourseIdScope(ri[RI_ENTITY]), fields='', **rbody)

Only the retry path is affected, so it shows up on large removals or busy
periods rather than every run.
