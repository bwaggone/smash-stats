#Data Formatting:

All Data is output as comma separated value (.csv) files.

The data is broken up by game, by type. If a tournament has Doubles, Singles or Crews, it will be recorded.

   * Notes:
      * Crews shows the **name of the crew only**, not the members of the crew

##Sets files:

Sets files in the Singles folder contain 5 columns total.

| P1  | P2  | Set Winner      | P1Score   | P2Score   |
| ------------- |---------------| --------------- | ----------| ----------|
| P1's tag      | P2's tag      | Who won the set | game count| game count|


   * Notes:
      * Set winner is 0 if player1 won, 1 if player2 won
      * Score has error codes. -1 is a DQ, -2 means no data was reported.
      * **There is an issue with players who have a '|' in their tag currently.**

      

Set files in the Doubles folder contain 7 columns total.
      
| T1P1  | T1P2  | T2P1  | T2P2  | Set Winner      | T1Score   | T2Score   |
| ------|------ |-------|-------| --------------- | ----------| ----------|
| Team 1 Player 1's Tag | Team 1 Player 2's Tag  | Team 2 Player 1's Tag | Team 2 Player 2's Tag | Who won the set | game count| game count|
      
   * Notes:
      * Set winner is 0 if Team 1 won, 1 if Team 2 won
      * Score has error codes. -1 is a DQ, -2 means no data was reported.
      
##Standings files

Placings are **not in sorted order**. They are relatively straightforward and have two columns.

| name  | finalPlacement                |
| ------------ |-------------------------------| 
| Player's tag | Final Placement of tournament | 

##Master Tournament File

This file has a list of tournament slugs and dates. There is one per folder, and three total columns.

| Tournament | slug | startAt | endAt | Entrants |
| ------------ | ---- |--------------| -----| ------|
| Tournament Name | Tournament Slug (smash.gg url) | Starting date (YYYY-MM-DD) | Ending date (YYYY-MM-DD) | Number of entrants |

   * Notes:
      * The tournaments file is created/appended automatically when running get_data.py
      * It can be configured to convert from date to epoch time, if that floats your boat.
      * **It is not in any sorted or chronological order.**

# Name Fixes

There is now a file to fix all incorrectly scrapped names. To use, all you need to do is a add a line to the name_fixes.csv file. It follows this format:

| name | game | to |
| ------------ | -----| ------|
| the wrong name to be changed | the game of the player | the name to change it to |

So for example, a fix involving mang0 would look like,

| name | game | to |
| ------------ | -----| ------|
| mango | Melee | mang0 |

  * Notes
    * Game is **case sensitive**. It must follow the exact name of the game's folder.
    * I currently only wrote this to work for singles, doubles support coming soon (tm).
    * If you mess up, just write a new line to fix your mistake.
    * I have it replace the trailing comma, to prevent partial ending string matches (superboom->superboomfan turns superboomfan->superboomfanfan). Technically this can still be a problem for a player like, player1->player2, could cause someone ith the name theplayer1->theplayer2. Assuming player1 and theplayer1 are two separate players, this can be a problem. I'll replace this with regex eventually.
