Warning: Might cause seizures

# Requirements
Python (Tested on 3.13.7)

# Usage
1. Run Da-Funny.bat or randomizer.py.
2. Select decode.
3. Enter the file name, Must also include the `.btnks` extention.
5. Then choose if you want to pretty-print.
6. After all of that select randomize.
7. select any option. (Currently data is the only option)
8. Choose a user's id or username.
9. Choose a tank data coloumn to randomize (Info will be in the `Info for data option.txt` file)
10. Enter your maximum and minimal values.
11. After it finishes changing the values, Select encode.
12. Choose your file name.

And it's done, now you can import your randomized replay to Blocktanks.net, Make sure you have `Record Match Replays` enabled to import replays.

### Known Issues
1. Same user ID's

    When there is same Id's for two players (When a bot replaces a user, user replaces a bot, user2 replaces user1),
    the column you input will be used on the new user and not the old user.

    For example (on ffa):
    ```json
    "idPool": {
        "unknownuser": 0,
        "[bot] kevin": 1,
        "[bot] vladmir": 2,
        "[bot] ryan": 3,
        "guest-13653": 3
    }
    ```
    `[BOT] Ryan` gets replaced by `guest-13653` which the values you inputted will be applied to the new user.

    These duplicate ID's do not show in the userlist.
