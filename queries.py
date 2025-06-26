import psycopg2
import psycopg2.extras

from config import (
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    EVENT_ID_DATASET,
    ID_COMMUNE,
)


def connect():
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return conn, cursor


def filter_by_column(sql, column, filter, parameters={}):
    sql += f" AND {column} = %({column})s "
    parameters[column] = filter
    return sql, parameters


def get_total_obs(column=None, filter=None):
    conn, cursor = connect()

    sql = """
        SELECT count(*) 
        FROM gn_synthese.synthese
        JOIN taxonomie.taxref USING(cd_nom)
        WHERE id_dataset = %(event_id_dataset)s
    """
    parameters = {"event_id_dataset": EVENT_ID_DATASET}
    if column and filter:
        sql, parameters = filter_by_column(sql, column, filter, parameters)
    cursor.execute(sql, parameters)
    data = cursor.fetchone()

    cursor.close()
    conn.close()

    return data[0]


def get_new_species():

    conn, cursor = connect()

    sql = """
    select distinct cd_ref, lb_nom, group2_inpn, regne, ordre, famille
    from gn_synthese.synthese s 
    join taxonomie.taxref using(cd_nom)
    where id_dataset=%(id_explore)s
    except
    select distinct cd_ref, lb_nom, group2_inpn, regne, ordre, famille
    from gn_synthese.synthese s 
    join taxonomie.taxref using(cd_nom)
    where id_dataset!=%(id_explore)s
    order by lb_nom ASC
    """
    cursor.execute(sql, {"id_explore": EVENT_ID_DATASET})
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return [dict(d) for d in data]


def get_new_species_commune():

    conn, cursor = connect()

    sql = """
    select distinct cd_ref, lb_nom, group2_inpn, regne, ordre, famille
    from gn_synthese.synthese s 
    join taxonomie.taxref using(cd_nom)
    where id_dataset=%(id_explore)s
    except
    select distinct cd_ref, lb_nom, group2_inpn, regne, ordre, famille
    from gn_synthese.synthese s 
    join taxonomie.taxref using(cd_nom)
    where  id_dataset!=%(id_explore)s AND EXISTS (
        SELECT id_synthese
        FROM gn_synthese.cor_area_synthese cor
        WHERE id_area = %(id_commune)s and cor.id_synthese = s.id_synthese
    )
    order by lb_nom ASC
    """
    cursor.execute(sql, {"id_explore": EVENT_ID_DATASET, "id_commune": ID_COMMUNE})
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return [dict(d) for d in data]


def get_all_data_geo():
    conn, cursor = connect()

    sql = """
        SELECT st_x(the_geom_point) as longitude,
        st_y(the_geom_point) as latitude,
        1 as nb
        FROM gn_synthese.synthese WHERE id_dataset = %s
        LIMIT 5000
    """
    cursor.execute(sql, (EVENT_ID_DATASET,))
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return [dict(d) for d in data]


def get_species_in_event(column=None, filter=None):
    conn, cursor = connect()
    sql = """
        select lb_nom, cd_ref, group2_inpn, regne, ordre, famille, count(s.*) as nb_obs
        from gn_synthese.synthese s 
        join taxonomie.taxref using(cd_nom)
        where id_dataset=%(id_explore)s
    """
    end_sql = """
        GROUP BY lb_nom, cd_ref, group2_inpn, regne, ordre, famille
        order by nb_obs DESC
    """
    parameters = {"id_explore": EVENT_ID_DATASET}
    if filter:
        sql, parameters = filter_by_column(sql, column, filter, parameters)
    sql += end_sql

    cursor.execute(sql, parameters)
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return [dict(d) for d in data]


def get_group2_inpn():
    conn, cursor = connect()

    sql = """
        SELECT distinct group2_inpn
        FROM taxonomie.taxref
        JOIN gn_synthese.synthese USING(cd_nom)
        where id_dataset=%(id_explore)s
        order by group2_inpn ASC
    """
    cursor.execute(sql, {"id_explore": EVENT_ID_DATASET})
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return [d[0] for d in data]


def get_ordres():
    conn, cursor = connect()

    sql = """
        SELECT distinct ordre
        FROM taxonomie.taxref
        JOIN gn_synthese.synthese USING(cd_nom)
        where id_dataset=%(id_explore)s
        order by ordre ASC
    """
    cursor.execute(sql, {"id_explore": EVENT_ID_DATASET})
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return [d[0] for d in data]


def get_familles():
    conn, cursor = connect()

    sql = """
        SELECT distinct famille
        FROM taxonomie.taxref
        JOIN gn_synthese.synthese USING(cd_nom)
        where id_dataset=%(id_explore)s
        order by famille ASC
    """
    cursor.execute(sql, {"id_explore": EVENT_ID_DATASET})
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return [d[0] for d in data]
