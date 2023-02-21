all: test
test:  

	@python3 mass_create_enterprises.py
	@python3 gui_check_enterprises.py
	@python3 mass_delete_enterprises.py
	@echo "Please Check /var/log/<YYY-MM-DD>_vsd_performance_checker.log"