from errbot import BotPlugin, botcmd
from json import dumps, loads
import os


class ServicePortNumber(BotPlugin):
    """Service Port Number Responder Bot"""

    def __init__(self, bot):
        super().__init__(bot)
        file_dir = os.path.dirname(__file__)
        self.services_file = os.path.join(file_dir, "services")
        self.services = self._load_services()

    def _load_services(self):
        """Load services and their port numbers from disk."""
        if not os.path.isfile(self.services_file):
            raise Exception("Services file does not exist!")
        with open(self.services_file, "r") as f:
            services = loads(f.read())
        return services

    def _save_services(self):
        """Save services and their port numbers to disk."""
        with open(self.services_file, "w") as f:
            f.write(dumps(self.services))

    @botcmd
    def port(self, msg, args):
        """Return the port number of the provided service."""
        if not args:
            return ("Need to pass a service to query. "
                    "Example: !port API")
        elif not self.services:
            return "There are no services registered."
        elif args not in self.services:
            return "There is no such service as {} registered.".format(args)
        else:
            return self.services[args]

    @botcmd
    def port_add(self, msg, args):
        """Add a service and port number to the list."""
        if not args:
            return ("Need to pass a service and port to add. "
                    "Example: !port add API 80")

        args = args.split(" ")
        if len(args) != 2:
            return ("Need to pass only 2 arguments. "
                    "Example: !port add API 80")
        elif args[0].lower() in [k.lower() for k, v in self.services]:
            return "{} is already a  service".format(args)
        else:
            try:
                self.services[args[0]] = int(args[1])
                self._save_services()
                return "{} has been added as a service".format(args)
            except:
                return "{} is not a valid port number.".format(args[1])

    @botcmd
    def port_remove(self, msg, args):
        """Remove a service from the list."""
        if not args:
            return ("Need to pass a service to remove. "
                    "Example: !port remove API")
        elif args.lower() not in [k.lower() for k, v in self.services]:
            return "{} is not registered as a service".format(args)
        else:
            self.services = [
                k for k in self.services if k.lower() != args.lower()]
            self._save_services()
            return "{} has been removed as a service".format(args)

    @botcmd
    def port_list(self, msg, args):
        """List all services."""
        return "Services:\n{}".format(
            "\n".join(["{}:{}".format(k,v) for k,v in self.services]))

    @botcmd
    def port_empty(self, msg, args):
        """Empty the services."""
        self.services = []
        self._save_services()
        return "All services have been deleted."
