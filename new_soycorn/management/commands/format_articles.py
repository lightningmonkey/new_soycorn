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
        f = Format()
        f.run()

class Format(object):
    def __init__(self):
        self.new_article_dir = "/Users/bcordonnier/repos/new_soycorn/new_soycorn/static/new_soycorn/articles"

    def run(self):
        for (dirpath, dirnames, file_list) in os.walk(self.new_article_dir):
            for file in file_list:
                with open(os.path.join(dirpath, file), 'r') as f:
                    all_lines = f.readlines()
                all_lines[0] = "<h4>{0}</h4>\n".format(all_lines[0].strip())
                all_lines[1] = "<h3>{0}</h3>\n".format(all_lines[1].strip())

                with open(os.path.join(dirpath, file), 'w') as f:
                    f.writelines(all_lines)