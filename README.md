# flow_log_parser
Description
This program parses flow log data and maps each row to a tag based on a lookup table. The flow log entries are in the default format (version 2 only), and the lookup table is provided as a CSV file containing columns: dstport, protocol, and tag.

Key Features:
Default Log Format: The program only supports the default log format (version 2).
Case Insensitivity: The protocol matching is case-insensitive.
Untagged Handling: If a dstport and protocol combination does not exist in the lookup table, the entry is labeled as "Untagged".
Invalid Lines Handling: Lines with fewer than 8 fields are skipped.
Duplicate Entries: Duplicate entries are counted.

Assumptions
Log Format: The program supports only the default flow log format, version 2. Custom log formats or other versions are not supported.
Lookup Table: The lookup table is a CSV file with three columns: dstport, protocol, and tag.
Protocol Mapping: The program uses a predefined mapping of protocol numbers to protocol names (e.g., 6 -> tcp, 17 -> udp). If a protocol number is not found in the mapping, it is labeled as unknown.
Case Insensitivity: Protocol names in the lookup table are matched case-insensitively.
Invalid Lines: Lines in the flow log with fewer than 8 fields are considered invalid and are skipped.
How to Run the Program

Prerequisites:
Python 3.x installed on your system.
Steps:
Clone the repository to your local machine.
Ensure that your flow log data and lookup table are formatted correctly.

Run the program as follows:
python3 flow_log_parser.py flow_logs.txt lookup_table.csv output.txt

Input:
Flow Log File: This file contains the flow log entries to be parsed.
Lookup Table File: This CSV file contains the dstport, protocol, and tag mappings.

Output:
The program will generate an output file that contains:
Tag Counts: The number of occurrences for each tag.
Port/Protocol Combination Counts: The number of occurrences for each dstport/protocol combination.

The program has been tested with the following cases:
Basic Functionality: Parsing and matching entries with correct dstport and protocol.
Case Sensitivity: Ensuring case-insensitive matching for protocol names.
Missing Tags: Handling flow log entries with no matching tags in the lookup table.
Invalid Lines: Skipping lines with fewer than 8 fields.
Duplicate Entries: Counting duplicate entries correctly.
Unusual Protocol Numbers: Handling protocol numbers that are not in the predefined mapping.
Empty Files: Ensuring the program runs without errors when input files are empty.

Edge Cases:
Non-matching Protocol: Protocol numbers that don't exist in the predefined mapping are labeled as unknown.
Invalid dstport: Non-integer values for dstport will result in an error, so the input should be validated to ensure this doesn't happen.
