import psycopg2
conn = psycopg2.connect(database = "postgres", 
                        user = "postgres",
                        host= 'localhost',
                        password = "Nurassyl1948",
                        port = 5433)

# Open a cursor to perform database operations
cur = conn.cursor()
# Execute a command: create datacamp_courses table
cur.execute("""CREATE TABLE nurasyl(id int, names varchar(30));""")
# Make the changes to the database persistent
conn.commit()
# Close cursor and communication with the database
cur.close()
conn.close()