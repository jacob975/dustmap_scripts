#!/usr/bin/python
'''
Program:
    This is a program providing the way to use mysql table.
Usage: 
    Add this line in your python program:
    import chiu20_mysql_lib
Editor:
    Jacob975
20200521
#################################
update log
20200521 version alpha 1
    1. The code works.
'''
import mysql.connector as mariadb
import time
import numpy as np
from astropy.io import fits as pyfits
from sys import argv

def chiu_auth():
    # Login mariadb as user 'TAT'@'localhost'
    authority = {   'user':'Jacob975',         
                    'password':'1234',        
                    'database':'chiu20', 
                    'host':'localhost'
                }
    cnx = mariadb.connect(**authority)
    return cnx
#--------------------------------------------------
# Create and Remove tables.
def create_tables():
    #-----------------------------------------
    # Initialization
    cnx = chiu_auth()
    cursor = cnx.cursor()
    #-----------------------------------------
    # Create table `Measure_Quantities_Cloud`, which save the data getting from image. 
    mq_cloud_format_strings = []
    for i in range(len(mq_cloud_format)):
        mq_cloud_format_strings.append(
            mq_cloud_format[i, 0] + mq_cloud_format[i, 1])
    sql = 'create table if not exists `{0}` ({1})'.format(
        mq_cloud_name, 
        ', '.join(mq_cloud_format_strings)
    )
    cursor.execute(sql)
    cnx.commit()
    #-----------------------------------------
    # Create table `WOerr_Cloud`, which save the data without error
    woerr_cloud_format_strings = []
    for i in range(len(woerr_cloud_format)):
        woerr_cloud_format_strings.append(
            woerr_cloud_format[i, 0] + woerr_cloud_format[i, 1])
    sql = 'create table if not exists `{0}` ({1})'.format(
        woerr_cloud_name, 
        ', '.join(woerr_cloud_format_strings)
    )
    cursor.execute(sql)
    cnx.commit()
    #-----------------------------------------
    # Create table `WOerr_Cloud`, which save the data without error
    mq_av_region_format_strings = []
    for i in range(len(mq_av_region_format)):
        mq_av_region_format_strings.append(
            mq_av_region_format[i, 0] + mq_av_region_format[i, 1])
    sql = 'create table if not exists `{0}` ({1})'.format(
        mq_av_region_name, 
        ', '.join(mq_av_region_format_strings)
    )
    cursor.execute(sql)
    cnx.commit()
    #-----------------------------------------
    # Close the database
    cursor.close()
    cnx.close()
    return 

def remove_tables():
    remove_mq_cloud()
    remove_woerr_cloud()
    remove_mq_av_region()
    return 
#--------------------------------------------------

mq_cloud_name = 'Measure_Quantities_Cloud'

