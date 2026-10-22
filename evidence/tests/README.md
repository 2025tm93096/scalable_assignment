# Test Evidence

- [result.json](result.json): timestamped scripted happy path across all four services.
- `pytest.txt` and `junit.xml`: captured full-suite output and machine-readable results.
- [database-isolation.json](database-isolation.json): each distinct service login has CONNECT only to its own application database.
- [browser-desktop.png](browser-desktop.png) and [browser-mobile.png](browser-mobile.png): actual desktop and 390px mobile browser views; loaded images and no page-level horizontal overflow verified.

Run the README test commands against live services and a separate test database.
Browser screenshots supplement API evidence; challenge scripts and raw logs are the
primary correctness evidence. Team-recorded terminal screenshots should include the
command, output and timestamp. No claims about unexecuted tests or recorded videos.