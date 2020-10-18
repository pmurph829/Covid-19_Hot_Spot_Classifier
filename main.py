from parse_utils import parse_county_adj
from county_relations import County, create_county_key

counties = []



counties = parse_county_adj('./data/california_counties.txt') 
#Retrieve other information

sorted_counties = sorted(counties, key=lambda c: c.name)
county_key = create_county_key(counties)
adjlists = {}
#Create adj list
for count in range(len(sorted_counties)):
    print(counties[count].name)
    adjlists[count] = sorted_counties[count].get_neighbors(county_key)
    #print(count, ': ', adjlists[count])

#Create tuple of information
properties = []
for 





