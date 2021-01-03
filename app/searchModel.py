from app import app, mysql

class Search():
    @classmethod
    def filter_query_by_price_and_place(cls):
        query = """ SELECT units.unitID, 
        feedbacks.starRating, 
        units.unitType,
        rentalbusiness.rbName, 
        units.rate, 
        locations.longitude 
        FROM rentalbusiness 
        INNER JOIN units ON rentalbusiness.RBID = units.RBID
        INNER JOIN feedbacks ON rentalbusiness.RBID = feedbacks.RBID
        INNER JOIN locations ON units.unitID = locations.unitID
        WHERE locations.City = 'Iligan' AND units.rate > 190 AND units.rate < 1800 """
        cur = mysql.connection.cursor()
        cur.execute(query)
        row_headers=[x[0] for x in cur.description] #this will extract row headers
        res = cur.fetchall()
        search_data=[]
        for result in res:
            search_data.append(dict(zip(row_headers,result)))
            
        return search_data       

    @classmethod
    def get_facilities(cls):
        query = """ SELECT facility FROM facilities """
        cur = mysql.connection.cursor()
        cur.execute(query)
        res = cur.fetchall()
        search_data=[]
        for result in res:
            if result not in search_data:
                search_data.append(result)
        return search_data
        

    @classmethod
    def get_amenities(cls):
        query = """ SELECT service FROM services """
        
        cur = mysql.connection.cursor()
        cur.execute(query)
        res = cur.fetchall()
        search_data=[]
        for result in res:
            if result not in search_data:
                search_data.append(result)
        return search_data


    @classmethod
    def filter_query_by_place(cls, place):

        query = """ SELECT units.unitID, 
        feedbacks.starRating, 
        units.unitType,
        rentalbusiness.rbName, 
        units.rate, 
        locations.longitude 
        FROM rentalbusiness 
        INNER JOIN units ON rentalbusiness.RBID = units.RBID
        INNER JOIN feedbacks ON rentalbusiness.RBID = feedbacks.RBID
        INNER JOIN locations ON units.unitID = locations.unitID
        WHERE locations.City = ? """
        cur = mysql.connection.cursor()
        cur.execute(query,(place,))
        row_headers=[x[0] for x in cur.description] #this will extract row headers
        res = cur.fetchall()
        search_data=[]
        for result in res:
            search_data.append(dict(zip(row_headers,result)))
            
        return search_data

    @classmethod
    def selected_search(cls, id):
        if id:
            query = """SELECT units.unitID, 
            rentalbusiness.rbName, 
            units.unitType,
            units.rate, 
            locations.City,
            locations.latitude,
            locations.longitude,
            rentalbusinessphonenumber.phoneNumber,
            services.service,
            facilities.facility,
            feedbacks.feedback,
            feedbacks.feedbackDate,
            feedbacks.starRating,
            protocols.protocol


            FROM rentalbusiness 
            INNER JOIN units ON rentalbusiness.RBID = units.RBID
            INNER JOIN feedbacks ON rentalbusiness.RBID = feedbacks.RBID
            INNER JOIN locations ON units.unitID = locations.unitID
            INNER JOIN services ON rentalbusiness.RBID = services.RBID
            INNER JOIN protocols ON rentalbusiness.RBID = protocols.RBID
            INNER JOIN rentalbusinessphonenumber ON rentalbusiness.RBID = rentalbusinessphonenumber.RBID
            INNER JOIN facilities ON units.unitID = facilities.unitID 
            WHERE units.unitID = '1' AND rentalbusiness.RBID = '1' """

            #WHERE units.unitID = '1' AND rentalbusiness.RBID = '1' 
            cur = mysql.connection.cursor()
            cur.execute(query)
            row_headers=[x[0] for x in cur.description]
            res = cur.fetchall()
            search_data=[]
            for result in res:
                search_data.append(dict(zip(row_headers,result)))
                
            return search_data

        else:
            return {'error': 'No results'}
        


