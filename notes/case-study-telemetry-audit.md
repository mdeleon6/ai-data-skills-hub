# Case Study: Telemetry Audit, Assassin's Creed Rebellion
*Data Analyst, Live Ops · Ubisoft Halifax · 2025 · Factors: Prepare, Process*

## Situation
Assassin's Creed Rebellion's telemetry fed the live-ops team's analysis:
how much players spent on in-app purchases, how long they spent on
missions, and which items and characters they bought. I started seeing
data missing from our tables.

## Task
I raised it with my manager, the product manager, who asked me to find
the cause and either fix it or escalate it. While I was investigating,
the producer asked me to run a full audit of the game's telemetry to make
sure every event was up to date and working. At the same time, new
features were launching that needed new events designed and tested.

## Action
- I checked each event against the telemetry documentation (our tracking
  plan), one event at a time, doubling back when something didn't add up.
- I found events that had been changed without the documentation being
  updated, and variables that had been deprecated.
- Where a variable was marked deprecated, I removed it. Where an event
  was missing variables it needed, I added them, correcting multiple
  tables in the process.
- For the new features, I designed new events with the properties the
  analysis would need: player ID, date, details of the action, and the
  player's level.
- QA tested every event. Once they confirmed it was collecting the right
  data, I marked it completed and tested.

## Result
Data started arriving clean at the source. Before the audit I was cleaning
data daily; afterwards it rarely needed cleaning.

## What I learned
Make sure I fully understand the task before starting. In the same role
again, I'd cross-check the data tables against the event definitions early,
and run a quiet audit of my own before problems show up in the data,
not after.