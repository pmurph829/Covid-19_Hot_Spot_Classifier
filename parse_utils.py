from county_relations import County
import re
import pandas
import csv
import numpy as np

rx_dict =  {
    'main_county': re.compile(r'"(?P<name>([a-z]|[A-Z]| )+) County, (?P<state>[A-Z]+)"\t+(?P<id>[0-9]+)\t+"(?P<adj_name>([a-z]|[A-Z]| )+) County, (?P<adj_state>[A-Z]+)"\t+(?P<adj_id>[0-9]+)$'),
    'adjacent_county': re.compile(r'\t+"(?P<adj_name>([a-z]|[A-Z]| )+) County, (?P<adj_state>[A-Z]+)"\t+(?P<adj_id>[0-9]+)$')
}


def parse_line(line):
    '''
    Do A Regex search against all defined patterns and return the key and match the works
    '''
    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    
    #if there are no matches
    return None, None


def parse_county_adj(filepath):
    counties = []

    with open(filepath, 'r') as adjfile:
        line = adjfile.readline()
        county = None
        while line:
            key, match = parse_line(line)
            #print(line)
            if key == 'main_county':
                name = match.group('name')
                id = match.group('id')
                state = match.group('state')

                county = County(name, id, state)
                #print("Created County: ", county.name)

                adj_name = match.group('adj_name')
                adj_id = match.group('adj_id')
                adj_state = match.group('adj_state')

                adj_county = County(adj_name, adj_id, adj_state)
                
                if adj_county.state == 'CA':
                    county.add_neighbor(adj_county)
                #print("Added Ajacent County: ", adj_county.name)

                counties.append(county)
            
            if key == 'adjacent_county':
                adj_name = match.group('adj_name')
                adj_id = match.group('adj_id')
                adj_state = match.group('adj_state')

                
                adj_county = County(adj_name, adj_id, adj_state)
                #print("Added Ajacent County: ", adj_county.name)
                if adj_county.state == 'CA':
                    county.add_neighbor(adj_county)

            line = adjfile.readline()
    return counties

def parse_labels(filename, counties):
    with open(filename, newline='') as labelfile:
        labelreader = csv.reader(labelfile)
        for row in labelreader:
            for c in counties:
                if c.name == row[0]:
                    c.label = row[1]
    return counties

def create_labels_matrix(counties):
    A = np.zeros((len(counties), 2))
    for index in range(len(counties)):
        if counties[index].label == '1':
            A[index] = [0, 1]
        else:
            A[index] = [1, 0]
    return A


