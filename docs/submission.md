# Submission Work Still Owned by the Team

## Links

- GitHub repository visible to faculty: TODO
- Google Drive folder with final PDF/video: TODO
- 8-10 minute demo video: TODO
- Team member names and student IDs: TODO

No repository has been published and no video has been recorded by this application.

## Contribution Appendix

| Student / ID | Implemented capability | Reviewed capability | Actual commits | Demo segment |
|---|---|---|---|---|
| TODO | TODO | TODO | TODO | TODO |

Add only actual team members (maximum four). Make real explanatory commits as you
review and change the project. Do not manufacture a historical contribution record.

## Individual Reflection (Each Student, Half a Page)

Write in your own words: what you built; the hardest distributed-systems problem you
solved; the concrete code/test/evidence that convinced you; one rejected alternative;
and what you would change with another week. Discuss AI-assisted code honestly.

## AI-use Declaration Draft

GitHub Copilot assisted with project structure, service implementation, JavaScript UI,
pytest and challenge scripts, report drafting, and execution of local checks. Team
members reviewed and understood the submitted implementation: TODO describe actual
review, corrections and independent verification. Other AI tools: TODO list or state none.

## Nine-Minute Video Outline

1. 0:00-1:00: introduce actual members, application, service ownership and scope.
2. 1:00-3:00: explain component diagram, separate database logins, atomic SQL,
   fingerprinted replay records, and why orchestration was chosen.
3. 3:00-4:15: create a booking with curl; inspect hold, charge, delivery and booking.
4. 4:15-6:00: force fail_notification with a fresh key; inspect transition history,
   REFUNDED charge, RELEASED hold and restored inventory.
5. 6:00-7:00: run `scripts/challenges.py concurrency`; explain why SELECT then UPDATE fails.
6. 7:00-8:00: run `scripts/challenges.py idempotency`; show simultaneous calls,
   changed-payload conflict, replay logs, fingerprint and one payment row.
7. 8:00-9:00: run saga script and pytest; explain recovery limitations and AI use.

Use real terminals, not only slides. Keep every member audible. Record commands,
timestamps and output together. Link the final recording in the report and rebuild PDF.

## Checklist

- [ ] Fresh clone tested by a different member using only README instructions.
- [ ] Faculty can access GitHub and Drive links.
- [ ] Real team details, contribution evidence and individual reflections added.
- [ ] AI declaration reviewed and completed.
- [ ] Current tests and all challenge scripts rerun, evidence inspected.
- [ ] Report links filled, PDF rebuilt and page count verified (maximum 15 excluding appendix).
- [ ] Demo is 8-10 minutes, each member speaks and explains the mechanisms.