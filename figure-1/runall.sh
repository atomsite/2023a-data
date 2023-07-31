ls -d */ | parallel -j10 'cd {} && i2mart 2> errors.txt && gzip -v *prn &&  mkdir prnfiles && mv *.prn.gz prnfiles/ && gzip mars_mantle && gzip mars_crust'
