import proselint

suggest = proselint.tools.lint

fh = open("../data/example.txt", "r")
raw_text = fh.read()
fh.close()

suggestions = suggest(raw_text)

def process_suggestions(list):
    alarms = []
    for suggestion in suggestions:
        alarms.append("(" + suggestion[7] + ") " + suggestion[1])


    return alarms


def about_linter():
    fh = open("../data/suggestions.txt")
    raw_text = fh.readlines()
    about_suggestions = []
    for line in raw_text:
        line.replace("\n", "")
        about_suggestions.append(line.split(":"))
    alert_list = []
    for line in about_suggestions:
        alert_list.append(line[1])
    return alert_list
def header():
    print "Auto Suggest Report\n------------------------"
    print "\n\n"
    print "Preface\n++++++++++++\n\n"
    alert_list = about_linter()
    for alert in alert_list:
        print("* " + alert)

def body(alarms):
    print("Initial Sniff of Text\n---------------------------\n")
    print("Duplicate warnings appear if the tools saw an issue in multiple places. The following tips were generated:\n")
    for alarm in alarms:
        print("* " + alarm + "\n")


header()
alarms = process_suggestions(suggestions)
body(alarms)
