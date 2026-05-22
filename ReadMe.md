This project is made as a teaching python program. It works against the Artifacts MMO api.

The Game Master is the "brain" that will assign Quests objects to Heroes. 
Quests objects are a succession of Routines : Go_dosomething, which in turn call Actions (which are the actual HTTP calls on the Artifact API); or check a few values in DB.

The Helpers are utility functions, and might have to be stored elsewhere to have an easier access to global data.