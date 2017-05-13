#!/bin/bash

# Change this to your DIR
DIR=~/neurio/

usage() 
{
  echo "recall: -d DATE -t TIME"
}

while getopts "d:t:" arg; do
  case $arg in 
    d)
      DATE=$OPTARG
      ;;
    t)
      TIME=$OPTARG
      ;;
    *)
      usage
      exit;
      ;;
    esac
done

if [ -z "${DATE}" ] || [ -z "${TIME}" ]; then
    usage
    exit;
fi


FILE=$DIR$DATE.csv

post() 
{
  RAW=$1
#  echo $RAW
  if [ -z "$RAW" ]; then
    echo "No data"
    exit;
  fi

  TIME=`echo $RAW|cut -d, -f1`
  GEN_W=`echo $RAW|cut -d, -f2`
  GEN_V=`echo $RAW|cut -d, -f3`
  CON_W=`echo $RAW|cut -d, -f4`
  TEMP=`echo $RAW|awk -F "," '{print $NF}' | sed -e 's/[[:space:]]*$//'`

  echo "POSTING AS $DATE $TIME "
#  curl -d "v4=$TEMP" -d "d=$DATE" -d "t=$TIME" -d "v2=$GEN_W" -d "v4=$CON_W" -d "v6=$GEN_V"  -H "X-Pvoutput-Apikey:6afa9ec13b0c9826654932ab8260088e1ad8826f" -H "X-Pvoutput-SystemId:50289" http://pvoutput.org/service/r2/addstatus.jsp
  echo ""
}


echo "Reading from $FILE"
RAW=`grep $TIME $FILE`
post $RAW

# API only allows 60 requests per hour, don't do this!
#array=$(sed -n '2,$p' "$FILE")
#for RAW in $array 
#do
#  post $RAW
#done




