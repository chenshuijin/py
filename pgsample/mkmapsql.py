#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'chenshuijin'
# select updategeometrysrid('public', 'ko_4_tmp','way',0);
# SELECT ST_SRID(boundary_bd) FROM regions;
# SELECT osm_id, "name:en" name_en, "name:zh" name_zh, way INTO ko_4_tmp FROM ko_polygon WHERE admin_level='4' AND boundary = 'administrative';
# DELETE FROM ko_4_tmp;
# SELECT osm_id, "name:en" name_en, "name:zh" name_zh, way INTO ko_6_tmp FROM ko_polygon WHERE admin_level='6' AND boundary = 'administrative';
# DELETE FROM ko_6_tmp;
# select name, svals("name:en") from ko_polygon where admin_level = '4';
# -----
# SELECT osm_id, name, svals("name:en"), way INTO ja_2_tmp FROM ja_polygon WHERE boundary = 'administrative' AND admin_level = '2';
# SELECT osm_id, name name_zh, svals("name:en") name_en, ST_UNION(ARRAY(SELECT way FROM ja_polygon WHERE boundary='administrative' AND admin_level='2'))) way INTO ja_2_tmp FROM ja_polygon WHERE boundary = 'administrative' AND admin_level = '2' LIMIT 1;
# SELECT ST_UNION(ARRAY(SELECT way FROM ja_2_tmp WHERE name_en = 'Japan'));
# 
# SELECT osm_id, name, "name:en" name_en, "name:zh" name_zh, "name:ko" name_ko, way INTO ko_4_tmp FROM ko_polygon WHERE admin_level='4' AND boundary = 'administrative';

import psycopg2

insertprovinceregionsql = "INSERT INTO regions(type, name_zh, name_en, center_bd, boundary_db) VALUES('province', '%s', '%s', '%s', '%s');\n"
updateprovinceregionsql = "UPDATE regions SET parent_id = (SELECT id from regions WHERE name_en = '%s' and type = 'country') WHERE name_en = '%s' AND type = 'city';"
insertcityregionsql = "INSERT INTO regions(type, name_zh, name_en, center_bd, boundary_db) VALUES('city', '%s', '%s', '%s', '%s');\n"
updatecityregionsql = "UPDATE regions SET parent_id = (SELECT id from regions WHERE name_en = '%s' and type = 'province') WHERE name_en = '%s' AND type = 'city';"
sqlKoAdminLevel4="SELECT osm_id, \"name:en\" name_en, \"name:zh\" name_zh, way FROM ko_polygon WHERE boundary = 'administrative' AND admin_level = '4';"
sqlKoAdminLevel6="SELECT osm_id, \"name:en\" name_en, \"name:zh\" name_zh, way FROM ko_polygon WHERE boundary = 'administrative' AND admin_level = '6';"
sqlStUnion = "SELECT ST_UNION(ARRAY(SELECT way FROM %s WHERE osm_id = %d));"
sqlStCentroid = "SELECT ST_CENTROID('%s');"

targetinsertsql = "INSERT INTO regions(name_zh, name_en, type, center_bd, boundary_bd) VALUES('%s', '%s', '%s', '%s', '%s');"
targetupdatepidsql = "UPDATE regions SET parent_id = (SELECT id FROM regions WHERE name_en = '%s' and type = '%s') WHERE name_en = '%s' AND type='%s';"
targetsqlcountry = "INSERT INTO regions(name_zh, name_en, type, center_bd, boundary_bd) VALUES('%s', '%s', 'country', '%s', '%s');"

def formatupdatepidsql(pname_en, ptype, name_en, mtype):
    return targetupdatepidsql % (pname_en, ptype, name_en, mtype)

def formatinsertsql(name_zh, name_en, mtype, center_bd, boundary_db):
    return targetinsertsql % (name_zh, name_en, mtype, center_bd, boundary_db)

