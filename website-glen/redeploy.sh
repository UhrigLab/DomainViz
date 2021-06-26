#!/bin/sh
NUM_INSTANCES=$(ps -ef | grep "python" | egrep -v "grep|vi|more|pg" | wc -l)
if [ $NUM_INSTANCES -gt 0 ]; 
then 
echo "Running {$NUM_INSTANCES} jobs." 
COMMANDS=$(ps -C python -o args --no-headers)
echo $COMMANDS
else echo "No jobs are running."; 
fi

#IFS=', ' read -r -a array <<< "$string"
#for index in "${!array[@]}"
#do
#    echo "$index ${array[index]}"
#done
cd ..
git pull
cd website-glen/
npm install
npm run build
systemctl reload nginx
systemctl daemon-reload
systemctl restart prodoplot
echo "Redeployment finished."