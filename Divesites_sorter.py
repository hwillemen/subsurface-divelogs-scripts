#!/usr/bin/python

import sys, os
import xml.etree.ElementTree as ET

def print_xmltree(root):
    xmlstr = ET.tostring(root, encoding="utf-8", method="xml")
    print(xmlstr.decode("utf-8"))


### https://docs.python.org/3/library/xml.etree.elementtree.html
### modes: 'xml_compact': moves childs to attributes, 
###        'xml_extend': only adds childs as attributes,
###        'csv': like 'xml_compact' but as a flat csv.
def convert_divesites(xml_in_path, mode='xml_compact'):
    split_ext = os.path.splitext(xml_in_path)
    if mode == 'csv':
        out_file = split_ext[0] + "_sorted.csv"
    else:
        out_file = split_ext[0] + "_sorted" + split_ext[1]
    print("in:", xml_in_path, " out:", out_file, " mode:", mode)
    
    tree = ET.parse(xml_in_path)
    root = tree.getroot()
    root = sort_divesites(root, mode = mode)
    #print_xmltree(root)
    
    if mode != 'csv':
        tree.write(out_file)
    else:
        divesites2csv(root, out_file)
    

def divesites2csv(root, csv_path): ### should have been parsed by sort_divesites()
    attributes = ['uuid', 'name', 'description', 'gps', 'country', 'state', 'town', 'notes']
    
    csvfile = open(csv_path, 'w')
    
    ### Column headers
    line = '"{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}"'.format(*attributes)
    csvfile.write(line)

    for parrent in root: ### site
        values = [(parrent.get(attrib) if parrent.get(attrib) != None else '') for attrib in attributes]
        line = '\n"{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}"'.format(*values)
        csvfile.write(line)
    csvfile.close()


def sort_divesites(root, mode='xml_compact'):
    ### add the child nodes of a divesite as attribute of the site
    for site in root:
        #print(site.tag, site.attrib)
        note_temp = None
        for prop in site:
            #print("    ", prop.tag, prop.attrib)
            if prop.tag == 'notes':
                note_temp = prop.text 
                ### add to 'site' after geo's 
            elif prop.tag == 'geo':
                match prop.attrib['cat']:
                    case '1':
                        site.attrib['ocean'] = prop.attrib['value']
                    case '2':
                        site.attrib['country'] = prop.attrib['value']
                    case '3':
                        site.attrib['state'] = prop.attrib['value']
                    case '4':
                        site.attrib['county'] = prop.attrib['value']
                    case '5':
                        site.attrib['town'] = prop.attrib['value']
                    case '6':
                        site.attrib['city'] = prop.attrib['value']
                    case _:
                        print("Unknown geo 'cat'", prop.attrib['cat'], " in site:", site.attrib['name'])
            else:
                print("Unknown prop:", prop.tag, "in site:", site.attrib['name'])
        if 'country' not in site.attrib: 
            ### 'country' required for next sorting step
            site.attrib['country'] = 'zzz_None'
        if note_temp != None:
            site.attrib['notes'] = note_temp
    
    ### remove childeren of 'site'
    if mode != 'xml_extend':
        #print(root.findall("./site/*"))
        for parent in root: # 'site'
            for child in parent.findall("*"): # 'geo', 'notes'
                ### using parent.findall() to avoid removal during traversal
                parent.remove(child)
    #print_xmltree(root)
        
    ### sort first by country, then by divesite name
    root[:] = sorted(root, key=lambda child: (child.get('country'),child.get('name')))
    #for site in root:
    #    print(site.attrib['country'].ljust(14, ' '), site.attrib['name'])
    return root


if __name__ == "__main__":
    args = sys.argv[1:]
    pathdir = os.path.dirname(__file__)
    mode = 'csv'
    if len(args) == 0:
        xml_in = pathdir + "/" + "Divesites.xml"
    elif len(args) == 1:
        if (args[0].lower() == '-h') or (args[0].lower() == '--help'):
            print("usage: ", os.path.basename(__file__), " [Divesites.xml path] [mode]")
            print("This script sorts the divesites first by country, then by name.")
            print("If divesites do not have a country (<geo cat='2') set, country will be set to 'zzz_None'")
            print("Arguments:")
            print("path   : input divesites xml path can be absolute or relative.") 
            print("         By default it reads Divesites.xml in te same directory.")
            print("mode   : xml_compact: child nodes like geo and notes will be removed but added as attributes to site.")
            print("         xml_extend: child nodes like geo and notes will be kept and added as attributes to site.")
            print("         csv: like 'xml_compact' but as a flat csv.") 
            print("         default:", mode) 
            wait = input("Press Enter to Exit.")
            exit()
        else:
            xml_in = pathdir + "/" + args[0]
    else:
        xml_in = xml_in = pathdir + "/" + args[0]
        mode = args[1]
   
    convert_divesites(xml_in, mode)  
    wait = input("Press Enter to Exit.")