dress: trousers shoes jacket
	@echo "All done. Let's go outside!"

jacket: pullover
	@echo "Putting on jacket."

pullover: shirt
	@echo "Putting on pullover."

shirt:
	@echo "Putting on shirt."

trousers: underpants
	@echo "Putting on trousers."

underpants:
	@echo "Putting on underpants."

shoes: socks
	@echo "Putting on shoes."

socks: pullover
	@echo "Putting on socks."


copy-to-bin:
	rm -rf ./bin
	mkdir ./bin

	cp -r ./config ./bin/config
	cp -r ./services ./bin/services
	cp -r ./utilities ./bin/utilities
	cp Dockerfile ./bin/Dockerfile
	cp requirements.txt ./bin/requirements.txt
	cp server.py ./bin/server.py

build-docker-prod-img:
	docker build .
