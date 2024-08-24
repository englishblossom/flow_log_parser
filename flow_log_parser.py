
import csv
from collections import defaultdict

PROTOCOL_MAP = {
    '0': 'hopopt',
    '1': 'icmp',
    '2': 'igmp',
    '3': 'ggp',
    '4': 'ipv4',
    '5': 'st',
    '6': 'tcp',
    '7': 'cbt',
    '8': 'egp',
    '9': 'igp',
    '10': 'bbn-rcc-mon',
    '11': 'nvp-ii',
    '12': 'pup',
    '13': 'argus',
    '14': 'emcon',
    '15': 'xnet',
    '16': 'chaos',
    '17': 'udp',
    '18': 'mux',
    '19': 'dcn-meas',
    '20': 'hmp',
    '21': 'prm',
    '22': 'xns-idp',
    '23': 'trunk-1',
    '24': 'trunk-2',
    '25': 'leaf-1',
    '26': 'leaf-2',
    '27': 'rdp',
    '28': 'irtp',
    '29': 'iso-tp4',
    '30': 'netblt',
    '31': 'mfe-nsp',
    '32': 'merit-inp',
    '33': 'dccp',
    '34': '3pc',
    '35': 'idpr',
    '36': 'xtp',
    '37': 'ddp',
    '38': 'idpr-cmtp',
    '39': 'tp++',
    '40': 'il',
    '41': 'ipv6',
    '42': 'sdrp',
    '43': 'ipv6-route',
    '44': 'ipv6-frag',
    '45': 'idrp',
    '46': 'rsvp',
    '47': 'gre',
    '48': 'dsr',
    '49': 'bna',
    '50': 'esp',
    '51': 'ah',
    '52': 'i-nlsp',
    '53': 'swipe',
    '54': 'narp',
    '55': 'min-ipv4',
    '56': 'tlsp',
    '57': 'skip',
    '58': 'ipv6-icmp',
    '59': 'ipv6-nonxt',
    '60': 'ipv6-opts',
    '61': 'host-internal',
    '62': 'cftp',
    '63': 'local-network',
    '64': 'sat-expak',
    '65': 'kryptolan',
    '66': 'rvd',
    '67': 'ippc',
    '68': 'distributed-file-system',
    '69': 'sat-mon',
    '70': 'visa',
    '71': 'ipcv',
    '72': 'cpnx',
    '73': 'cphb',
    '74': 'wsn',
    '75': 'pvp',
    '76': 'br-sat-mon',
    '77': 'sun-nd',
    '78': 'wb-mon',
    '79': 'wb-expak',
    '80': 'iso-ip',
    '81': 'vmtp',
    '82': 'secure-vmtp',
    '83': 'vines',
    '84': 'iptm',
    '85': 'nsfnet-igp',
    '86': 'dgp',
    '87': 'tcf',
    '88': 'eigrp',
    '89': 'ospfigp',
    '90': 'sprite-rpc',
    '91': 'larp',
    '92': 'mtp',
    '93': 'ax.25',
    '94': 'ipip',
    '95': 'micp',
    '96': 'scc-sp',
    '97': 'etherip',
    '98': 'encap',
    '99': 'private-encryption',
    '100': 'gmtp',
    '101': 'ifmp',
    '102': 'pnni',
    '103': 'pim',
    '104': 'aris',
    '105': 'scps',
    '106': 'qnx',
    '107': 'a/n',
    '108': 'ipcomp',
    '109': 'snp',
    '110': 'compaq-peer',
    '111': 'ipx-in-ip',
    '112': 'vrrp',
    '113': 'pgm',
    '114': '0-hop-protocol',
    '115': 'l2tp',
    '116': 'ddx',
    '117': 'iatp',
    '118': 'stp',
    '119': 'srp',
    '120': 'uti',
    '121': 'smp',
    '122': 'sm',
    '123': 'ptp',
    '124': 'isis-over-ipv4',
    '125': 'fire',
    '126': 'crtp',
    '127': 'crudp',
    '128': 'sscpmce',
    '129': 'iplt',
    '130': 'sps',
    '131': 'pipe',
    '132': 'sctp',
    '133': 'fc',
    '134': 'rsvp-e2e-ignore',
    '135': 'mobility-header',
    '136': 'udplite',
    '137': 'mpls-in-ip',
    '138': 'manet',
    '139': 'hip',
    '140': 'shim6',
    '141': 'wesp',
    '142': 'rohc',
    '143': 'ethernet',
    '144': 'aggfrag',
    '145': 'nsh',
    '253': 'experimentation-1',
    '254': 'experimentation-2',
    '255': 'reserved',
}

def parse_lookup_table(file_path):
    lookup_table = {}
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            port = int(row['dstport'])
            protocol = row['protocol'].lower()
            tag = row['tag']
            lookup_table[(port, protocol)] = tag
    return lookup_table

def process_flow_logs(flow_log_file, lookup_table):
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)

    with open(flow_log_file, 'r') as file:
        for line in file:
            fields = line.strip().split()
            if len(fields) < 8:
                continue
            dst_port = int(fields[6])
            protocol_num = fields[7]
            protocol = PROTOCOL_MAP.get(protocol_num, 'unknown').lower()
            tag = lookup_table.get((dst_port, protocol), 'Untagged')
            tag_counts[tag] += 1
            port_protocol_counts[(dst_port, protocol)] += 1

    return tag_counts, port_protocol_counts

def write_output(tag_counts, port_protocol_counts, output_file):
    with open(output_file, 'w') as file:
        file.write("Tag Counts:\n")
        file.write("Tag,Count\n")
        for tag, count in tag_counts.items():
            file.write(f"{tag},{count}\n")

        file.write("\nPort/Protocol Combination Counts:\n")
        file.write("Port,Protocol,Count\n")
        for (port, protocol), count in port_protocol_counts.items():
            file.write(f"{port},{protocol},{count}\n")

def main(flow_log_file, lookup_table_file, output_file):
    lookup_table = parse_lookup_table(lookup_table_file)
    tag_counts, port_protocol_counts = process_flow_logs(flow_log_file, lookup_table)
    write_output(tag_counts, port_protocol_counts, output_file)

if __name__ == "__main__":
    main("flow_logs.txt", "lookup_table.csv", "output.txt")
