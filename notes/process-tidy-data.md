# Tidy data

## The problem it solves
Messy data slows analysis down because the tools expect a certain shape. GROUP BY, filters, and charts all assume each variable is its own column. When a variable is hidden somewhere else, like the platform buried in column names such as purchases_ios and purchases_android, you have to reshape the data or write a separate query for each column before you can analyze anything. 

## The rules
When looking at this from a game telemetry perspective:
Each variable is a column - Varibles like time played, money spent, install date etc
Each obserevation is a row - Each player would have their own row
Each type of observational unit - each table in the database would be a unit ex. there would be a table for events, one for purchases etc


## Where I used it
In Lesson 1, whether a number was a current level or a target was stuck in the column headers (level, target), like a platform hidden in purchases_ios / purchases_android. melt moved it into its own column, series, so the radar chart could group by series and draw one shape for each. In Lesson 2, I kept track as a column instead of splitting the data into two files, so I could filter to one track and group by track, the same as WHERE and GROUP BY in SQL.

## What I'm still unsure about
How does tidy data relate to missing values? Are they the same kind of messy?