PyBotVac
========
Unofficial pythonic API for Neato BotVac. This API allows you to easily
control and communicate with your Neato BotVac vacuum cleaner. It uses the
official API.


Requirements
------------
In order to use the library you need to register your application with Neato.
Log into `<https://developers.neatorobotics.com/>`_, click *Applications* and
create a new application. If you're making a desktop application, use
``https://localhost:443/`` as the redirect URI. You will also need both the
*Client ID* and *Secret*.


Connect to Beehive
------------------
Beehive is the REST API provided by Neato. It mostly allows account related
queries. It's main purpose is to access the list of robots with their secrets.
OAuth2 is used to authenticate with Beehive.

Here's an example of a simple console application to access the list of robots.

.. code-block:: python

   from pybotvac import Beehive
   from pybotvac._compat import safe_input


   # If you've previously obtained a token you can pass it here as a keyword
   # argument. Then you can skip the fetch_token step
   beehive = Beehive(
       client_id="0000000000000000000000000000000000000000000000000000000000000000",
       client_secret="0000000000000000000000000000000000000000000000000000000000000000",
       redirect_uri="https://localhost:443/",
   )


   # Generate the URL where the user must go to allow API access to the
   # application
   print("Goto the following URL")
   print()
   print("    {}".format(beehive.authorization_url()))
   print()

   # Fetch an OAuth2 token using the redirect URI from the authentication
   # request
   redirect_uri = safe_input("Response URL: ")
   token = beehive.fetch_token(authorization_response=redirect_uri)
   print("Token (save this to avoid re-authentication):")
   print(token)
   print()

   # Get a list of robots (includes serial number and secret for Nucleo)
   print(beehive.get("/users/me/robots").json())


Connect to the robot using Nucleo
---------------------------------
The robot has a persistent connection to Nucleo which is a REST API where one
can send commands directly to the robot using a serial number and secret
obtained using Beehive.

.. code-block:: python

   from pybotvac import Nucleo, RobotRemote


   # Create a default remote we can use to fetch one with more services enabled
   default_remote = RobotRemote()

   # Create a Nucleo query object
   nucleo = Nucleo(
       serial="00000000-000000000000",
       secret="00000000000000000000000000000000",
   )

   # Obtain a list of available services from the current state
   state = nucleo(remote.get_state())

   # Create a new remote based on the available services
   remote = RobotRemote(state["availableServices"])

   # Start cleaning
   nucleo(remote.start_cleaning())