mq_cloud_format = np.array([
    ['`index`', ' INT AUTO_INCREMENT PRIMARY KEY'],
    ['`dt`', ' DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'],
    ['`cloud`', ' VARCHAR(100)'],
    ['`l_deg`', 'FLOAT'],
    ['`b_deg`', 'FLOAT'],
    # Number of YSO
    ['`yso_number`', ' INT'],
    ['`class_i_yso_number`', ' INT'],
    ['`class_f_yso_number`', ' INT'],
    # YSO lifetime
    ['`yso_lifetime_Myr`', 'FLOAT'],
    ['`e_yso_lifetime_Myr`', 'FLOAT'],
    ['`class_i_yso_lifetime_Myr`', 'FLOAT'],
    ['`e_class_i_yso_lifetime_Myr`', 'FLOAT'],
    ['`class_f_yso_lifetime_Myr`', 'FLOAT'],
    ['`e_class_f_yso_lifetime_Myr`', 'FLOAT'],
    # YSO mass
    ['`avg_yso_mass_Msun`', 'FLOAT'],
    ['`e_avg_yso_mass_Msun`', 'FLOAT'],
    ['`total_yso_mass_Msun`', 'FLOAT'],
    ['`e_total_yso_mass_Msun`', 'FLOAT'],
    ['`total_class_i_yso_mass_Msun`', 'FLOAT'],
    ['`e_total_class_i_yso_mass_Msun`', 'FLOAT'],
    ['`total_class_f_yso_mass_Msun`', 'FLOAT'],
    ['`e_total_class_f_yso_mass_Msun`', 'FLOAT'],
    # Distance to the cloud
    ['`distance_pc`', ' FLOAT'],
    ['`e_distance_pc`', ' FLOAT'],
    # Surface area of the cloud
    ['`area_deg2`', ' FLOAT'],
    ['`area_pc2`', ' FLOAT'],
    ['`e_area_pc2`', ' FLOAT'],
    ['`yso_number_per_deg2`', ' FLOAT'],
    ['`yso_number_per_pc2`', ' FLOAT'],
    ['`e_yso_number_per_pc2`', ' FLOAT'],
    ['`class_i_yso_number_per_deg2`', ' FLOAT'],
    ['`class_i_yso_number_per_pc2`', ' FLOAT'],
    ['`e_class_i_yso_number_per_pc2`', ' FLOAT'],
    ['`class_f_yso_number_per_deg2`', ' FLOAT'],
    ['`class_f_yso_number_per_pc2`', ' FLOAT'],
    ['`e_class_f_yso_number_per_pc2`', ' FLOAT'],
    ['`Av_threshold`', ' VARCHAR(20)'],
    # Cloud mass derived from extinctions or dust emission.
    ['`cloud_mass_Msun`', ' FLOAT'],
    ['`e_cloud_mass_Msun`', ' FLOAT'],
    ['`cloud_surface_density_Msun_per_pc2`', ' FLOAT'],
    ['`e_cloud_surface_density_Msun_per_pc2`', ' FLOAT'],
    # Star Formation Rate (SFR)
    ['`sfr_Msun_per_Myr`', ' FLOAT'],
    ['`e_sfr_Msun_per_Myr`', ' FLOAT'],
    ['`sfr_I_Msun_per_Myr`', ' FLOAT'],
    ['`e_sfr_I_Msun_per_Myr`', ' FLOAT'],
    ['`sfr_F_Msun_per_Myr`', ' FLOAT'],
    ['`e_sfr_F_Msun_per_Myr`', ' FLOAT'],
    # Star Formation Rate density (All YSO)
    ['`sfr_surface_density_Msun_per_Myr_pc2`', ' FLOAT'],
    ['`e_sfr_surface_density_Msun_per_Myr_pc2`', ' FLOAT'],
    ['`flag_sfr_surface_density_Msun_per_Myr_pc2`', 'VARCHAR(4)'],
    # Star Formation Rate density (Class I only)
    ['`sfr_I_surface_density_Msun_per_Myr_pc2`', ' FLOAT'],
    ['`e_sfr_I_surface_density_Msun_per_Myr_pc2`', ' FLOAT'],
    ['`flag_sfr_I_surface_density_Msun_per_Myr_pc2`', 'VARCHAR(4)'],
    # Star Formation Rate density (Class F only)
    ['`sfr_F_surface_density_Msun_per_Myr_pc2`', ' FLOAT'],
    ['`e_sfr_F_surface_density_Msun_per_Myr_pc2`', ' FLOAT'],
    ['`flag_sfr_F_surface_density_Msun_per_Myr_pc2`', 'VARCHAR(4)'],
    # Depletion time
    ['`cloud_depletion_time_Myr`', ' FLOAT'],
    ['`e_cloud_depletion_time_Myr`', ' FLOAT'],
    ['`cloud_free_fall_time_Myr`', ' FLOAT'],
    ['`e_cloud_free_fall_time_Myr`', ' FLOAT'],
    ['`sfr_per_t_ff`', ' FLOAT'],
    ['`e_sfr_per_t_ff`', ' FLOAT'],
    # Star Formation Efficiency (SFE)
    ['`sfe`', ' FLOAT'],
    ['`e_sfe`', ' FLOAT'],
    # Input files and Assumptions
    ['`input_file`', 'VARCHAR(100)'],
    ['`reference`', 'VARCHAR(100)'],
    ['`comments`', 'VARCHAR(200)'],
])

