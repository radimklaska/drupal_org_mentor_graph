import urllib.request
import json
import array
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--user", "-u", help="Set the Drupal.org user ID to start from", type=int)
parser.add_argument("--depth", "-d", help="How deep to go down the rabbit hole", type=int)
args = parser.parse_args()

if args.user:
    print("Using Drupal.org ID #%s" % args.user)
else:
    print("Please supply a --user argument")
    exit(1)

if args.depth:
    print("Using depth of %s" % args.depth)
else:
    args.depth = 3
    print("Using default depth of %s" % args.depth)

def get_mentors(uid):
    with urllib.request.urlopen("https://www.drupal.org/api-d7/user.json?uid=" + str(uid)) as url:
        user = json.loads(url.read().decode())

    mentors = array.array('i', [])
    for mentor in user["list"][0]["field_mentors"]:
        mentors.append(int(mentor["id"]))
    return mentors

def get_name(uid):
    with urllib.request.urlopen("https://www.drupal.org/api-d7/user.json?uid=" + str(uid)) as url:
        user = json.loads(url.read().decode())
    return str(uid) + "_" + strip_name(user["list"][0]["name"])

def strip_name(name):
    return ''.join(filter(str.isalpha, name))

def process_mentors(uid, depth, processed):
    if depth == 0:
        return
    if uid in processed:
        return
    current = get_name(uid)
    processed.append(int(uid))
    print("Processing: " + current + ", Depth: " + str(depth))
    for mentor in get_mentors(uid):
        mentor_name = get_name(mentor)
        print("	" + mentor_name)
        f.write("	\"" + current + "\" -> \"" + mentor_name + "\";\n")
        process_mentors(mentor, depth - 1, processed)
    
filename = "do_mentors_graph_" + get_name(args.user) + "_depth_" + str(args.depth)

f = open(filename + ".dot", "w")
f.write("digraph G {\n")
processed = array.array('i', [])
process_mentors(args.user, args.depth, processed)
f.write("}\n")
f.close()

os.system("dot -Tpng " + filename + ".dot > " + filename + ".png")
