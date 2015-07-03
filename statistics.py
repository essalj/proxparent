import json

def sum_category(category, json_dict):
    sum_cat = 0
    for param in json_dict[category].keys():
        sum_cat += int(json_dict[category][param])
    return sum_cat

def calc_percentage(category, data):
    sum = sum_category(category, data)
    pre_dict = {}
    for url in json_dict[category]:
        pre_dict[url] = (round((int(json_dict[category][url])*1.0 / int(sum)*1.0)*100, 2))
    return pre_dict

def sort_percentage(pre_dict):
    # Copied from the Internet
    new_dict = {}
    for key, value in sorted(pre_dict.iteritems(), key=lambda (k, v): (v, k), reverse=True):
        print key + " -> " + str(value) + "%"

def run():
    print "Categories: \n"
    global  json_dict
    json_dict = json.loads(open('jsondata.json').read())
    for i in json_dict:
        print i
    cat = raw_input("\nWhich category would you like to see: ")
    while not cat in json_dict:
        print cat + " category does not exist. See the category list above."
        cat = raw_input("\nWhich category would you like to see: ")

    sort_percentage(calc_percentage(cat, json_dict))

run()

raw_input("Press enter to exit...")
