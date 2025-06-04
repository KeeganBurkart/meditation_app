# Premium Tiers

Mindful Connect offers an optional **Premium** subscription. Premium unlocks
advanced statistics, unlimited friend connections, and the ability to create
private challenges. Users without an active subscription remain on the **Free**
tier.

The backend stores subscription information in a `subscriptions` table keyed by
`user_id`. Helper functions in `subscriptions.py` allow the app to determine a
user's tier and whether a feature requires premium access.


