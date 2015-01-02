import os
import re
from datetime import datetime

class Transfer(object):
    def __init__(self):
        self.article_dir = "/Users/bcordonnier/repos/soycorn/soycorn/public/articles"
        self.regex = re.compile("(\D+)(\d+)_(\d+)")
        self.month_map = {
            "Jan": 1,
            "Feb": 2,
            "Mar": 3,
            "Apr": 4,
            "May": 5,
            "Jun": 6,
            "Jul": 7,
            "Aug": 8,
            "Sep": 9,
            "Oct": 10,
            "Nov": 11,
            "Dec": 12
        }

    def run(self):
        self.parse_links()

    def parse_date(self, date_str):
        split = self.regex.findall(date_str)
        if len(split) == 0 or len(split[0]) != 3:
            print "BOOM"
            return
        split = split[0]
        day = int(split[1])
        year = 2000 + int(split[2])
        if split[0] in self.month_map:
            month = self.month_map[split[0]]
        else:
            print "BOOM"
            return
        d = datetime(year, month, day)
        print("str:{0} obj:{1}".format(date_str, d))

    def parse_links(self):
        with open(os.path.join(self.article_dir, "links")) as f:
            links = f.readlines()
        print("num:{0}".format(len(links)))
        for l in links:
            l = l.strip()
            if ";" in l:
                split = l.split(";")
                file_name = split[0]
                print file_name
                title = split[1].strip()
                date_str = file_name.split("-")[0]
                self.parse_date(date_str)

if __name__ == "__main__":
    t = Transfer()
    t.run()