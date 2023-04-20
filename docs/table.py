import os
import pandas as pd


# get json of each file for:
# file name
# author
# org location
# directory name
# link
# client or server file
# tags (use subdir for now)

metadata = []

for root, dirs, files in os.walk(r"C:\Users\Justi\Documents\GitHub\blandlibs\libs", topdown=False):
    # for name in dirs:
    #     if "test" in root:
    #         print("skipping", os.path.join(root, name))
    #         continue
    # # print(os.path.join(root, name))

    for name in files:

        if "test" in root:
            # print("skipping", os.path.join(root, name))
            continue
        if ".krnk" not in name:
            continue
        if "_h.krnk" in name:
            print("skipping", os.path.join(root, name))
            continue
        else:
            newdict = dict(
                script_name="",
                author="",
                link="",
                client="",
                server="",
                other="",
                description="",
                tags=[]
            )
            if ("_c." in name) or (("_client.") in name):
                newdict["client"] = "yes"
            elif ("_s." in name) or (("_server.") in name):
                newdict["server"] = "yes"
            else: 
                newdict["other"] = "yes"
            
            newdict["script_name"] = name.replace("_client.","").replace("_server.","").replace("_c.","").replace("_s.","").replace(".krnk","").replace("krnk","").lower()
            fullpath = os.path.join(root, name)
            with open(fullpath, 'r') as infile:
                for line in infile:
                    if line.startswith("# Author:"):
                        newdict['author'] = line.replace("# Author:","").strip()
                    elif line.startswith("# Description:"):
                        newdict['description'] = line.replace("# Description:","").strip()
                    elif line.startswith("# Link:"):
                        newdict['link'] = line.replace("# Link:","").strip()
                    elif line.startswith("# Discord:"):
                        newdict['link'] = line.replace("# Discord:","").strip()
            newdict["tags"] = root[root.find("blandlibs\\libs\\")+len("blandlibs\\libs\\"):].replace("/","\\").split("\\")
            newdict["category"] = newdict["tags"][0]
            newdict['path'] = r"https://github.com/blandrice/blandlibs/tree/master/libs/" + root[root.find("blandlibs\\libs\\")+len("blandlibs\\libs\\"):].replace("\\","/")
            print(newdict)
            metadata.append(newdict)

        # print(fullpath)
        # print(os.path.join(root, name))
df = pd.DataFrame(metadata)


df.to_csv("table.csv")