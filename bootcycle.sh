#
# bootcycle.sh  Check if system has been rebooting repeatedly. 
#
# chkconfig: S 31 0
#
#

BOOTCYCLE_FILE=/sbin/bootcycle

# Execute the bootcycle program to detect frequent reboots
if [ -x $BOOTCYCLE_FILE ];
then
    $BOOTCYCLE_FILE
fi
     
