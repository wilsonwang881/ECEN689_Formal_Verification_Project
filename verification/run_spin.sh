# Delete trail files
rm *_rst*
rm *_trail*
rm model
rm *pan*

# Elaborate Model
spin -a main.pml -O 

# Compile the code
gcc -DNOBOUNDCHECK -DVECTORSZ=8192 -DMEMLIM=60000 -DSPACE -DBITSTATE -DNOFAIR -DSAFETY -DSFH -DNCORE=16 -DVMAX=9000 -o model pan.c

# Execute the code
./model -w30 -m5000000
