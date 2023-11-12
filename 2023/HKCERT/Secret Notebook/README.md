We have been provided with the server code for this challenge - looks like our goal is to get the value of the flag through either:
- Getting access to the Administrator account
- Getting access to the Administrator's secret node through SQL injects

For this challenge, option 2 seems the most likely, since in the app.py file there are a bunch of SQL query functions.
All of them, except for two, are prepared statements.

One of the two that isn't a prepared statement is used during init (so we can't do that), but the second one is in the `doGetPublicNotes` function, which is tied to the
noteType=public.

Two parameters is passed to this: column (request.args.get("column")) and ascending (request.args.get("ascending")).

The following is the query: `SELECT username, publicnote FROM users ORDER BY {column} {ascending};`

Sadly, the column variable is checked for SQL injects, so we can't do anything there.

However, the ascending variable is not checked, so we might be able to do some fun there:

```
if column and not isInputValid(column):
    abort(403)
if ascending  != "ASC":
    ascending = "DESC"
```

ascending is a str (https://flask.palletsprojects.com/en/2.3.x/api/#flask.Request.args)
