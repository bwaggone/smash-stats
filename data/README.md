#Data Formatting:

All Data is output as comma separated value (.csv) files.

##Sets files:

Sets files contain 5 columns total.

| P1  | P2  | Set Winner      | P1Score   | P2Score   |
| ------------- |---------------| --------------- | ----------| ----------|
| P1's tag      | P2's tag      | Who won the set | game count| game count|


   * Notes:
      * Set winner is 0 if player1 won, 1 if player2 won
      * Score has error codes. -1 is a DQ, -2 means no data was reported.
      
##Standings files

Placings are **not in sorted order**. They are relatively straightforward and h ave two columns.

| name  | finalPlacement                |
| ------------ |-------------------------------| 
| Player's tag | Final Placement of tournament | 
