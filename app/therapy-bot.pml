<?xml version="1.0" encoding="UTF-8" ?>
<Package name="therapy-bot" format_version="4">
    <Manifest src="manifest.xml" />
    <BehaviorDescriptions />
    <Dialogs />
    <Resources>
        <File name="icon" src="icon.png" />
        <File name="wrapperservice" src="scripts/wrapperservice.py" />
        <File name="__init__" src="scripts/stk/__init__.py" />
        <File name="__init__" src="scripts/stk/__init__.pyc" />
        <File name="events" src="scripts/stk/events.py" />
        <File name="events" src="scripts/stk/events.pyc" />
        <File name="logging" src="scripts/stk/logging.py" />
        <File name="logging" src="scripts/stk/logging.pyc" />
        <File name="runner" src="scripts/stk/runner.py" />
        <File name="runner" src="scripts/stk/runner.pyc" />
        <File name="services" src="scripts/stk/services.py" />
        <File name="services" src="scripts/stk/services.pyc" />
        <File name="__init__" src="scripts/communication/__init__.py" />
        <File name="behaviours" src="scripts/communication/behaviours.json" />
        <File name="behaviours" src="scripts/communication/behaviours.txt" />
        <File name="wrapper" src="scripts/communication/NaoQiWrapper.py" />
        <File name="request_handler" src="scripts/communication/RequestHandler.py" />
        <File name="server" src="scripts/communication/Server.py" />
        <File name="signal_handler" src="scripts/communication/SignalHandler.py" />
        <File name="socket" src="scripts/communication/WebSocketHandler.py" />
    </Resources>
    <qipython name="wrapperservice" />
    <Topics />
    <IgnoredPaths>
        <Path src=".metadata" />
    </IgnoredPaths>
</Package>
