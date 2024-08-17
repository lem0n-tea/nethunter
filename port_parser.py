# port_parser.py
def port_parse(listed_ports):
    result = []
    port_ranges = listed_ports.split(',')
    for port_range in port_ranges:
        # Exclude any spacing from the content
        port_range = port_range.strip()
        try:
            # Determine whether port_range contains range or a single number
            if '-' in port_range:
                # Include all ports from range
                start, end = map(int, port_range.split('-'))
                if out_of_bounds(start) or out_of_bounds(end):
                    return "Port is out of bounds"
                result.extend(range(start, end + 1))
            else:
                # Include single port
                if out_of_bounds(int(port_range)):
                    return "Port is out of bounds"
                result.append(int(port_range))
        except ValueError:
            return "Invalid port input"

    return result


# Check if a port is outside the allowed range
def out_of_bounds(port):
    return port < 1 or port > 65535
