from django.core.management.base import BaseCommand
import os
import re
from datetime import datetime
from logger import SoycornLogger
from new_soycorn.models import Article


class Command(BaseCommand):
    help = 'Does some magical work'

    def handle(self, *args, **options):
        """ Do your work here """
        t = Transfer()
        t.run()

class ArticleData(object):
    def __init__(self):
        self.name = ""
        self.pub_date = None
        self.file_name = ""

    def __str__(self):
        return "{0} - {1} - {2}".format(self.pub_date, self.name, self.file_name)


class Transfer(object):
    def __init__(self):
        self.old_article_dir = "/Users/bcordonnier/repos/soycorn/soycorn/public/articles"
        self.new_article_dir = "/Users/bcordonnier/repos/new_soycorn/new_soycorn/static/new_soycorn/articles"
        self.regex = re.compile("(\D+)(\d+)_(\d+)")
        self.day_count = {}
        self.article_list = []
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
        self.logger = SoycornLogger("transfer_articles", True)

    def run(self):
        self.logger.start()
        self.parse_links()
        self.rewrite_files()
        self.insert_into_db()
        self.logger.end()

    def bump_day_count(self, date_str):
        if date_str in self.day_count:
            self.day_count[date_str] += 1
        else:
            self.day_count[date_str] = 1

    def parse_date(self, date_str, article_data):
        split = self.regex.findall(date_str)
        if len(split) == 0 or len(split[0]) != 3:
            self.logger.error("parse_data failed len test with {0}".format(date_str))
            return False
        split = split[0]
        day = int(split[1])
        year = 2000 + int(split[2])
        if split[0] in self.month_map:
            month = self.month_map[split[0]]
        else:
            self.logger.error("parse_data failed month with {0}".format(date_str))
            return False
        self.bump_day_count(date_str)
        article_data.pub_date = datetime(year, month, day, 1, 10-self.day_count[date_str])
        self.logger.debug("date_str {0} turns into {1}".format(date_str, article_data.pub_date))
        return True

    def parse_links(self):
        with open(os.path.join(self.old_article_dir, "links")) as f:
            links = f.readlines()
        self.logger.info("Number of articles:{0}".format(len(links)))
        for l in links:
            l = l.strip()
            if ";" in l:
                self.logger.info("parse_link: {0}".format(l))
                split = l.split(";")
                article_data = ArticleData()
                article_data.file_name = split[0]
                article_data.name = split[1].strip()
                date_str = article_data.file_name.split("-")[0]
                if not self.parse_date(date_str, article_data):
                    self.logger.error("Could not split {0}".format(l))
                self.article_list.append(article_data)
                self.logger.debug("Article data:{0}".format(article_data))

    def rewrite_files(self):
        for article_data in self.article_list:
            self.logger.debug("{0}".format(article_data))
            with open(os.path.join(self.old_article_dir, article_data.file_name), "rb") as f:
                old_str = f.read()
            with open(os.path.join(self.new_article_dir, article_data.file_name), "w") as f:
                f.write(old_str)
            print "boo"

    def insert_into_db(self):
        for article_data in self.article_list:
            a = Article(name=article_data.name, pub_date=article_data.pub_date, file=article_data.file_name)
            a.save()

# if __name__ == "__main__":
#     t = Transfer()
#     t.run()