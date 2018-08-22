from lexical.lexicalanayzer import LexicalAnalyzer

if __name__ == "__main__":
    analyzer = LexicalAnalyzer()
    f = open('lms.txt', 'r')
    analyzer.run(f.read())