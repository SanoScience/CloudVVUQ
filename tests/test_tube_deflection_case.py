import os
import json
import unittest

from cloudvvuq.easy_executor import Executor

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../credentials/credentials.json'
url = "https://europe-west1-sano-332607.cloudfunctions.net/TubeDeflection"  # Cloud Functions
# url = "https://dx6qs64nzckbqqfh73g4m5ssqq0yjmhz.lambda-url.eu-central-1.on.aws/"  # AWS lambda


class TestTubeDeflectionCase(unittest.TestCase):
    def test_tube_deflection(self):
        executor = Executor(url)

        samples = [{'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 0.7347159221014868, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 0.7347159221014868, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 0.7347159221014868, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 0.7347159221014868, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 0.8650047391037858, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 0.8650047391037858, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 0.8650047391037858, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 0.8650047391037858, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 1.0349952608962139, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 1.0349952608962139, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 1.0349952608962139, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 1.0349952608962139, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 1.1652840778985132, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 1.1652840778985132, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 1.1652840778985132, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 1.1652840778985132, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4925803621569729, 'a': 0.7347159221014868, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4925803621569729, 'a': 0.7347159221014868, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4925803621569729, 'a': 0.7347159221014868, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4925803621569729, 'a': 0.7347159221014868, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4925803621569729, 'a': 0.8650047391037858, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4925803621569729, 'a': 0.8650047391037858, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4925803621569729, 'a': 0.8650047391037858, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4925803621569729, 'a': 0.8650047391037858, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4925803621569729, 'a': 1.0349952608962139, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4925803621569729, 'a': 1.0349952608962139, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4925803621569729, 'a': 1.0349952608962139, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4925803621569729, 'a': 1.0349952608962139, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4925803621569729, 'a': 1.1652840778985132, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4925803621569729, 'a': 1.1652840778985132, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4925803621569729, 'a': 1.1652840778985132, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4925803621569729, 'a': 1.1652840778985132, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.5074196378430273, 'a': 0.7347159221014868, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.5074196378430273, 'a': 0.7347159221014868, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.5074196378430273, 'a': 0.7347159221014868, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.5074196378430273, 'a': 0.7347159221014868, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.5074196378430273, 'a': 0.8650047391037858, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.5074196378430273, 'a': 0.8650047391037858, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.5074196378430273, 'a': 0.8650047391037858, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.5074196378430273, 'a': 0.8650047391037858, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.5074196378430273, 'a': 1.0349952608962139, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.5074196378430273, 'a': 1.0349952608962139, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.5074196378430273, 'a': 1.0349952608962139, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.5074196378430273, 'a': 1.0349952608962139, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.5074196378430273, 'a': 1.1652840778985132, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.5074196378430273, 'a': 1.1652840778985132, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.5074196378430273, 'a': 1.1652840778985132, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.5074196378430273, 'a': 1.1652840778985132, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.52334414218339, 'a': 0.7347159221014868, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.52334414218339, 'a': 0.7347159221014868, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.52334414218339, 'a': 0.7347159221014868, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.52334414218339, 'a': 0.7347159221014868, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.52334414218339, 'a': 0.8650047391037858, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.52334414218339, 'a': 0.8650047391037858, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.52334414218339, 'a': 0.8650047391037858, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.52334414218339, 'a': 0.8650047391037858, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.52334414218339, 'a': 1.0349952608962139, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.52334414218339, 'a': 1.0349952608962139, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.52334414218339, 'a': 1.0349952608962139, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.52334414218339, 'a': 1.0349952608962139, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.52334414218339, 'a': 1.1652840778985132, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.52334414218339, 'a': 1.1652840778985132, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.52334414218339, 'a': 1.1652840778985132, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.52334414218339, 'a': 1.1652840778985132, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4766558578166098, 'a': 0.7347159221014868, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4766558578166098, 'a': 0.7347159221014868, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4766558578166098, 'a': 0.7347159221014868, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4766558578166098, 'a': 0.7347159221014868, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4766558578166098, 'a': 0.8650047391037858, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4766558578166098, 'a': 0.8650047391037858, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4766558578166098, 'a': 0.8650047391037858, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4766558578166098, 'a': 0.8650047391037858, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4766558578166098, 'a': 1.0349952608962139, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4766558578166098, 'a': 1.0349952608962139, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4766558578166098, 'a': 1.0349952608962139, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4766558578166098, 'a': 1.0349952608962139, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4766558578166098, 'a': 1.1652840778985132, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4766558578166098, 'a': 1.1652840778985132, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4766558578166098, 'a': 1.1652840778985132, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4766558578166098, 'a': 1.1652840778985132, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4925803621569729, 'a': 0.7347159221014868, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4925803621569729, 'a': 0.7347159221014868, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4925803621569729, 'a': 0.7347159221014868, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4925803621569729, 'a': 0.7347159221014868, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4925803621569729, 'a': 0.8650047391037858, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4925803621569729, 'a': 0.8650047391037858, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4925803621569729, 'a': 0.8650047391037858, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4925803621569729, 'a': 0.8650047391037858, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4925803621569729, 'a': 1.0349952608962139, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4925803621569729, 'a': 1.0349952608962139, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4925803621569729, 'a': 1.0349952608962139, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4925803621569729, 'a': 1.0349952608962139, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4925803621569729, 'a': 1.1652840778985132, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4925803621569729, 'a': 1.1652840778985132, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4925803621569729, 'a': 1.1652840778985132, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.4925803621569729, 'a': 1.1652840778985132, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.5074196378430273, 'a': 0.7347159221014868, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.5074196378430273, 'a': 0.7347159221014868, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.5074196378430273, 'a': 0.7347159221014868, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.5074196378430273, 'a': 0.7347159221014868, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.5074196378430273, 'a': 0.8650047391037858, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.5074196378430273, 'a': 0.8650047391037858, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.5074196378430273, 'a': 0.8650047391037858, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.5074196378430273, 'a': 0.8650047391037858, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.5074196378430273, 'a': 1.0349952608962139, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.5074196378430273, 'a': 1.0349952608962139, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.5074196378430273, 'a': 1.0349952608962139, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.5074196378430273, 'a': 1.0349952608962139, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.5074196378430273, 'a': 1.1652840778985132, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.5074196378430273, 'a': 1.1652840778985132, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.5074196378430273, 'a': 1.1652840778985132, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.5074196378430273, 'a': 1.1652840778985132, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.52334414218339, 'a': 0.7347159221014868, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.52334414218339, 'a': 0.7347159221014868, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.52334414218339, 'a': 0.7347159221014868, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.52334414218339, 'a': 0.7347159221014868, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.52334414218339, 'a': 0.8650047391037858, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.52334414218339, 'a': 0.8650047391037858, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.52334414218339, 'a': 0.8650047391037858, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.52334414218339, 'a': 0.8650047391037858, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.52334414218339, 'a': 1.0349952608962139, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.52334414218339, 'a': 1.0349952608962139, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.52334414218339, 'a': 1.0349952608962139, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.52334414218339, 'a': 1.0349952608962139, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.52334414218339, 'a': 1.1652840778985132, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.52334414218339, 'a': 1.1652840778985132, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.52334414218339, 'a': 1.1652840778985132, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.9258036215697274, 'L': 1.52334414218339, 'a': 1.1652840778985132, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4766558578166098, 'a': 0.7347159221014868, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4766558578166098, 'a': 0.7347159221014868, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4766558578166098, 'a': 0.7347159221014868, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4766558578166098, 'a': 0.7347159221014868, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4766558578166098, 'a': 0.8650047391037858, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4766558578166098, 'a': 0.8650047391037858, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4766558578166098, 'a': 0.8650047391037858, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4766558578166098, 'a': 0.8650047391037858, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4766558578166098, 'a': 1.0349952608962139, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4766558578166098, 'a': 1.0349952608962139, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4766558578166098, 'a': 1.0349952608962139, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4766558578166098, 'a': 1.0349952608962139, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4766558578166098, 'a': 1.1652840778985132, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4766558578166098, 'a': 1.1652840778985132, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4766558578166098, 'a': 1.1652840778985132, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4766558578166098, 'a': 1.1652840778985132, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4925803621569729, 'a': 0.7347159221014868, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4925803621569729, 'a': 0.7347159221014868, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4925803621569729, 'a': 0.7347159221014868, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4925803621569729, 'a': 0.7347159221014868, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4925803621569729, 'a': 0.8650047391037858, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4925803621569729, 'a': 0.8650047391037858, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4925803621569729, 'a': 0.8650047391037858, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4925803621569729, 'a': 0.8650047391037858, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4925803621569729, 'a': 1.0349952608962139, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4925803621569729, 'a': 1.0349952608962139, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4925803621569729, 'a': 1.0349952608962139, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4925803621569729, 'a': 1.0349952608962139, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4925803621569729, 'a': 1.1652840778985132, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4925803621569729, 'a': 1.1652840778985132, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4925803621569729, 'a': 1.1652840778985132, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.4925803621569729, 'a': 1.1652840778985132, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.5074196378430273, 'a': 0.7347159221014868, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.5074196378430273, 'a': 0.7347159221014868, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.5074196378430273, 'a': 0.7347159221014868, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.5074196378430273, 'a': 0.7347159221014868, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.5074196378430273, 'a': 0.8650047391037858, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.5074196378430273, 'a': 0.8650047391037858, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.5074196378430273, 'a': 0.8650047391037858, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.5074196378430273, 'a': 0.8650047391037858, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.5074196378430273, 'a': 1.0349952608962139, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.5074196378430273, 'a': 1.0349952608962139, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.5074196378430273, 'a': 1.0349952608962139, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.5074196378430273, 'a': 1.0349952608962139, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.5074196378430273, 'a': 1.1652840778985132, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.5074196378430273, 'a': 1.1652840778985132, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.5074196378430273, 'a': 1.1652840778985132, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.5074196378430273, 'a': 1.1652840778985132, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.52334414218339, 'a': 0.7347159221014868, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.52334414218339, 'a': 0.7347159221014868, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.52334414218339, 'a': 0.7347159221014868, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.52334414218339, 'a': 0.7347159221014868, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.52334414218339, 'a': 0.8650047391037858, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.52334414218339, 'a': 0.8650047391037858, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.52334414218339, 'a': 0.8650047391037858, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.52334414218339, 'a': 0.8650047391037858, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.52334414218339, 'a': 1.0349952608962139, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.52334414218339, 'a': 1.0349952608962139, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.52334414218339, 'a': 1.0349952608962139, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.52334414218339, 'a': 1.0349952608962139, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.52334414218339, 'a': 1.1652840778985132, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.52334414218339, 'a': 1.1652840778985132, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.52334414218339, 'a': 1.1652840778985132, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.0741963784302726, 'L': 1.52334414218339, 'a': 1.1652840778985132, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4766558578166098, 'a': 0.7347159221014868, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4766558578166098, 'a': 0.7347159221014868, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4766558578166098, 'a': 0.7347159221014868, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4766558578166098, 'a': 0.7347159221014868, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4766558578166098, 'a': 0.8650047391037858, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4766558578166098, 'a': 0.8650047391037858, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4766558578166098, 'a': 0.8650047391037858, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4766558578166098, 'a': 0.8650047391037858, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4766558578166098, 'a': 1.0349952608962139, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4766558578166098, 'a': 1.0349952608962139, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4766558578166098, 'a': 1.0349952608962139, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4766558578166098, 'a': 1.0349952608962139, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4766558578166098, 'a': 1.1652840778985132, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4766558578166098, 'a': 1.1652840778985132, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4766558578166098, 'a': 1.1652840778985132, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4766558578166098, 'a': 1.1652840778985132, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4925803621569729, 'a': 0.7347159221014868, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4925803621569729, 'a': 0.7347159221014868, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4925803621569729, 'a': 0.7347159221014868, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4925803621569729, 'a': 0.7347159221014868, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4925803621569729, 'a': 0.8650047391037858, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4925803621569729, 'a': 0.8650047391037858, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4925803621569729, 'a': 0.8650047391037858, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4925803621569729, 'a': 0.8650047391037858, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4925803621569729, 'a': 1.0349952608962139, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4925803621569729, 'a': 1.0349952608962139, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4925803621569729, 'a': 1.0349952608962139, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4925803621569729, 'a': 1.0349952608962139, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4925803621569729, 'a': 1.1652840778985132, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4925803621569729, 'a': 1.1652840778985132, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4925803621569729, 'a': 1.1652840778985132, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.4925803621569729, 'a': 1.1652840778985132, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.5074196378430273, 'a': 0.7347159221014868, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.5074196378430273, 'a': 0.7347159221014868, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.5074196378430273, 'a': 0.7347159221014868, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.5074196378430273, 'a': 0.7347159221014868, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.5074196378430273, 'a': 0.8650047391037858, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.5074196378430273, 'a': 0.8650047391037858, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.5074196378430273, 'a': 0.8650047391037858, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.5074196378430273, 'a': 0.8650047391037858, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.5074196378430273, 'a': 1.0349952608962139, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.5074196378430273, 'a': 1.0349952608962139, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.5074196378430273, 'a': 1.0349952608962139, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.5074196378430273, 'a': 1.0349952608962139, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.5074196378430273, 'a': 1.1652840778985132, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.5074196378430273, 'a': 1.1652840778985132, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.5074196378430273, 'a': 1.1652840778985132, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.5074196378430273, 'a': 1.1652840778985132, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.52334414218339, 'a': 0.7347159221014868, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.52334414218339, 'a': 0.7347159221014868, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.52334414218339, 'a': 0.7347159221014868, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.52334414218339, 'a': 0.7347159221014868, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.52334414218339, 'a': 0.8650047391037858, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.52334414218339, 'a': 0.8650047391037858, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.52334414218339, 'a': 0.8650047391037858, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.52334414218339, 'a': 0.8650047391037858, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.52334414218339, 'a': 1.0349952608962139, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.52334414218339, 'a': 1.0349952608962139, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.52334414218339, 'a': 1.0349952608962139, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.52334414218339, 'a': 1.0349952608962139, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.52334414218339, 'a': 1.1652840778985132, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.52334414218339, 'a': 1.1652840778985132, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.52334414218339, 'a': 1.1652840778985132, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 1.2334414218338974, 'L': 1.52334414218339, 'a': 1.1652840778985132, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}]
        outputs = executor.run(samples, max_load=256, cloud_provider="gcp")

        other_outputs = json.load(open("test_data/tube_outputs.json"))
        assert sorted(outputs, key=lambda x: x["input_id"]) == other_outputs


if __name__ == "__main__":
    unittest.main()
