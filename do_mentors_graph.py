import urllib.request
import json
import array
import os

start_user = 229127
depth = 3

def get_mentors(uid):
    with urllib.request.urlopen("https://www.drupal.org/api-d7/user.json?uid=" + str(uid)) as url:
        user = json.loads(url.read().decode())

    mentors = array.array('i', [])
    for mentor in user["list"][0]["field_mentors"]:
        mentors.append(int(mentor["id"]));
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
    
filename = "do_mentors_graph_" + get_name(start_user) + "_depth_" + str(depth)

f = open(filename + ".dot", "w")
f.write("digraph G {\n")
processed = array.array('i', [])
process_mentors(start_user, depth, processed)
f.write("}\n")
f.close()

os.system("dot -Tpng " + filename + ".dot > " + filename + ".png")
