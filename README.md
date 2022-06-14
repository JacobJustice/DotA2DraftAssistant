# DotA2DraftAssistant

Uses match history and global winrate data from the OpenDota API to generate a model that predicts your winrate on any hero, given a current draft.

The model takes into account: 
 + The average winrate for the hero on the most recent version of the game. This value can be weighted by λ. If you have a lot of matches, the model performs better with lower λ values.
 + The heroes on your team
 + How you perform as any given hero WITH the heroes on YOUR team
 + The heroes on the enemy team
 + How you perform as any given hero AGAINST the heroes on the ENEMY team

This is intended to be used during captains mode, and an assisting program (`poll_screen.py`) is available that runs the model while reading the heroes from the game using Computer Vision.
