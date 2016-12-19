#Data Formatting:

All Data is output as comma separated value (.csv) files.

The data is broken up by game, by type. If a tournament has Doubles, Singles or Crews, it will be recorded.

   * Notes:
      * Crews shows the **name of the crew only**, not the members of the crew

##Sets files:

Sets files contain 5 columns total.

| P1  | P2  | Set Winner      | P1Score   | P2Score   |
| ------------- |---------------| --------------- | ----------| ----------|
| P1's tag      | P2's tag      | Who won the set | game count| game count|


   * Notes:
      * Set winner is 0 if player1 won, 1 if player2 won
      * Score has error codes. -1 is a DQ, -2 means no data was reported.
      
      
| T1P1  | T1P2  | T2P1  | T2P2  | Set Winner      | T1Score   | T2Score   |
| ------|------ |-------|-------| --------------- | ----------| ----------|
| Team 1 Player 1's Tag | Team 1 Player 2's Tag  | Team 2 Player 1's Tag | Team 2 Player 2's Tag | Who won the set | game count| game count|
      
   * Notes:
      * Set winner is 0 if Team 1 won, 1 if Team 2 won
      * Score has error codes. -1 is a DQ, -2 means no data was reported.
      * **There is an issue with players who have a '|' in their tag currently.**
      
##Standings files

Placings are **not in sorted order**. They are relatively straightforward and have two columns.

| name  | finalPlacement                |
| ------------ |-------------------------------| 
| Player's tag | Final Placement of tournament | 

##Master Tournament File

This file has a list of tournament slugs and dates. There is one per folder, and three total columns.

| Tournament | startAt | endAt | Entrants* |
| ------------ | --------------| -----| ------|
| Tournament Slug | Starting date (YYYY-MM-DD) | Ending date (YYYY-MM-DD) | Number of entrants |

   * Notes:
      * The tournaments file is created/appended automatically when running get_data.py
      * It can be configured to convert from date to epoch time, if that floats your boat.
      * \*This does *not* currently get the number of entrants.
