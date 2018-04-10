def read_stops_write_links(input_file):
    stopslist = []
    with open(input_file, mode="r") as stops:
        for line in stops:
            splitted  = line.split(";")
            stop = splitted[0]
            lat = splitted[1]
            lon = splitted[2]
            link = "https://www.google.com/maps/place/%s,%s" % (lat,lon)
            stopslist.append((stop, link))

    return stopslist

def write_stops(stopslist, output):
    with open(output, mode="w") as stops:
        for stop,link in stopslist:
            stops.write("%s\t%s" % (stop, link))

if __name__ == "__main__":
    st = read_stops_write_links("stops.csv")
    write_stops(st, "newstops.csv")
