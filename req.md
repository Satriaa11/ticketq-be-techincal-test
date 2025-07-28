Use NestJS (preferred) or Flask if you’re allergic to TypeScript.
Implement the following endpoints:
GET /tickets — List all tickets
GET /tickets/:id — View a specific ticket
POST /tickets — Create a new ticket
PATCH /tickets/:id — Mark a ticket as used
DELETE /tickets/:id — Remove a ticket

Ticket model should include:
id, eventName, location, time, isUsed
Use ORM with SQLite/PostgreSQL/MongoDB (bonus if you dockerise it)
Add input validation (e.g., eventName required, time must be valid ISO)
Include error handling (404, 400, 500)