def execsql(sql):
    conn = psycopg2.connect(database='gis',user='postgres',host='localhost',port='5432')
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    #for i in rows:
        #print(i[3])
    conn.close()
    return rows;

def st_union(way):
    sql = sqlStCentroid % way
    return execsql(sql)[0][0]

def st_contains(a, b):
    sql = "select st_contains('%s', '%s');" % (a, b)
    return execsql(sql)[0][0]

def st_centroid(way):
    return execsql("select st_centroid('%s');" % way)[0][0]

def getjanpansql():
    japan = execsql("select * from ja_2_tmp;")
    jaid = 0
    
    for v in japan:
        if getLastHstoreValue(v[2]) == 'Japan' :
            jaid = v[0]
            break;

    jaboundary = execsql("select st_union(array(select way boundary from ja_2_tmp where " + "osm_id = " + str(jaid) + "));")[0][0]
    jacenter = execsql("select st_centroid(st_union(array(select way boundary from ja_2_tmp where " + "osm_id = " + str(jaid)  + ")));")[0][0]
    return "INSERT INTO regions(name_zh, name_en, name_ko, name_ja, type, center_bd, boundary_bd) VALUES('%s', '%s', '%s', '%s', 'country', '%s', '%s');" % (japan[0][1], getLastHstoreValue(japan[0][2]), getLastHstoreValue(japan[0][2]), getLastHstoreValue(japan[0][4]), jacenter, jaboundary);

def getjapanprosql():
    japanpros = execsql("select distinct osm_id, name, name_en, name_ja from ja_4_tmp;")
    ret = "";
    for pro in japanpros:
        cbd, bbd = "", ""
        if execsql("select count(*) from ja_4_tmp where osm_id = %d;" % pro[0])[0][0] > 1:
            bbd = execsql("select st_union(array(select way from ja_4_tmp where osm_id = %d));" % pro[0])[0][0]
        else:
            bbd = execsql("select way from ja_4_tmp where osm_id = %d;" % pro[0])[0][0]
        cbd = st_centroid(bbd)
        name_en = getLastHstoreValue(pro[1])
        name_zh = getLastHstoreValue(pro[2])
        name_ko = name_en
        name_ja = getLastHstoreValue(pro[3])
        ret += "INSERT INTO regions(name_zh, name_en, name_ko, name_ja, type, center_bd, boundary_bd) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (name_zh, name_en, name_ko, name_ja, 'province', cbd, bbd) + "\n";
        ret += formatupdatepidsql("Japan", 'country', name_en, 'province') + "\n"

    return ret;

def getjapancities():
    japanpros = execsql("select distinct osm_id, name, name_en, name_ja from ja_4_tmp;")
    ret = "";
    for pro in japanpros:
        cbd, bbd = "", ""
        if execsql("select count(*) from ja_4_tmp where osm_id = %d;" % pro[0])[0][0] > 1:
            bbd = execsql("select st_union(array(select way from ja_4_tmp where osm_id = %d));" % pro[0])[0][0]
        else:
            bbd = execsql("select way from ja_4_tmp where osm_id = %d;" % pro[0])[0][0]
        cbd = st_centroid(bbd)
        name_en = getLastHstoreValue(pro[1])
        name_zh = getLastHstoreValue(pro[2])
        name_ko = name_en
        name_ja = getLastHstoreValue(pro[3])
        ret += "INSERT INTO regions(name_zh, name_en, name_ko, name_ja, type, center_bd, boundary_bd) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (name_zh, name_en, name_ko, name_ja, 'city', cbd, bbd) + "\n";
        ret += formatupdatepidsql(name_en, 'province', name_en, 'city') + "\n"

    return ret;

def getjaregionsql():
    fo = open("ja.sql", "wb")
    fo.write(getjanpansql());
    fo.write(getjapanprosql());
    fo.write(getjapancities());
    fo.close()

