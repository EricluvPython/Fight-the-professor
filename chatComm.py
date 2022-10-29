import socket


class chatComm:
    # constructor function. ip address and port number are needed
    def __init__(self, ipaddress, portnum):
        self.ipaddress = ipaddress
        self.portnum = portnum

    # esetablish connection to the specified server
    def startConnection(self):
        # construct socket object
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to server
        self.socket.connect((self.ipaddress, self.portnum))
        return

    # log in to server with username, password, and md5
    def login(self, username, password):
        def generateBlock(password, challenge):
            message = password+challenge
            block = message+'1'
            lenMessage = len(message)
            numMessages = (512-3-len(block))//lenMessage
            len0s = (512-3-len(block))-numMessages*lenMessage
            for i in range(numMessages):
                block += message
            for i in range(len0s):
                block += '0'
            block += '0'*(3-len(str(lenMessage)))+str(lenMessage)
            return block

        def generateAsciiChunks(block):
            M = []
            # sum the ascii of every 32 chars
            for i in range(0, 512, 32):
                cnt = 0
                chars = block[i:i+32]
                for char in chars:
                    cnt += ord(char)
                M.append(cnt)
            return M

        def leftRotate(x, c):
            return (x << c) & 0xFFFFFFFF | (x >> (32-c) & 0x7FFFFFFF >> (32-c))

        def hexHash(M):
            s = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
                 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]
            K = [0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
                 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
                 0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
                 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
                 0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
                 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
                 0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
                 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
                 0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
                 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
                 0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
                 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
                 0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
                 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
                 0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
                 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391]
            A = a0 = 0x67452301
            B = b0 = 0xefcdab89
            C = c0 = 0x98badcfe
            D = d0 = 0x10325476
            for i in range(64):
                if 0 <= i <= 15:
                    F = (B & C) | ((~B) & (D))
                    F = F & 0xFFFFFFFF
                    g = i
                elif 16 <= i <= 31:
                    F = (D & B) | ((~D) & C)
                    F = F & 0xFFFFFFFF
                    g = (5*i+1) % 16
                elif 32 <= i <= 47:
                    F = B ^ C ^ D
                    F = F & 0xFFFFFFFF
                    g = (3*i+5) % 16
                elif 48 <= i <= 63:
                    F = C ^ (B | (~D))
                    F = F & 0xFFFFFFFF
                    g = (7*i) % 16
                dTemp = D
                D = C
                C = B
                B = B+leftRotate((A+F+K[i]+M[g]), s[i])
                B = B & 0xFFFFFFFF
                A = dTemp
            a0 = (a0+A) & 0xFFFFFFFF
            b0 = (b0+B) & 0xFFFFFFFF
            c0 = (c0+C) & 0xFFFFFFFF
            d0 = (d0+D) & 0xFFFFFFFF
            result = str(a0)+str(b0)+str(c0)+str(d0)
            return result

        # main logic of md5 hashing
        def md5Hash(password, challenge):
            block = generateBlock(password, challenge)
            M = generateAsciiChunks(block)
            result = hexHash(M)
            return str(result)
        self.socket.send(b"LOGIN "+username.encode('utf-8')+b'\n')
        challenge = self.socket.recv(1024).decode().split()[2]
        messageDigest = md5Hash(password, challenge)
        self.socket.send(
            b"LOGIN "+(username+" "+messageDigest).encode('utf-8')+b"\n")
        status = self.socket.recv(1024).decode()
        return ("Successful" in status)

    # get my friends list
    def getFriends(self):
        self.socket.send(b"@friends")
        size = int(self.socket.recv(6).decode()[1:])
        data = self.socket.recv(size-6).decode()
        diff = size-6-len(data)
        while diff > 0:
            data += self.socket.recv(diff).decode()
            diff = size-6-len(data)
        data = data.split("@")
        return data[3:]

    # send message to others
    def sendMessage(self, friend, message):
        info = "@sendmsg@"+friend+"@"+message
        size = (5-len(str((len(info)+6))))*'0'+str((len(info)+6))
        data = "@"+size+info
        self.socket.send(data.encode('utf-8'))
        status = self.socket.recv(64).decode()
        return "ok" in status

    # send file to others
    def sendFile(self, friend, filename):
        with open(filename) as f:
            content = ''.join(f.readlines())
        info = "@sendfile@"+friend+"@"+filename+"@"+content
        size = (5-len(str((len(info)+6))))*'0'+str((len(info)+6))
        data = "@"+size+info
        self.socket.send(data.encode('utf-8'))
        status = self.socket.recv(64).decode()
        return "ok" in status

    # check received messages and files
    def getMail(self):
        self.socket.send(b"@rxmsg")
        size = int(self.socket.recv(6).decode()[1:])
        data = self.socket.recv(size-6).decode()
        diff = size-6-len(data)
        while diff > 0:
            data += self.socket.recv(diff).decode()
            diff = size-6-len(data)
        data = data.split("@")
        messages = []
        files = []
        for i in range(len(data)):
            if data[i] == "msg":
                messages.append((data[i+1], data[i+2]))
            elif data[i] == "file":
                files.append((data[i+1], data[i+2]))
                with open(data[i+2], 'w') as f:
                    f.write(data[i+3])
        return (messages, files)
