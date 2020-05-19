#!/bin/bash
# Usage: YSO_number_routine.sh

# check arguments
if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "Usage: ${0##*/} [table name]"
    echo "Example: ${0##*/} irsa_catalog_search_results.tbl "
    exit 1
fi

# Initialization and Assignation
table_name=${1::-4}
echo '-------------------'
echo ${table_name} start

# extract data from table
extract_SEIP.py ${table_name}.tbl
# Exclude or Mask bad data
mask_ul.py ${table_name}_Q.txt ${table_name}_sed.txt
exclud_XUS_678.py ${table_name}_Q.txt ${table_name}_sed.txt
exclud_XUS_678.py ${table_name}_Q.txt ${table_name}_coord.txt
exclud_XUS_678.py ${table_name}_Q.txt ${table_name}_Av.txt
exclud_XUS_678.py ${table_name}_Q.txt ${table_name}_id.txt
exclud_XUS_678.py ${table_name}_Q.txt ${table_name}_Q.txt
exclud_XUS_678.py ${table_name}_Q.txt ${table_name}_2MASS_SPITZER_sed.txt
# Rename the file to 20190522_SCAO format
cp ${table_name}_sed_exXUS_678.txt source_sed_MaxLoss0.txt
cp ${table_name}_coord_exXUS_678.txt source_coord_MaxLoss0.txt
cp ${table_name}_Av_exXUS_678.txt source_Av_MaxLoss0.txt
cp ${table_name}_id_exXUS_678.txt source_id_MaxLoss0.txt
cp ${table_name}_Q_exXUS_678.txt source_Q_MaxLoss0.txt
# Make predictions (It need to be done manually.)
make_predicion_cnn.sh ../../c2d-SWIRE_region/appendix_Model_IV/part1_train/ MaxLoss5 MaxLoss0
echo ${table_name} done.
echo '-------------------'
