# DUMMIE Documentation

> All **regular** commands require the prefix **!d**.<br>
**Tree (slash)** commands require no prefix.<br>
`<>` indicates a required parameter for a command.

## <u>Contextual Responses & Tasks</u>

**DUMMIE** may greet any user in a Discord server without being explicitly mentioned (@). If a user says "hi", "hey" or "hello" to **DUMMIE** (e.g. "hey, dummie"), it will respond appropriately.

**DUMMIE** will send a Happy Birthday message to a specified channel for a person or group of people if it is their birthday. In order to do this, a database of birthdays is required; please refer to the [README](/README.md) for more information. It will check for birthdays at an explicitly defined start-of-day time (e.g. UTC (0 by default), EST (UTC-5)). **DUMMIE** will *not* explicitly mention their Discord username, even if they are in the same server as **DUMMIE**. It will also not use their real name, unless this information is specified by the database owner.

## <u>Regular Commands</u>

|  Command	| Description	| Usage
|---------------|--------------------|--------------|
| help	|	DUMMIE (me!) sends this list of commands to you (not a DUMMIE!)	| `help` |
| wowmods	|	Sends a list of some useful World of Warcraft mods to the current channel	| `wowmods` |
| wordcount	|	Scrapes a web page to find the five most frequently used words on it, then sends them to the current channel	| `wc <url>` |

## <u>Tree (Slash) Commands</u>

|  Command	| Description	| Usage
|---------------|--------------------|--------------|
| namesake	|	Prints where DUMMIE's name comes from.	| `namesake` |

