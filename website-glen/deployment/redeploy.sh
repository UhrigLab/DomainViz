# TODO: The IFS and following for loop should be able to display the information of the currently running jobs,
# and then you should be able to kill those jobs before closing the service files with `systemctl restart prodoplot`.
# The goal there is to be able to re-run the jobs using a direct python3 call to the domainviz.py file, thus not losing any
# data for users upon redeployment.
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