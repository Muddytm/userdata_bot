# userdata_bot
Your friendly neighborhood automated Skytap userdata maintenance service.

How to use:
(Note: I'll make this section prettier later)

1. Make sure Skytap is installed ("pip install skytap"). Configure it to work with your credentials.
2. Clone this repo to wherever you want.
3. Initialize variables in all environment userdata by running "python update.py reset".
4. Every hour, run "python update.py check".

Note: "reset" will delete all existing userdata and replace it with a new
format. Variables by the name of "shutdown_time", "shutdown_delay", and
"delete_environment" will be preserved, however. (This value format looks like
"shutdown_time: 4" in the userdata form)

That's it!

More relevant information:

- This version of userdata_bot does not account for additional variables other than the 3 mentioned. This will be addressed soon.
- shutdown_delay and delete_environment will decrement when shutdown_time is equal to the time in UTC.
- delete_environment is not necessary to have in userdata and will not appear by default.
- Upon reaching 0, shutdown_delay will force an environment suspension every time shutdown_time is equal to the time in UTC.
- Similarly, delete_environment will delete the environment if the value is at 0 at this time.
