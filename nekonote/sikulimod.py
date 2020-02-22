# encoding: utf-8

from sikuli import * # pylint: disable=wildcard-import,redefined-builtin,unused-wildcard-import

class MatchedImage(object):
    def __init__(self, match, candidates):
        self.region = match
        self.filename = os.path.basename(candidates[match.getIndex()])
        self.screen, self.label = self.filename.split("-")
        if self.label.startswith("0"):
            self.label = None
        else:
            self.label = self.label.split(".")[0]
        self.kind = (self.screen, self.label)

    def __str__(self):
        return "%s, %s" % (self.region, self.filename)

    def get_score(self):
        return self.region.getScore()

    def highlight(self, sec):
        return self.region.highlight(sec)

    def click(self):
        return self.region.click()
