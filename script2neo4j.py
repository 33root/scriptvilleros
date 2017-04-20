from neo4j.v1 import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://localhost:7687", auth=("neo4j", "password"))

input_file = "output.txt"


def get_data():
    data = {}
    file = open(input_file, "r")
    c = file.read()
    file.close()

    for line in c.splitlines():
        tmp = {}
        results = line.split("|")
        sha1 = results[1].replace("-", "NA")
        if sha1 != '':
            data[sha1] = tmp
            tmp["SHA1"] = sha1
            tmp["SHA256"] = results[2].replace("-", "NA")
            tmp["MD5"] = results[3].replace("-", "NA")
            tmp["FileName"] = results[4].replace("-", "NA")
            tmp["pdb"] = results[5].replace("-", "NA")
            tmp["CompTime"] = results[6].replace("-", "NA")
            tmp["Size"] = results[7].replace("-", "NA")
            tmp["Description"] = results[8].replace("-", "NA")
        # {<SHA1>: {SHA1: 'SARA', SHA256: 'BBB', MD5: 'LALALA'}}
    return data


def add_family(tx, fam_name):
    tx.run("MERGE (a:Cyber_Actor {name: $name})", name=fam_name)


def add_pdb(tx, key, value, pdb):
    print "key:" + key + " value: " + value + "\n"

    tx.run("MERGE (a:" + key + "{value: $value})"
           "MERGE (b:pdb {pdb: $pdb})"
           "CREATE (a)-[:HAS_PDB]->(b)", value=value, pdb=pdb)


def add_filename(tx, key, value, file):
    tx.run("MERGE (a:" + key + "{value: $value})"
           "MERGE (b:FileName {value: $file})"
           "CREATE (a)-[:NAMED]->(b)", value=value, file=file)


with driver.session() as session:
    session.write_transaction(add_family, "APT28")
    session.write_transaction(add_family, "APT29")
    data = get_data()
    i = 0
    for register in data.items():
        # session.write_transaction(add_pdb, register[1]["PDB"])
        i = i + 1
        for key in register[1]:
            if (register[1]["pdb"] != "NA" and "pdb" != key):
                session.write_transaction(add_pdb, key, register[
                    1][key], register[1]["pdb"])
            if (register[1]["FileName"] != "NA" and "FileName" != key):
                session.write_transaction(add_filename, key, register[
                    1][key], register[1]["FileName"])
