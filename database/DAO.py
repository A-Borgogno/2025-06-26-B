from database.DB_connect import DBConnect
from model.circuit import Circuit
from model.driverScore import DriverScore


class DAO():
    @staticmethod
    def getYears():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT DISTINCT `year` 
                    from races r 
                    order by `year` desc"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row['year'])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllCircuits():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT circuitId, circuitRef, name, location, country, lat, lng 
                    from circuits"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Circuit(row['circuitId'],
                               row['circuitRef'],
                               row['name'],
                               row['location'],
                               row['country'],
                               row['lat'],
                               row['lng'], {}))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getResultsCircuitYear(circuitID, year):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select rID.raceId, rID.year, rID.circuitId, rID.name, rID.date, res.driverId, res.position, res.points, res.time
                    from (select *
                    from races r 
                    where r.year= %s
                    and r.circuitId = %s) rID, results res
                    where rID.raceId = res.raceId """

        cursor.execute(query, (year, circuitID))

        res = []
        for row in cursor:
            res.append(DriverScore(row["driverId"], row["time"]))

        cursor.close()
        cnx.close()
        return res

