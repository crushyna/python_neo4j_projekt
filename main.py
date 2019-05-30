from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "AllsoP123098"))

ans=True
while ans:
    print("""
    1.Add a Student
    2.Delete a Student
    3.Look Up Student Record
    4.Exit/Quit
    """)
    ans=input("What would you like to do? ")
    if ans=="1":
      print("\nStudent Added")
    elif ans=="2":
      print("\n Student Deleted")
    elif ans=="3":
      print("\n Student Record Found")
    elif ans=="4":
      print("\n Goodbye") 
      ans = None
    else:
       print("\n Not Valid Choice Try again")


def print_friends_of(tx, name):
    for record in tx.run("MATCH (a:Person)-[:KNOWS]->(f) "
                         "WHERE a.name = {name} "
                         "RETURN f.name", name=name):
                         print(record["f.name"])

def return_selected_manufacturer(tx, nazwa):
    for record in tx.run("MATCH (a:Producent) "
                         "RETURN a.nazwa", nazwa=nazwa):
                         print(record["a.nazwa"])

def return_all_manufacturers (tx, nazwa):
    for record in tx.run("MATCH (a:Producent) "
                         "RETURN a.nazwa", nazwa=nazwa):
                         print(record["a.nazwa"])


#with driver.session() as session:
 #   session.read_transaction(return_selected_manufacturer, "Volkswagen")

with driver.session() as session:
    result = session.run("MATCH (n:Producent) RETURN n")
    session.read_transaction(return_selected_manufacturer, "Volkswagen")
    driver.close()