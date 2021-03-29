#! /bin/bash

#set

echo ""
echo "Stoping fastdata... (may take a while)"
	docker stop fastdata
	docker stop $(echo $1)
	


echo ""
echo "Removing fastdata.."
	docker rm fastdata
	docker rm $(echo $1)
	


