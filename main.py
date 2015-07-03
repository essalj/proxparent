def end():
    global run
    run = False
run = True

def main():
    if run:
        import socket
        import sys
        import time
        import thread
        import re
        import json

        HOST = '127.0.0.1'  # Address to attach the proxy to
        PORT = 8080  # Port
        MAX_REQUEST_SIZE = 8192  # Max client requests size in bytes
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        blacklist = open('blacklist.txt').read().splitlines()  # Reading the website blacklist file
        bad_words = json.loads(open('bad_words.txt').read())  # Reading the blocked words list in json

        def display_message(message):

            if __name__ == '__main__':
                print message
            else:
                print message
                gui.insert_log(message)

        display_message( 'Socket created')


        def save_json():
            """
            Encodes the statistics dictionary into JSON text and saves it
            """
            #global data
            #with open('jsondata.json', 'w') as f:
            #    f.write(json.dumps(data, indent=4))



        json_read = open('jsondata.json', 'r')
        global data
        data = json.loads(json_read.read())
        json_read.close()


        def json_push(jsonout, subject, name):
            """
            Updates the statistics dictionary

            :param jsonout: statistics dictionary (decoded JSON dictionary)
            :param subject: statistics category
            :param name: statistics value to update
            :returns: updated statistics dictionary
            """
            if type(jsonout) is dict and name in jsonout[subject]:
                jsonout[subject][name] = int(jsonout[subject][name]) + 1
            else:
                jsonout[subject][name] = 1
            return jsonout

        def write_json(value, subject):
            """
            Activates the json_push function

            :param value: statistics value to update
            :param subject:  statistics category
            """
            global data
            data = json_push(data, subject, value)





        def disable_gzip(data):
            """
            Removes the Accept-Encoding from the request in order to not accept GZIP

            :param data: client request
            :returns: updated headers
            """
            if data.find('\r\n\r\n') != -1:
                raw_headers = data.split('\r\n\r\n')
            else:
                return data
            dict_headers = {}
            for header in raw_headers[0].splitlines():
                if header.find(':') != -1:
                    current_header = header.split(':')
                    dict_headers[current_header[0]] = current_header[1]
                else:
                    continue
            if dict_headers.has_key("Accept-Encoding"):
                del dict_headers["Accept-Encoding"]

            request = raw_headers[0].splitlines()[0] + "\r\n"
            for i in dict_headers:
                if not i.startswith("GET "):
                    request += i + ":" + dict_headers[i] + "\r\n"
                else:
                    continue
            return (request + "\r\n")


        def remove_word(content, index, word):
            """
            Replaces a word in the content with '*'

            :param content: content to update
            :param index: index of word to remove
            :param word: the word to remove
            :returns: updated content
            """
            return content[0:index]+'*'*len(word)+content[index+len(word):]

        def find_all(word, content):
            """
            Finds all occurrences of a word in the content

            :param word: word to search
            :param content: content to search in
            :returns: list of words occurrences index
            """
            return [m.start() for m in re.finditer(word.strip(), content)]

        def is_in_tag(data, index):
            """
            Checks whether a word or an index is inside an HTML tag or not

            :param data: HTML content
            :param index: index to check
            :returns: true or false
            """

            start_index = index
            while not data[start_index] == "<":
                if start_index >= 1:
                     start_index -= 1
                else:
                    return False
                end_index = start_index
                while not data[end_index] == ">":
                    if end_index < len(data)-1:
                        end_index += 1
                    else:
                        return False
            if end_index < index:
                return False
            else:
                return True

        def filter_data(content):
            """
            Filters the server response according to the rules

            :param content: content to filter
            :returns: filtered content
            """
            for category in bad_words:
                for word in bad_words[category]:
                    all = find_all(word, content)

                    for i in all:
                        if not is_in_tag(content, i):
                            write_json(word, "Blocked_Words")
                            write_json(category, "Blocked_Words_Categories")

                            display_message( word + " removed. -> Reason: "+category)
                            content = remove_word(content, i, word)
            return content




        def extract_dest(request):
            """
            Extracts the destination URL of a requests

            :param request: client request
            :returns: url
            """
            url = ""
            port = ""
            headers = {}
            for i in request.splitlines():
                if i.find(":") != -1:
                    headers[i.split(":")[0]] = i.split(":")[1]
            first_line = request.splitlines()[0]
            type, dir, version = first_line.split()
            url_regex=r'/\b(([\w-]+:\/\/?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|\/)))/i'
            if re.search(url_regex, dir):
                if url.find(':') != -1:
                    return (dir, port)
                else:
                    return (dir, 80)
            elif "Host" in headers.keys():
                return (headers['Host'], 80)
            else:
                sys.exit()

        try:
            s.bind((HOST, PORT))
        except socket.error as e:
            display_message( 'Bind failed. Message: ' + e[1])
            sys.exit()
        display_message( 'Socket bind complete')

        s.listen(100)

        def socket_thread(sock, addr):
            """
            The main program

            Connects between the client and the server, filters the content and more...

            :param sock: client socket
            :addr: client socket ip
            """
            while True and sock:
                # Validation of the base request and error handling
                try:
                    request = sock.recv(MAX_REQUEST_SIZE)
                except:
                    pass

                if not request:
                    break

                if request.find('\r\n\r\n') == -1:
                    sock.send("")
                    sys.exit()

                # Destination address extraction
                address, port = extract_dest(request)
                address = address.strip()

                # User-Agent extraction
                dict_headers = {}
                if request.find('\r\n\r\n') != -1:
                    raw_headers = request.split('\r\n\r\n')
                    for header in raw_headers[0].splitlines():
                        if header.find(':') != -1:
                            current_header = header.split(':')
                            dict_headers[current_header[0]] = current_header[1]
                    if "User-Agent" in dict_headers:
                        user_agent = dict_headers["User-Agent"]
                        # write_json(user_agent, "User-Agents")
                    request = disable_gzip(request)

                # Website blocking
                for i in blacklist:
                    if address.find(i) != -1:
                        write_json(address, "Blocked_Requests_URL")

                        display_message( (address+" blocked!"))
                        # Website blocked response
                        sock.send("""HTTP/1.1 403 Forbidden\r\n\r\n
                                <!doctype html>
                                <html>
                                <head>
                                    <title>Website Blocked!</title>
                                </head>
                                <body>
                                <div id="main" style="background-color: #FF9494; text-align:center; border-radius:10px; width:80%; margin: 0 auto; padding: 20px;">

                                    <img alt="Error!" src="data:image/png;base64,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" title="You are not allowed" />


                                <div id="text" style="height:100%; width:100%;>
                                <p style="text-align: center;"><span style="font-size:36px;"><span style="font-family:tahoma,geneva,sans-serif;">The website has been blocked!</span></span><br />
                                <span style="font-family:tahoma,geneva,sans-serif;">The website <strong> """+address+""" </strong>has been blocked.<br />
                                You are not allowed to access websites like this.</span></p>

                                <p style="text-align: center;"><font face="tahoma, geneva, sans-serif">A notification has been sent to your parents.</font></p>
                                </div>
                                </div>
                                </body>
                                </html>""")
                        sock.send("")
                        sock.shutdown(2)
                        sys.exit()

                try:
                    # Update statistics
                    write_json(address, "Requests_URL")
                except:
                    display_message( "Error saving statistics.")

                """ :param req_sock: remote server socket """
                req_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    req_sock.connect((address, int(port)))
                    req_sock.send(request)
                    req_sock.settimeout(3)
                    count = 0
                    while True:
                        try:
                            data = req_sock.recv(MAX_REQUEST_SIZE)
                        except socket.timeout:
                            req_sock.settimeout(0.1)
                            count += 1
                            if count > 2:
                                sock.shutdown(2)
                                sys.exit()
                            continue

                        if len(data) > 0:
                            data = filter_data(data)
                            sock.send(data)
                        else:
                            break

                    req_sock.close()
                    sock.close()
                    sys.exit()

                except socket.error:
                    if req_sock:
                        req_sock.close()

                    if sock:
                        closed = False
                        sock.close()
                    sys.exit()


        try:
            count = 1
            while True:
                try:
                    conn, addr = s.accept()
                    save_json()
                    thread.start_new_thread(socket_thread, (conn, addr))
                    count += 1
                except KeyboardInterrupt:
                    conn.close()
        except():
            pass


    if __name__ == '__main__':
        main()

        # --- GZIP decompression class --- #
        # class Gzip:
        #     def run(self):
        #         if self.is_gzip():
        #             self.data = self.decode_gzip()
        #
        #
        #
        #     def __init__(self, data, run=False):
        #         self.data = data
        #         if run:
        #             self.run()
        #
        #
        #
        #     def render_headers(self):
        #
        #         if self.data.find('\r\n\r\n') != -1:
        #             raw_headers = self.data.split('\r\n\r\n')
        #         else:
        #             return {}
        #         dict_headers = {}
        #         for header in raw_headers[0].splitlines():
        #             if header.find(':')!=-1:
        #                 current_header = header.split(':')
        #                 dict_headers[current_header[0]] = current_header[1]
        #             else:
        #                 continue
        #         return dict_headers
        #
        #     def is_gzip(self):
        #         headers = self.render_headers()
        #         if 'Content-Encoding' in headers.keys():
        #
        #             if headers['Content-Encoding'].strip() == 'gzip':
        #                 return True
        #                 display_message( "Is GZIP!"
        #             else:
        #                 return False
        #         else:
        #             return False
        #
        #     def decode_gzip(self):
        #         import gzip
        #         import StringIO
        #         #return gzip.GzipFile('', 'rb', 9, StringIO.StringIO(self.data)).read()
        #         with open("file.gz", "wb") as f:
        #             f.write(self.data.split('\r\n\r\n')[1].strip().split('\r\n')[1])
        #         f = gzip.GzipFile(fileobj=open('file.gz', 'rb'))
        #         new_data = ""
        #         while True:
        #             try:
        #                 new_data += f.read(1)
        #             except IOError, e:
        #                 if str(e).find('CRC') != -1:
        #                     display_message( e
        #                     continue
        #                 else:
        #                     break
        #
        #         display_message( self.data.split('\r\n\r\n')[0] + new_data
        #         return self.data.split('\r\n\r\n')[0] + new_data
        #
