# Delete trail files
rm *_rst*
rm *_trail*

# Elaborate Model
spin -a main.pml -O

# Compile the code
gcc -DNOBOUNDCHECK -DVECTORSZ=8192 -DMEMLIM=60000 -DSPACE -DBITSTATE -DNOFAIR -DSAFETY -DSFH -DNCORE=16 -DVMAX=6000 -o model pan.c

# Execute the code
./model -w30