def getkoreasql():
    korea = execsql("select distinct osm_id, name, name_en, name_ja, name_zh, oname_zh from ko_2_tmp;")
    name_ko = getLastHstoreValue(korea[0][1])
    name_en = getLastHstoreValue(korea[0][2])
    name_ja = getLastHstoreValue(korea[0][3])
    name_zh = getLastHstoreValue(korea[0][4])
    koboundary = execsql("select st_union(array(select way boundary from ko_2_tmp where osm_id = " + str(korea[0][0]) + "));")[0][0]
    kocenter = execsql("select st_centroid(st_union(array(select way boundary from ko_2_tmp where osm_id = " + str(korea[0][0]) +")));")[0][0]
    return "INSERT INTO regions(name_zh, name_en, name_ko, name_ja, type, center_bd, boundary_bd) VALUES('%s', '%s', '%s', '%s', 'country', '%s', '%s');" % (name_zh, name_en, name_ko, name_ja, kocenter, koboundary)

def getkoprossql():
    kopros = execsql("select distinct osm_id, name, name_en, name_ja, name_zh, oname_zh from ko_4_tmp;")
    ret = ""
    for pro in kopros:
        cbd, bbd = "", ""
        name_ko = getLastHstoreValue(pro[1])
        name_en = getLastHstoreValue(pro[2])
        name_ja = getLastHstoreValue(pro[3])
        name_zh = pro[4]
        if (name_zh == None or name_zh == '') :
            name_zh = getLastHstoreValue(pro[5])
        else : 
            name_zh = getLastHstoreValue(pro[4])
        if execsql("select count(*) from ko_4_tmp where osm_id = %d;" % pro[0])[0][0] > 1:
            bbd = execsql("select st_union(array(select way from ko_4_tmp where osm_id = %d));" % pro[0])[0][0]
        else:
            bbd = execsql("select way from ko_4_tmp where osm_id = %d;" % pro[0])[0][0]
        cbd = st_centroid(bbd)
        ret += "INSERT INTO regions(name_zh, name_en, name_ko, name_ja, type, center_bd, boundary_bd) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (name_zh, name_en, name_ko, name_ja, 'province', cbd, bbd) + "\n";
        ret += formatupdatepidsql("South Korea", 'country', name_en, 'province') + "\n"
    
    return ret

def getkocitiessql():
    kopros = execsql("select distinct osm_id, name, name_en, name_ja, name_zh, oname_zh from ko_4_tmp;")
    ret = ""
    for pro in kopros:
        cbd, bbd = "", ""
        name_ko = getLastHstoreValue(pro[1])
        name_en = getLastHstoreValue(pro[2])
        name_ja = getLastHstoreValue(pro[3])
        name_zh = pro[4]
        if (name_zh == None or name_zh == '') :
            name_zh = getLastHstoreValue(pro[5])
        else : 
            name_zh = getLastHstoreValue(pro[4])
        if execsql("select count(*) from ko_4_tmp where osm_id = %d;" % pro[0])[0][0] > 1:
            bbd = execsql("select st_union(array(select way from ko_4_tmp where osm_id = %d));" % pro[0])[0][0]
        else:
            bbd = execsql("select way from ko_4_tmp where osm_id = %d;" % pro[0])[0][0]
        cbd = st_centroid(bbd)
        ret += "INSERT INTO regions(name_zh, name_en, name_ko, name_ja, type, center_bd, boundary_bd) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (name_zh, name_en, name_ko, name_ja, 'city', cbd, bbd) + "\n";
        ret += formatupdatepidsql(name_en, 'province', name_en, 'city') + "\n"
    
    return ret

def getLastHstoreValue(str):
    return str.split(',')[-1].split('=>')[-1].replace('"','')

def getkoregionsql():
    fo = open("ko.sql", "wb")
    fo.write(getkoreasql())
    fo.write(getkoprossql())
    fo.write(getkocitiessql())
    fo.close()

getkoregionsql()
getjaregionsql()


print 'ok'
