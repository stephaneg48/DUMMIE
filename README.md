> # DUMMIE - A Discord Bot

---

<img src="icon.png" width="200" height="200">

**DUMMIE** is an open-source, personal bot for [Discord](https://discord.com/) that has various features. It is still a work-in-progress, so new features are occasionally added.

> # Features

**DUMMIE** currently has capabilities such as:

- responding to basic greetings
- fetching birthdays from a database to say Happy Birthday to one person or multiple people
- web scraping a web page (where allowed) to find the 5 most frequently used words on it 
- listing a collection of useful video game mods 

For more detailed documentation on what **DUMMIE** can do, please refer to [this file](/INFO.md).
## <u>Example of web scraping feature</u>

![](/img/web-scrape.png)

> # Dependencies

**DUMMIE** requires a few external resources in order to be fully functional:

- Several Python libraries (Beautiful Soup, discord.py, MySQL Connector/Python) [(requirements.txt)](/requirements.txt)
- An SQL database (MySQL preferrable)
    - for saying Happy Birthday, a table `birthdays` is assumed to exist in the database with the following structure:
        - `id` (INT)
        - `name` (VARCHAR)
        - `month` (INT)
        - `day` (INT)
- Device / service to host the Python executable
    - If this cannot be acquired, the executable for **DUMMIE** can simply run on your machine
- Appropriate API tokens from Discord
    - Unsure about this? Refer to [this page](https://discord.com/developers/docs/getting-started).
> # Disclaimer

**DUMMIE** is meant for recreational purposes. Anyone may use it by simply cloning/forking this repository and acquiring the pre-requisite tools. You do not need to request a server authorization link for the bot - it is free to host personally, and this software will always be available for free. However, it cannot be used for the following (**not an exhaustive or fully explicit list**):

- *any* kind of monetary gain
- streaming music/soundbites from YouTube (this is *not* a planned feature)

The Pathfinder icon [`(icon.png)`](icon.png) comes from [Apex Legends](https://www.ea.com/games/apex-legends) or from websites created and owned by **Electronic Arts Inc.** or **Respawn Entertainment**, who hold the copyright of Apex Legends. All trademarks and registered trademarks present in the icon are proprietary to Electronic Arts Inc.

# Have a suggestion for this project? [Feel free to submit a new issue](https://github.com/stephaneg48/DUMMIE/issues).