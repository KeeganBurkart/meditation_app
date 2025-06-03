# Configurable Notifications

Mindful Connect allows users to tailor reminder notifications to their schedule. Users can enable daily or weekly reminders and choose the delivery time for each notification.

The backend stores the preferred times in a user settings table. Mobile and web clients read these preferences and schedule local notifications accordingly.

Example settings structure:

```json
{
  "reminders": [
    {"time": "07:00", "message": "Start your morning with a calm mind"},
    {"time": "21:00", "message": "Take a moment to wind down"}
  ]
}
```

Notifications can be turned on or off per reminder, giving members full control over how often they're nudged to meditate.
