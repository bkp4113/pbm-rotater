python3=`which python3`
degree="0;90;180;270;360;-90;-180;-270;-360"

for f in `ls ./driver_pbm`;do
    for d in ${degree//;/ } ; do 
        $python3 ./src/pbm_rotater.py --path ./driver_pbm/${f} --export_path /tmp/new.pbm --degree ${d}
        if [[ -f /tmp/new.pbm ]]; then
            cat /tmp/new.pbm
        fi
        echo ""
    done
done