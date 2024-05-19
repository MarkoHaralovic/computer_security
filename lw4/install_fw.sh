#! /bin/sh

if [ `id -u` -ne  0 ]; then
    echo "You must be root to run this script."
    exit 1
fi

himage -e FW > /dev/null
if test $? -ne 0; then
    echo "If FW is not a unique name, multiple experiments are running with the same node names."
    echo "Experiment Terminate / File Quit / sudo cleanupAll"
    echo ""
    echo "It the error is: 'cannot find node name server', you must start the experiment: Experiment->Execute"
    exit 1
fi

hcp FW.sh FW:/root
himage FW sh /root/FW.sh

