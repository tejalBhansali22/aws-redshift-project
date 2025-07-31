import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from awsglue import DynamicFrame
import re

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node airport_dim
airport_dim_node1752966467457 = glueContext.create_dynamic_frame.from_catalog(database="airline-datamart", table_name="dev_airlines_airports_dim",
redshift_tmp_dir = "s3://redshift-temp-data-tejal/temp-data/airline-dim/",transformation_ctx="airport_dim_node1752966467457")

# Script generated for node daily_flights_data
daily_flights_data_node1752966159371 = glueContext.create_dynamic_frame.from_catalog(database="airline-datamart", table_name="daily_flights", transformation_ctx="daily_flights_data_node1752966159371")

# Script generated for node Filter
Filter_node1752966409659 = Filter.apply(frame=daily_flights_data_node1752966159371, f=lambda row: (row["depdelay"] >= 60), transformation_ctx="Filter_node1752966409659")

# Script generated for node join-for-arr-airport
Filter_node1752966409659DF = Filter_node1752966409659.toDF()
airport_dim_node1752966467457DF = airport_dim_node1752966467457.toDF()
joinforarrairport_node1752966591579 = DynamicFrame.fromDF(Filter_node1752966409659DF.join(airport_dim_node1752966467457DF, (Filter_node1752966409659DF['originairportid'] == airport_dim_node1752966467457DF['airport_id']), "left"), glueContext, "joinforarrairport_node1752966591579")

# Script generated for node modify-departure-airport-columns
modifydepartureairportcolumns_node1752966703690 = ApplyMapping.apply(frame=joinforarrairport_node1752966591579, mappings=[("depdelay", "long", "dep_delay", "bigint"), ("arrdelay", "long", "arr_delay", "bigint"), ("destairportid", "long", "destairportid", "long"), ("carrier", "string", "carrier", "string"), ("city", "string", "dep_city", "string"), ("name", "string", "dep_airport", "string"), ("state", "string", "dep_state", "string")], transformation_ctx="modifydepartureairportcolumns_node1752966703690")

# Script generated for node join_for_dep_airport
modifydepartureairportcolumns_node1752966703690DF = modifydepartureairportcolumns_node1752966703690.toDF()
airport_dim_node1752966467457DF = airport_dim_node1752966467457.toDF()
join_for_dep_airport_node1752967283633 = DynamicFrame.fromDF(modifydepartureairportcolumns_node1752966703690DF.join(airport_dim_node1752966467457DF, (modifydepartureairportcolumns_node1752966703690DF['destairportid'] == airport_dim_node1752966467457DF['airport_id']), "left"), glueContext, "join_for_dep_airport_node1752967283633")

# Script generated for node Change Schema
ChangeSchema_node1752967346571 = ApplyMapping.apply(frame=join_for_dep_airport_node1752967283633, mappings=[("carrier", "string", "carrier", "string"), ("dep_state", "string", "dep_state", "string"), ("state", "string", "arr_state", "string"), ("arr_delay", "bigint", "arr_delay", "long"), ("city", "string", "arr_city", "string"), ("name", "string", "arr_airport", "string"), ("dep_city", "string", "dep_city", "string"), ("dep_delay", "bigint", "dep_delay", "long"), ("dep_airport", "string", "dep_airport", "string")], transformation_ctx="ChangeSchema_node1752967346571")

# Script generated for node redshift-target-table
redshifttargettable_node1752967422109 = glueContext.write_dynamic_frame.from_catalog(frame=ChangeSchema_node1752967346571, database="airline-datamart", table_name="dev_airlines_daily_flights_fact", redshift_tmp_dir = "s3://aws-glue-assets-883467885365-us-east-2/temporary/", transformation_ctx="redshifttargettable_node1752967422109")

job.commit()