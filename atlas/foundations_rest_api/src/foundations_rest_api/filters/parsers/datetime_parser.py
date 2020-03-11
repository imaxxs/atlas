from datetime import datetime


class DateTimeParser(object):

    def parse(self, value):
        if value:
            if isinstance(value, datetime):
                return value

            value = str(value)  # Avoid Python 2 unicode issues
            if '_' in value:
                return self._parse_input(value)
            else:
                return self._parse_output(value)
        return None
        
    def _parse_input(self, value):
        return datetime.strptime(value, '%m_%d_%Y_%H_%M')

    def _parse_output(self, value):
        return self._fromisoformat(value)

    def _fromisoformat(self, value):
        try:
            return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
