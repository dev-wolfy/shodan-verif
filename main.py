#!/usr/bin/env python3.8

from shodan import Shodan
import argparse
import logging
import json
import time
import re


def valid_API_Key(arg_values):
    """ to valid argument value for metadata
    """

    regex = "^([A-Za-z0-9]{32})$"
    if not re.match(regex, arg_values):
        msg = "The api key is invalid"
        raise argparse.ArgumentTypeError(msg)
    else:
        return arg_values


def loadKeyFromFile(filename):

    try:
        fichier = open(filename, "r")
        lines = fichier.readlines()
        fichier.close()
    except:
        print(f"fichier {filename} non trouvé...")
        quit()

    for line in lines:
        if valid_API_Key(line.strip()):
            return line.strip()

    quit()


def parse_args():
    """function to parse arguments from the CLI
    """

    epilog = """
    Exemples:
    
        blablabla
    
      Enjoy!
    """

    parser = argparse.ArgumentParser(epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-l", "--loglevel", type=str, help="The log level for the program",
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="DISABLE")
    
    subparser = parser.add_subparsers(dest='command')

    search = subparser.add_parser('search')
    search.description = "search for servers on shodan"

    search.add_argument("-k", "--api-key", type=valid_API_Key, required=False, help="api key for shodan")
    search.add_argument("-q", "--query", type=str, required=True, help="query for shodan search")
    search.add_argument("-i", "--ip", type=str, required=False, help="Test if the ip is find in the result", nargs="*")
    search.add_argument("-d", "--dns", type=str, required=False, help="dns name to find in result", nargs="*")

    count = subparser.add_parser('count')
    count.description = "count servers on shodan"

    count.add_argument("-k", "--api-key", type=valid_API_Key, required=False, help="api key for shodan")
    count.add_argument("-q", "--query", type=str, required=True, help="query for shodan search")
    count.add_argument("-n", "--number", type=int, required=True, help="teorical number of result")

    
    key = subparser.add_parser('api-key')

    key.add_argument("-k", "--key-value", type=valid_API_Key, required=False, help="the api key for shodan")

    key.add_argument("-d", "--delete", required=False, action="store_true")
    key.add_argument("-c", "--confirm", required=False, action="store_true")


    return parser.parse_args()


        
def search(api_key, query, ip, dns):

    if not ip and not dns:
        quit()

    try:
        api = Shodan(api_key)
    except Exception as e:
        print(e)
        quit()

    try:
        results = api.search(query)
    except Exception as e:
        print(e)
        quit()
    
    filename = "shodan" + time.strftime("%Y%m%d-%H%M%S") + ".json"

    fichier = open(filename, "w")
    fichier.write(json.dumps(results))
    fichier.close()

    to_return = []

    j = 1
    for matche in results['matches']:

        for dn in dns:
            if dn in matche['domains']:
                to_return.append(dn)
        for i in ip:
            if i == matche['ip_str']:
                to_return.append(i)

        j += 1

    found = ','.join(to_return)

    j = str(j)
    print(f"In {j} element I found following element : {found}")

    return to_return

    
def count(api_key, query, number):
    try:
        api = Shodan(api_key)
    except Exception as e:
        print(e)
        quit()

    try:
        results = api.count(query)
    except Exception as e:
        print(e)
        quit()

    find = int(results['total'])
    number = int(number)

    if find == number:
        print(f"Pas de nouvelle entrée dans Shodan, {number} serveurs trouvé")
    else:
        print(f"Nouvelle entrée dans shodan détecté. {number} espected and {find} found")
    
    
def key(key, delete=False, confirm=False):

    if confirm == False and delete:

        choice = ""
        while choice != "y" and choice != "n":
            choice = input("(y)es or (n)o : ")
        if choice == "y":
            confirm = True
        else:
            print("Not okay, no key deleted...")
            quit(0)

    if delete:
        if confirm:
            fichier = open("api-key.txt", "w")
            fichier.write("")
            fichier.close()
            print("Key file deleted")

    if key:
        fichier = open("api-key.txt", "w")
        fichier.write(key)
        fichier.close()
        print("Key added successfully")

    return 0


def main():
    """main function
    """
    
    # ARGPARSE
    args = parse_args()
    print(args)


    # LOGGING
    disable_logging = False
    
    if args.loglevel == "DEBUG":
        p_level = logging.DEBUG
    elif args.loglevel == "INFO":
        p_level = logging.INFO
    elif args.loglevel == "WARNING":
        p_level = logging.WARNING
    elif args.loglevel == "ERROR":
        p_level = logging.ERROR
    elif args.loglevel == "CRITICAL":
        p_level = logging.CRITICAL
    elif args.loglevel == "DISABLE":
        p_level = logging.CRITICAL
        disable_logging = True
    else:
        p_level = logging.WARNING

    logging.basicConfig(level=p_level, format='%(asctime)s - %(levelname)s - %(message)s')
    if disable_logging:
        logging.disable(level=logging.CRITICAL)


    # ACTION
    if args.command == "search":

        print("search !")
        
        api_key = loadKeyFromFile("api-key.txt") if args.api_key == None else args.api_key
        query = args.query
        ip = args.ip
        dns = args.dns

        search(api_key, query, ip, dns)

    elif args.command == "count":

        print("count !")

        api_key = loadKeyFromFile("api-key.txt") if args.api_key == None else args.api_key
        query  = args.query
        number = args.number

        count(api_key, query, number)

    elif args.command == "api-key":
        key(args.key_value, args.delete, args.confirm)
    else:
        print("nothing to do.")


if __name__ == "__main__":
    """Entrypoint of the script
    """

    main()


class Class():
    """Class template
    """

    def __init__(self):
        pass

    def function(self):
        pass
