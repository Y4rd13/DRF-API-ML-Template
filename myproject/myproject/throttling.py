from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle


class CustomThrottle(ScopedRateThrottle):
    def parse_rate(self, rate):
        """
        Given the request rate string, return a two tuple of:
        <allowed number of requests>, <period of time in seconds>

        So we always return a rate for X request per X second.
        Example:
            1, 1

        Args:
            string: rate to be parsed, which we ignore.

        Returns:
            tuple:  <allowed number of requests>, <period of time in seconds>
        """
        return 1, 1