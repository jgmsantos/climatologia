#!/bin/bash

diretorio_dados="/mnt/c/Users/guilherme.martins/guilherme/base_dados/FOCOS/INPE/satelite_referencia/netcdf/mensal"
diretorio_tmp="/mnt/c/Users/guilherme.martins/guilherme/streamlit/climatologia_focos/tmp"
diretorio_output="/mnt/c/Users/guilherme.martins/guilherme/streamlit/climatologia_focos/output"

cdo -s --no_history -ymonmean -selyear,2003/2024 -mergetime ${diretorio_dados}/*.nc ${diretorio_tmp}/climatologia_espacial.nc