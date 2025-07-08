from database.DB_connect import DBConnect
from model.circuit import Circuit
from model.piazzamento import Piazzamento


class DAO():
    @staticmethod
    def getAllCircuits():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * 
                    from circuits"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Circuit(row["circuitId"], row["circuitRef"], row["name"], row["location"], row["country"],
                               row["lat"], row["lng"], row["alt"], row["url"], {}))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getYears():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT distinct(year) as year 
                        from seasons order by year"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row["year"])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getRisultatiCircuito(circuitId, year1, year2):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select r2.`year`, r2.raceId, r.driverId, r.`time` 
                    from results r, races r2 
                    where r.raceId = r2.raceId 
                    and r2.`year` between %s and %s
                    and r2.circuitId = %s"""
        cursor.execute(query, (year1, year2, circuitId))

        res = []
        for row in cursor:
            res.append((row["year"], Piazzamento(row["raceId"], row["driverId"], row["time"])))

        cursor.close()
        cnx.close()
        return res