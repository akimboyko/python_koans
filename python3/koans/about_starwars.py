#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import re
from collections import OrderedDict, Counter
from functools import lru_cache

from runner.koan import *

# To run this koans we have to install several libraries
# pip install lxml
from lxml import html
# pip install requests
import requests

# pip install approvaltests
from approvaltests.Approvals import verify
from approvaltests.GenericDiffReporter import GenericDiffReporter


# this is approval test verification code based on git diff
def diff_verify(result):
    json_result = json.dumps(result, indent=4, separators=(',', ': '))
    diff_path = 'C:/Program Files/Git/usr/bin/diff.exe' if os.name == 'nt' else '/usr/bin/diff'
    verify(json_result, GenericDiffReporter(('Custom', diff_path)))

# link to script draft of Star Wars: a new hope
URL = "http://www.imsdb.com/scripts/Star-Wars-A-New-Hope.html"


class AboutStarWars(Koan):
    """ Explore draft of Star Wars: a new hope using regex and XPath """

    # loading page with script from internet
    @staticmethod
    @lru_cache(maxsize=None)
    def load_html_script_of_a_movie():
        response = requests.get(URL)

        # what is expected HTTP OK status code
        # take a look here https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
        if response.status_code == 200:
            return response.text
        else:
            assert False, "can't load script from IMDB"

    def test_perform_http_method_get_to_load_html(self):
        raw_html = AboutStarWars.load_html_script_of_a_movie()

        # now we have whole HTML page loaded, let verify it
        self.assertIsNotNone(raw_html)
        self.assertEqual(len(raw_html), 348725)

    @staticmethod
    def load_raw_line_by_line_script_of_a_movie():
        tree = html.fromstring(AboutStarWars.load_html_script_of_a_movie())

        # you could yse browser's developers tools to find script
        # here is an example http://pasteboard.co/AWrJYwQho.png
        #
        # here is examplanatino how to test XPath expressions
        # http://yizeng.me/2014/03/23/evaluate-and-validate-xpath-css-selectors-in-chrome-developer-tools/
        #
        # here you need to select all text within <td class="scrtext"><pre> ... </pre></td>
        movie_script = tree.xpath('//td[@class="scrtext"]/pre//text()')

        return movie_script

    def test_extracting_raw_script_from_html(self):
        movie_script = AboutStarWars.load_raw_line_by_line_script_of_a_movie()

        # lets check number of lines and content
        self.assertEqual(len(movie_script), 2992)
        diff_verify(movie_script)

    scene_name_regex = r'(INT|EXT)\.'
    role_name_regex = r'^\s*([A-Z\']+(\s[A-Z\']+)*)\s*$'

    def test_extracting_all_scenes_from_html_using_re(self):
        movie_script = AboutStarWars.load_raw_line_by_line_script_of_a_movie()
        diff_verify(self.extracting_all_scenes_and_roles(movie_script, self.scene_name_regex, self.role_name_regex))

    @staticmethod
    def load_b_tags_only_line_by_line():
        tree = html.fromstring(AboutStarWars.load_html_script_of_a_movie())

        # could we simplify calculations by extracting only text from within <b> ... </b> tags?
        movie_script = tree.xpath('//td[@class="scrtext"]//b/text()')

        return movie_script

    def test_extracting_names_from_html_using_xpath(self):
        b_tags_texts = AboutStarWars.load_b_tags_only_line_by_line()
        diff_verify(self.extracting_all_scenes_and_roles(b_tags_texts, self.scene_name_regex))

    def test_difference_between_two_results(self):
        movie_script = AboutStarWars.load_raw_line_by_line_script_of_a_movie()
        b_tags_texts = AboutStarWars.load_b_tags_only_line_by_line()

        re_results = self.extracting_all_scenes_and_roles(movie_script, self.scene_name_regex, self.role_name_regex)
        xpath_results = self.extracting_all_scenes_and_roles(b_tags_texts, self.scene_name_regex)

        # there should not be any difference between to results
        self.assertSetEqual(set(xpath_results) ^ set(re_results), set())

    def test_who_are_three_main_roles_by_number_of_phrases(self):
        movie_script = AboutStarWars.load_raw_line_by_line_script_of_a_movie()
        re_results = self.extracting_all_scenes_and_roles(movie_script, self.scene_name_regex, self.role_name_regex)

        top = Counter()

        for roles in re_results.values():
            top += Counter(roles)

        diff_verify(top.most_common(n=3))

    def test_who_is_important_but_never_speaks(self):
        """
        here is homework challenge:
        who is important, but never speaks?
        """

        role_name = __

        self.assertEqual(role_name, ___)

    @staticmethod
    def extracting_all_scenes_and_roles(movie_script, scene_name_regex, role_name_regex=r".+"):
        # I'd like to preserve chronological order of scenes and roles in scenes
        scenes = OrderedDict()

        current_scene_name = None

        scene_name_re = re.compile(scene_name_regex)
        role_name_re = re.compile(role_name_regex)

        for line in movie_script:
            line = line.strip()
            if scene_name_re.match(line):
                current_scene_name = line
            elif current_scene_name and role_name_re.match(line):
                role_name = line
                scene_counter = scenes.get(current_scene_name, OrderedDict())
                scene_counter[role_name] = scene_counter.get(role_name, 0) + 1
                scenes[current_scene_name] = scene_counter
            else:
                pass

        return scenes
