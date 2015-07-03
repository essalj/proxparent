__author__ = 'Guy'


def block_website():
    import re
    website = raw_input("Please enter the base url of the website you would like to block: ")
    url_regex = r'[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?(\?([-a-zA-Z0-9@:%_\+.~#?&//=]+)|)'
    while not re.search(url_regex, website):
        print "\nURL is invalid"
        print "Example: google.com\n"
        website = raw_input("Please enter the base url of the website you would like to block: ")

    with open('blacklist.txt', 'a') as f:
        f.write(website+"\n")
    print website + " has been added to the blacklist successfully"

import os.path
if not os.path.isfile('password.txt'):
    print "Hello"
    import hashlib
    password = hashlib.sha1(raw_input("Please set a password: "))
    print password.hexdigest()
    with open('password.txt', 'w') as f:
        f.write(password.hexdigest())
else:
    with open('password.txt', 'r') as f:
        password = f.read()
        import hashlib
        if password == hashlib.sha1(raw_input("Password: ")).hexdigest():
            print "What would you like to do: "
            print "1. Block a website\n" \
                  "2. Block a word\n" \
                  "3. View statistics"
            action = raw_input("Answer number: ")
            while not int(action) <= 3 or not int(action) >= 1:
                print "Please choose an id from the list above"
                action = raw_input("Answer number: ")
            action = int(action)
            if action == 1:
                block_website()
            elif action == 2:
                import json
                with open('bad_words.txt', 'r+') as f:

                    words = json.loads(f.read())
                    words["CUSTOM"].append(raw_input("Please enter the word that you would like to block: "))
                with open('bad_words.txt', 'w') as f:
                    f.write(json.dumps(words, indent=4))
                    print "The word has been added to the blacklist successfully"
            elif action == 3:
                import statistics
                statistics.run()
                #statistics()
raw_input("Press enter to exit...")
