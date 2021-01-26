#!/bin/sh
NUM_INSTANCES = (ps -ef | grep "gunicorn" | egrep -v "grep|vi|more|pg" | wc -l)
 if [ $NUM_INSTANCES -gt 2 ]; 
 then 
 echo "running" 
 echo $NUM_INSTANCES
 ; 
 else echo "stopped"; 
 fi

# cd ..
# git pull
# cd website-glen/
# npm run build
# systemctl reload nginx
# systemctl daemon-reload
# systemctl restart prodoplot
# echo "Redeployment finished."