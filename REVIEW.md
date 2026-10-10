# REVIEW.md

List every defect you found in the starter `app/main.py` (helpers and endpoints). For each one:

| # | Where (function / line) | What is wrong | How you'd notice it (test, input, or symptom) | How you fixed it |
|---|---|---|---|---|
| 1 | punch_in() (line 103) | When the supplied emp_code that does not exists, the database returns None. The function attemps to access emp["shift_start"], causing a TypeError and a server error instead of the required 404 response. | A test that calls POST /attendance/punch-in with an unknown employee code. Before the fix, the request caused a TypeError, after the fix the test passed with HTTP 404. | Added an employee existence check immediately after the databse lookup. If the employee is missing, the endpoint raises an HTTPException with status code 404. |

Also note anything you looked at and decided was **not** a defect, and why.
