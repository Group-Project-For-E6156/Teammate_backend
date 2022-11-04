import pymysql

import os

###Define default LIMIT and OFFSET
LIMIT = 50
OFFSET = 0

class TeamResource:
    @classmethod
    def __int__(self):
        pass

    @staticmethod
    def _get_connection():

        usr = "root"
        pw = ""
        h = "localhost"

        conn = pymysql.connect(
            user=usr,
            password=pw,
            host=h,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def browse_all_team(course_id):
        if not (course_id):
            return False, "Please fill in all blanks!"
        sql = "SELECT * From teammate_db.Team WHERE Course_id = %s"
        conn = TeamResource._get_connection()
        cur = conn.cursor()
        cur.execute(sql, args=(course_id))
        records = cur.fetchall()
        return records

    @staticmethod
    def browse_team_info_by_input(course_id, team_id):
        if not (course_id and team_id):
            return False, "Please fill in all blanks!"
        sql = "SELECT * From teammate_db.Team WHERE Course_id = %s and Team_id = %s"
        conn = TeamResource._get_connection()
        cur = conn.cursor()
        cur.execute(sql, args=(course_id, team_id))
        records = cur.fetchall()
        return records

    @staticmethod
    def add_team(team_name, team_captain_uni, team_captain, course_id, number_needed=0, team_message=""):
        if not (team_name and course_id and team_captain_uni and team_captain):
            return False, "Please fill in all blanks!"
        team_name = team_name.strip()
        conn = TeamResource._get_connection()
        cur = conn.cursor()
        sql1 = """
                SELECT * From teammate_db.Team 
                WHERE Team_Captain_Uni = %s and Course_id = %s
                """
        cur.execute(sql1, args=(team_captain_uni, course_id))
        records = cur.fetchall()
        if len(records) >= 1:
            return False, "DUPLICATED TEAM"

        sql2 = """
                 insert into teammate_db.Team (Team_Name, Team_Captain_Uni, Team_Captain, Course_id, Number_needed, Team_message)
                 values (%s, %s, %s, %s, %s, %s);
                """
        cur.execute(sql2, args=(team_name, team_captain_uni, team_captain, course_id, number_needed, team_message))
        result = cur.rowcount
        return True if result == 1 else False

    @staticmethod
    def edit_team(team_name, team_captain_uni, team_captain, course_id, number_needed=0, team_message=""):
        if not (team_captain_uni and course_id):
            return False
        conn = TeamResource._get_connection()
        team_name, team_captain, course_id = team_name.strip(), team_captain.strip(), course_id.strip()
        cur = conn.cursor()
        sql1 = """
            SELECT * FROM teammate_db.Team where team_captain_uni = %s and course_id = %s
            """
        res = cur.execute(sql1, args=(team_captain_uni, course_id))
        records = cur.fetchall()
        if len(records) < 1:
            return False
        sql2 = """
            UPDATE teammate_db.Team 
            set team_captain = %s, number_needed = %s, team_message = %s, team_name = %s
            where team_captain_uni = %s and course_id = %s
            """;
        cur.execute(sql2, args=(team_captain, number_needed, team_message, team_name, team_captain_uni, course_id))
        return True

    @staticmethod
    def delete_team(team_captain_uni, course_id, team_id):
        if not (course_id and team_captain_uni and team_id):
            return False
        sql1 = """
        SELECT * FROM teammate_db.Team where Team_Captain_Uni = %s and Course_id = %s
        """
        conn = TeamResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql1, args=(team_captain_uni, course_id))
        records = cur.fetchall()
        if len(records) < 1:
            return False
        sql2 = "DELETE FROM teammate_db.Team where Team_Captain_Uni = %s and Course_id = %s";
        cur.execute(sql2, args=(team_captain_uni, course_id))
        sql3 = """
            DELETE FROM teammate_db.StudentsInTeam 
                    where Team_id = %s
                """;
        cur.execute(sql3, args=team_id)
        return True

    @staticmethod
    def get_all_team_member(team_id, course_id):
        sql = "SELECT * FROM teammate_db.StudentsInTeam where Team_id = %s and Course_id = %s";
        conn = TeamResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=(team_id, course_id))
        result = cur.fetchall()
        return result

    @staticmethod
    def add_team_member(uni, team_id, course_id):
        if not (uni and team_id and course_id):
            return False, "Please fill in all blanks!"
        uni = uni.strip()
        conn = TeamResource._get_connection()
        cur = conn.cursor()
        sql1 = """
                SELECT * From teammate_db.StudentsInTeam 
                WHERE Uni = %s and Team_id = %s and Course_id = %s 
                """
        cur.execute(sql1, args=(uni, team_id, course_id))
        records = cur.fetchall()
        if len(records) >= 1:
            return False, "DUPLICATED MEMBER"
        sql2 = """
                 insert into teammate_db.StudentsInTeam  (Uni, Team_id, Course_id)
                 values (%s, %s, %s);
                """
        cur.execute(sql2, args=(uni, team_id, course_id))
        result = cur.rowcount
        return True if result == 1 else False

    @staticmethod
    def delete_team_member(uni, team_id, course_id):
        if not (course_id and team_id and uni):
            return False
        sql1 = """
        SELECT * From teammate_db.StudentsInTeam WHERE Uni = %s and Team_id = %s and Course_id = %s
        """
        conn = TeamResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql1, args=(uni, team_id, course_id))
        records = cur.fetchall()
        if len(records) < 1:
            return False
        sql2 = "DELETE FROM teammate_db.StudentsInTeam WHERE Uni = %s and Team_id = %s and Course_id = %s";
        cur.execute(sql2, args=(uni, team_id, course_id))
        return True