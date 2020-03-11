

class ElapsedTimeParser(object):

    def parse(self, value):
        if value:
            if '_' in value:
                return self._parse_input(value)
            else:
                return self._parse_output(value)
        return None

    def _parse_input(self, value):
        parts = value.split('_')
        if len(parts) != 4:
            return None
        return int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])

    def _parse_output(self, value):
        import re

        regex = re.compile(r'(\d+)d(\d+)h(\d+)m(\d+)s')
        matcher = regex.match(value)
        if matcher:
            return self._get_matched_parts(matcher)
        return None

    def _get_matched_parts(self, regex_match_object):
        parts = regex_match_object.groups()
        if len(parts) != 4:
            return None
        return int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])
