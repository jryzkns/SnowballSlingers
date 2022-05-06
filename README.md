# SnowballSlingers!

This is a networked multiplayer game that uses a dedicated server. The goal of the game is to sling snowballs at others and have a great time!

## Up and running

If you want to, you can simply start a server instance and two game clients (two because there's no other way to know that the multiplayer aspect is working) with the following commands:
```
xhost +local:docker # needed for X forwarding... read on to find out more
docker-compose up
```

### game client

First and foremost, the client spawns a graphical PyGame window, this means that X forwarding is required if the project is to be run through docker-compose (This is only tested on a linux host environment that is running X as its display server). Fortunately most of the configuration is handled within `docker-compose.yml`. Prior to starting the client service, docker needs to be added to the list of hosts that the X server accepts:
```
xhost +local:docker
```
Then you can just run the docker command to start this service:
```
docker-compose up client
```
Otherwise, the only requirements to running the client is `pyzmq` and `pygame`, both can be installed through `pip` and you can run `python main.py` in the `client` folder.

We have pre-built executables for both Windows and Linux on [Github Releases](https://github.com/jryzkns/snowballslingers/releases), do bear in mind that they may not be up to date.

### game server

I **STRONGLY** recommend starting up the server service first before attempting to run any clients. It takes longer for the server to launch than the clients, which means that clients will have trouble connecting to the server if the server loads after the client(s). Nothing much to note except starting the server service via `docker-compose up server` sometimes gets stuck at
```
Downloaded from central: https://repo.maven.apache.org/maven2/commons-codec/commons-codec/1.11/commons-codec-1.11.jar
```
If that happens, simply cancel it (press ctrl + C twice) and run it again. Once again, a reminder that a server is running at `18.218.4.58`.

## How to play

This is a section that is relatively volatile. We are planning on adding UI to show how to play once we add in new features. Should there be a descrepancy between the descriptions here or in the game, the game takes precedence.

The rectangular "totem" with a floating triangle above its head is the player that you are currently controlling.

Click any location on the screen with the right mouse button to move to that location (after holding down the mouse button you can move your mouse and your character will follow you as well).

You can throw a snowball at your mouse's cursor location by pressing the space bar (The snowball will only travel as far as where you put your mouse, so if you put your mouse really close to your totem, the snowball will not go far at all).

You can only throw a snowball once every `0.5` seconds. This is reflected by the replenishing gauge on the left side of the player once a snowball has been thrown: a snowball can only be thrown when the gauge is full.

The goal of the game is to dodge snowballs coming from other players in the game and hit other players with your snowballs. Each player has 3 health indicated by the little hearts on the right side of the player totem. Once you run out of health, you will die.

Pro tip: You can deflect an incoming snowball with your own snowball.

Because you will be furiously clicking around on a small screen to move around and sling snowballs, you are bound to accidentally click out of the window and get interrupted. To account for this, you can lock your mouse cursor into the window by pressing the left control key. This is a toggle key so you can press it again to release your mouse cursor.

## Side Notes

There is some information about the architecture in `docs` folder, feel free to read that to get a sense of how the game was pieced together
