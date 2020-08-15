class DB:

    from os import environ
    password : str = environ['MONGODB']

    from pymongo import MongoClient
    client : MongoClient = MongoClient("mongodb+srv://nishant:{}@firstcluster-b8uyp.gcp.mongodb.net/test?retryWrites=true&w=majority".format(password))

    # Only working with the Orders database
    orders = client['Orders']

    from Order import Order
    @staticmethod
    def add(order : Order):

        from typing import List, Dict
        memberCosts : Dict[str, float] = {member.getName() : member.getTotal() for member in order.getMembers()}

        # Need to specify session because atomicity is necessary
        # Multiple document operations aren't atomic by default
        with DB.client.start_session() as session:
            # Add order to transactions collection
            transactions = DB.orders['Transactions']
            transactions.insert_one({
                'Date' : order.getDate(),
                'Location' : order.getLocation(),
                'Total' : order.getTotal(),
                'Members' : memberCosts
                }, session = session)

            # Update balances in Members collection
            members = DB.orders['Members']

            # No need to track how much my balance is
            memberCosts.pop('Nishant')
            for member_name in memberCosts:
                members.update_one(
                    {'Name' : member_name},
                    {'$inc' : {'Balance' : memberCosts[member_name]}},
                    upsert = True,
                    session = session
                )

            locations = DB.orders['Locations']

            # Retrieves Yelp URL, categories business is relevant to, and coordinates
            from Yelp import Yelp
            location_details : Dict = Yelp.search(order.getLocation())

            # Inserts new location if it does not exist in database, if exists the no change
            locations.update_one(
                {'Name' : location_details['Name']},
                {'$setOnInsert' : location_details},
                upsert = True
            )

            # Names of members in this order
            memberNames : List[str] = list(memberCosts.keys())

            # Returns list of dictionaries of members with excessive balances
            return list(members.find({'$and': [{'Name': {'$in': memberNames}}, {'Balance': {'$gt': 100}}]}))

    # Don't need to specify session because single document operations are atomic
    @staticmethod
    def credit(name : str, value : float) -> float:
        from pymongo import ReturnDocument
        members = DB.orders['Members']
        new_balance : float = members.update_one(
            {'Name' : name},
            {'$inc' : {'Balance' : -value}},
            projection = {'Balance' : 1, '_id' : 0},
            upsert = True, return_document = ReturnDocument.AFTER
        )['Balance']
        return new_balance