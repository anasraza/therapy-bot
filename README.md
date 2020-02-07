
# Therapy Bot
This is a NAOqi service for NAO robots. It was developed for, and tested on, NAO robots running NAOqi version 2.1.4.

This purpose of this service is to allow a remote device, such as an iPad, to call custom behaviours (therapy exercises in my case) that are installed on the robot.

---

## Installation
> Note: Currently (2020-02-07), the application package does not auto-run the service after NAO is rebooted. 
> Therefore, the following steps will need to be carried out after every reboot.

1. Download the `.zip` package and unzip the folder
2. Navigate to `therapy-bot/app/` and open the `therapy-bot.pml` file in Choregraphe
3. From the Robot Applications panel in Choregraphe, click the *"Package and install current project to the robot"* icon. (This step assumes you are connected to the robot on the same network)
4. The robot should say *"Ready to connect"* once package is installed and service starts running, if it was not already running. (you can confirm if service is running by `ssh`-ing into robot and running `qicli` and checking if `WrapperService` is listed)

---

## Development
This service was created using the python-service template from [robot-jumpstarter](https://github.com/pepperhacking/robot-jumpstarter).

### Dependencies
- For using `qi`, Python 2.7 **must** be used
  - May even need to use Python 2.7.10 *specifically*
- For developing behaviours, Choregraphe 2.1.4 **must** be used
- For the WebSocket server, Tornado 5.1.1 is used

### Installed Behaviours
The installed behaviours on the robot should be added to `behaviours.json` or `behaviours.txt`. 

The idea was to send the JSON file as a message to the client when it connects, so it can then programmatically send the desired exercise as a request to the server (not yet implemented).

Otherwise, just send the text file to the client developer manually if they want to hard-code the values into their requests (this is the currently implemented approach).

---

## Writing a Client
> Note: This service was originally designed to be connected to by a native iOS application.

This service works by starting a WebSocket server that listens for connections on `ws://<ip>:9999/`. The `ip` is the local address of the robot which is found by pressing the NAO chest button. 

The client device and the robot must be connected to the same network for this to work.

### Messaging Format
A client app that wants to connect to the WebSocket server and send instructions to the robot will need to send a JSON message in the following format:
```
{
"type": "type",
"action": "action",
"description": "description"
}
```

#### Type
The type of instruction the client wants to send to the server. Currently, supported `type` include:

- "command" --- a command for the robot to carry out

> The idea was to allow a client to send two types of instructions: "command", to make the robot do something, or "request", to get some data from the robot. 

#### Action
The action client wants done. Currently, supported `action` include:

- "start" --- starts a behaviour
- "stop" --- stops a behaviour

#### Description
Details of the action the client wants performed. For example, for starting a behaviour, it would be the name of the behaviour as listed in `behaviours.txt`, such as:

- "hip/ely-test"
- "shoulder/shoulder-rotation"

#### Example
For example, to make the robot start a behaviour named "my-behaviour" in a package called "activities", the client app should send the following JSON message:

```
{
"type": "command",
"action": "start",
"description": "activities/my-behaviour"
}
```

---

## Issues

There are a few issues with the current version of this service:

- **Does not load when NAO is rebooted**
  - this means the package will have to be re-uploaded after every reboot to make the WebSocket server run 
  - currently, will have to upload through Choregraphe (`qipkg` gives error)
  - the `robot-jumpstarter` template used is to blame here, since it does not actually work as expected/desired (I really should have tested that before I started this project using the template)
- **Lots of hard-coding, especially the behaviour names being sent by a client**
  - this could possibly be improved by using a combination of `getInstalledBehaviors()` and the `resolveBehaviorName()` methods from `ALBehaviorManager` and by sending the `behaviour.json` file to client on connection
- **Multiple WebSocket clients can connect** 
  - that is the point of WebSockets, but for the purpose of this service it should not be supported
  - therefore, there is currently no multithreading for connections, so best not to open multiple clients
- **Not properly tested**
  - the service has not been properly tested (evident from lack of test files), so could possibly crash unexpectedly (without evidence of it having happened)
 - **Likely many other issues I am unaware of**

 