def save2sql_mq_cloud(data):
    cnx = chiu_auth()
    cursor = cnx.cursor()
    # Creat database if did not exist.
    create_tables()
    # Save data into the table in the database.
    cursor.execute( 
        "insert into {0} ({1}) values ({2})".format(
            mq_cloud_name,  
            ', '.join(mq_cloud_format[2:,0]), 
            ', '.join(['%s'] * len(mq_cloud_format[2:,0]))), 
        tuple(data[2:]))
    cnx.commit()
    cursor.close()
    cnx.close()

def load2py_mq_cloud(col_list):
    # Connect to SQL
    cnx = chiu_auth()
    cursor = cnx.cursor()
    col_list_str = ', '.join(col_list)
    cursor.execute(
        "select {0} from {1}".format(
            col_list_str,
            mq_cloud_name,
        )
    )
    data = cursor.fetchall()
    data = np.array(data, dtype = str)
    # Close the SQL
    cnx.commit()
    cursor.close()
    cnx.close()
    return data

def remove_mq_cloud():
    cnx = chiu_auth()
    cursor = cnx.cursor()
    sql = 'drop table {0}'.format(mq_cloud_name)
    cursor.execute(sql)
    cnx.commit()
    cursor.close()
    cnx.close()
    return 
#--------------------------------------------------

mq_av_region_name = 'Measure_Quantities_Av_Regions'
mq_av_region_format = mq_cloud_format

def save2sql_mq_av_region(data):
    cnx = chiu_auth()
    cursor = cnx.cursor()
    # Creat database if did not exist.
    create_tables()
    # Save data into the table in the database.
    cursor.execute( 
        "insert into {0} ({1}) values ({2})".format(
            mq_av_region_name,  
            ', '.join(mq_av_region_format[2:,0]), 
            ', '.join(['%s'] * len(mq_av_region_format[2:,0]))), 
        tuple(data[2:]))
    cnx.commit()
    cursor.close()
    cnx.close()

def load2py_mq_av_region(col_list):
    # Connect to SQL
    cnx = chiu_auth()
    cursor = cnx.cursor()
    col_list_str = ', '.join(col_list)
    cursor.execute(
        "select {0} from {1}".format(
            col_list_str,
            mq_av_region_name,
        )
    )
    data = cursor.fetchall()
    data = np.array(data, dtype = str)
    # Close the SQL
    cnx.commit()
    cursor.close()
    cnx.close()
    return data
    
def remove_mq_av_region():
    cnx = chiu_auth()
    cursor = cnx.cursor()
    sql = 'drop table {0}'.format(mq_av_region_name)
    cursor.execute(sql)
    cnx.commit()
    cursor.close()
    cnx.close()
    return 


#--------------------------------------------------

woerr_cloud_name = 'WOerr_Cloud'
woerr_cloud_format = mq_cloud_format

def save2sql_woerr_cloud(data):
    cnx = chiu_auth()
    cursor = cnx.cursor()
    # Creat database if did not exist.
    create_tables()
    # Save data into the table in the database.
    cursor.execute( 
        "insert into {0} ({1}) values ({2})".format(
            woerr_cloud_name,  
            ', '.join(woerr_cloud_format[2:,0]), 
            ', '.join(['%s'] * len(woerr_cloud_format[2:,0]))), 
        tuple(data[2:]))
    cnx.commit()
    cursor.close()
    cnx.close()

def load2py_woerr_cloud(col_list):
    # Connect to SQL
    cnx = chiu_auth()
    cursor = cnx.cursor()
    col_list_str = ', '.join(col_list)
    cursor.execute(
        "select {0} from {1}".format(
            col_list_str,
            woerr_cloud_name,
        )
    )
    data = cursor.fetchall()
    data = np.array(data, dtype = str)
    # Close the SQL
    cnx.commit()
    cursor.close()
    cnx.close()
    return data
    
def remove_woerr_cloud():
    cnx = chiu_auth()
    cursor = cnx.cursor()
    sql = 'drop table {0}'.format(woerr_cloud_name)
    cursor.execute(sql)
    cnx.commit()
    cursor.close()
    cnx.close()
    return 

