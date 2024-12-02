# AuthenService
Here I decide to create an authen service that registers and logs in users without the use of http and is purely socket connection based. 

The database info on the server-side will insert users in an unordered db and then after create a ordered db by extracting from the first one.

The ultimate purpose of this is to serve as the basis of a Spotify clone 
# NOTE: might move the UI to tauri but hold the same functionality
