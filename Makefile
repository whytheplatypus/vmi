
develop:
	docker-compose -f .development/docker-compose.yml up -d 

develop-logs:
	docker-compose -f .development/docker-compose.yml logs -f

clean:
	docker-compose -f .development/docker-compose.yml down
	
