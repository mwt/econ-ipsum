# api/index.py
from http.server import BaseHTTPRequestHandler
from os.path import join
from random import choice, choices
from pickle import load
from re import compile as recompile


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        binomial = [12, 13, 14, 14, 15, 15, 15, 15, 16, 16, 16, 16, 16, 16, 17, 17, 17,
            17, 17, 17, 17, 17, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 19, 19,
            19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 20, 20, 20, 20, 20, 20, 20,
            20, 20, 20, 20, 20, 20, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
            21, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 23, 23, 23, 23, 23, 23,
            23, 23, 24, 24, 24, 24, 24, 24, 25, 25, 25, 25, 26, 26, 27, 28]

        with open(join("data", "dictionary.p"), "rb") as file:
            jdictionary = load(file)

        # Initialize text
        p = ""

        # Create a regex to ignore punctuation
        alphanumonly = recompile(r"\w+")

        # Generate a list containing lengths of each paragraphs
        parlen = choices(population=range(4, 11), k=100)
        for nsp in parlen:  # for each paragraph
            # Selecting number of sentences in a paragraph
            p += "<p>"
            for ns in range(nsp):
                # Selecting number of words in sentence
                nw = choice(binomial)
                s = [choice(jdictionary[0])]
                for i in range(nw - 1):
                    new = s[i]
                    while alphanumonly.findall(new.lower()) == alphanumonly.findall(
                        s[i].lower()
                    ):
                        new = choice(jdictionary[i + 1])
                    s.append(new)
                for i in range(-2, 0):
                    new = s[nw + i + 1]
                    while alphanumonly.findall(new.lower()) == alphanumonly.findall(
                        s[nw + i + 1].lower()
                    ):
                        new = choice(jdictionary[i])
                    s.append(new)
                p += " ".join(s) + ". "
            p += "</p>\n"
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(p[:-1].encode())
            return
