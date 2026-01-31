# Telegram Productivity Bot System

3-bot system for task logging, habit tracking, and conversational productivity insights. Built with PostgreSQL + RAG for temporal querying of activity patterns.

## What This Does

- **Task Logger**: Store tasks, notes, and entries in PostgreSQL with timestamps
- **Habit Checker**: Scheduled morning reminders with habit completion tracking
- **Conversational Agent**: RAG-powered bot that queries your historical tasks and habits for productivity insights

## Architecture
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Task Logger │────▶│  PostgreSQL │◀────│Habit Checker│
└─────────────┘     └─────────────┘     └─────────────┘
                           ▲
                           │
                    ┌──────┴──────┐
                    │Conversational│
                    │    Agent     │
                    │    (RAG)     │
                    └──────────────┘
```

All bots share the same PostgreSQL database, enabling cross-bot data access and temporal analysis of user behavior.

## Features

### Task Logger
- Log tasks, notes, ideas via natural language
- Automatic timestamping and categorization
- PostgreSQL storage for efficient querying

### Habit Checker
- Scheduled morning check-ins via Telegram
- Track habit completion over time
- Streak tracking and historical analysis

### Conversational Agent
- Ask questions about your productivity patterns
- RAG-powered insights from historical data
- Examples: "What did I work on last Tuesday?", "How consistent are my morning habits?"

---

**Status**: Ongoing project
