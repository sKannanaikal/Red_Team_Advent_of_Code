import argparse
import requests

matches = []

def attemptConnection(host, dirname):
    with requests.get('{host}/{dirname}'.format(host=host, dirname=dirname), stream=True) as r:
        if r.status_code == 404:
            return
        else:
            print('[+] Found a Match: {dirname}'.format(dirname=dirname))
            matches.append(dirname)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, required=True, help='The target of the port scan')
    parser.add_argument('--wordlist', type=str, required=True, help='A bank of words to search up as potential sub directories')
    arguments = parser.parse_args()

    host = arguments.host
    file_path = arguments.wordlist

    file = open(file_path, "r")
    
    for line in file.readlines():
        attemptConnection(host, line.strip('\n'))

    file.close()

    file = open(file_path, "r")

    while(len(matches) >= 1):
    
        for subdir in matches:
            
            for line in file.readlines():
                newline = subdir + "/" + line
                attemptConnection(host, newline)
            
            matches.remove(subdir)


if __name__ == '__main__':
    main()