import datetime
import skytap
import sys


def rewrite(e, def_time, def_delay, def_delete):
    """Rewrite an environment's userdata with new values."""
    # Wiping data; 10 is an arbitrary amount that should work for our purposes
    for x in range(10):
        e.user_data.delete_line(e.user_data.get_line(0))
        e.refresh()

    try:
        if int(def_delete) >= 0:
            e.user_data.add("delete_environment", str(def_delete))
            e.refresh()
    except ValueError:
        pass

    e.user_data.add("shutdown_delay", str(def_delay))
    e.refresh()
    e.user_data.add("shutdown_time", str(def_time))
    e.refresh()

    e.user_data.add_line("// For more information, see the related Skytap "
                         "userdata Confluence page.", 0)
    e.refresh()
    e.user_data.add_line("// shutdown_delay = amount of days left before "
                         "automated suspension resumes.", 0)
    e.refresh()
    e.user_data.add_line("// shutdown_time = the time (in UTC) when the "
                         "environment will be suspended.", 0)
    e.refresh()


def check(envs):
    """Check all environments' userdata and act based on it."""
    time = datetime.datetime.utcnow()

    for e in envs:
        print ("Checking environment. ID: " + str(e.id) + ". Name: " + e.name)
        # Default values
        def_time = 3
        def_delay = 0
        def_delete = -1

        if "shutdown_time" in e.user_data:
            # Check if data is valid
            if e.user_data.shutdown_time == "-":
                # Permanent exclusion!
                continue

            try:
                if (int(e.user_data.shutdown_time) >= 0 and
                        int(e.user_data.shutdown_time) <= 23):
                    def_time = int(e.user_data.shutdown_time)
            except ValueError:
                # Value is invalid (not - or a number), use def_time
                pass

        if "shutdown_delay" in e.user_data:
            if e.user_data.shutdown_delay == "-":
                continue

            try:
                if (int(e.user_data.shutdown_delay) >= 0 and
                        int(e.user_data.shutdown_delay) <= 31):
                    def_delay = int(e.user_data.shutdown_delay)
            except ValueError:
                pass

        if "delete_environment" in e.user_data:
            try:
                if int(e.user_data.delete_environment) >= 0:
                    def_delete = int(e.user_data.delete_environment)
            except ValueError:
                pass

        if def_time == int(time.hour):
            if def_delete == 0:
                e.delete()
            elif def_delete > 0:
                def_delete -= 1

            if def_delay == 0:
                e.suspend()
            else:
                def_delay -= 1

        rewrite(e, def_time, def_delay, def_delete)


def reset(envs):
    """Reset all environments to default layout.

    Attempt to obtain values if they exist, and keep them."""
    for e in envs:
        print ("Resetting environment. ID: " + str(e.id) + ". Name: " + e.name)
        # Default values
        def_time = 3
        def_delay = 0
        def_delete = -1

        if "shutdown_time" in e.user_data:
            def_time = e.user_data.shutdown_time

        if "shutdown_delay" in e.user_data:
            def_delay = e.user_data.shutdown_delay

        if "delete_environment" in e.user_data:
            def_delete = e.user_data.shutdown_delay

        rewrite(e, def_time, def_delay, def_delete)


def start(args):
    """Begin update process."""
    if len(args) == 1:
        return

    envs = skytap.Environments()

    if args[1] == "check":
        check(envs)
    elif args[1] == "reset":
        reset(envs)
    else:
        print ("Invalid argument.")


if __name__ == "__main__":
    start(sys.argv)
