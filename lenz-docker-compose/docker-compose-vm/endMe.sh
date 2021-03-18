#! /bin/bash

echo ""
echo "Stoping fastdata... (may take a while)"
	docker stop fastdata
	docker stop mqtt

echo ""
echo "Removing fastdata.."
	docker rm fastdata
	docker rm mqtt
