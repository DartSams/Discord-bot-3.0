import os
from pymongo import MongoClient


db_str = "mongodb+srv://DartSams:Dartagnan_19@personal-cluser-db.qavgfkq.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(db_str)
mydb = client["Personal_db"] #connects to db but if not found will create it 

class DiscordTable:
    def __init__(self):
        self.table = None
        self.admins = []

    def create_db(self,table_name):
        main_table = mydb[table_name]
        self.table = main_table
        return main_table

    def insert_user(self,name,discord_id,money=1000,privilege="user"):
        data = {
            "name":name,
            "discriminator":discord_id,
            "money":money,
            "privilege":privilege   
        }
        self.table.insert_one(data) #inserts into db

    def show_entries(self):
        self.discord_users = []
        for user in self.table.find({},{"_id":0}):
            # print(user)
            self.discord_users.append(user)
        
        return self.discord_users

    def delete_user(self,name,discord_id):
        myquery = {
            "name": name,
            "discriminator":discord_id
        }

        self.table.delete_one(myquery)

    def mass_destry(self):
        self.table.delete_many({})

    def create_admin(self,discord_id):
        old_data = {
            "discriminator":discord_id
        }

        new_data = {
            "$set":{
                "privilege":"admin"
            }
        } # the keyword <$set> is needed to represent that its going to updata the column
        self.table.update_one(old_data,new_data) #takes 2 parameters the 1st finds the entry in db collection then replaces it with the 2nd paramater


# z = DiscordTable()
# z.create_db("Discord_DB")

# z.mass_destry()


class Reminder:
    def __init__(self):
        self.table = None
        self.admins = []

    def create_db(self,table_name:str):
        main_table = mydb[table_name]
        self.table = main_table
        return main_table

    def create_reminder(self,author:str,name:str,task:str,due_date:str):
        data = {
            "name":name,
            "task":task,
            "due_date":due_date,
            "made_by":author
        }

        self.table.insert_one(data)

    def delete_reminder(self,name):
        myquery = {
            "name": name,
        }

        self.table.delete_one(myquery)


r = Reminder()
r.create_db("Reminder")
# r.create_reminder("calculus","make 5 page notes","Dec 5 2022")