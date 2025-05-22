create-venv:
	uv venv -p 3.11 venv

install:
	uv pip install -r pyproject.toml --all-extras --link-mode=copy  --no-cache-dir
	uv lock
	uv pip install -e . --link-mode=copy  --no-cache-dir

lint:
	pre-commit run --all-files

clean:
	rm -rf __pycache__ dist build ./**/*.egg-info

test:
	pytest

run-test:
	@job_id=$$(databricks jobs list --output JSON | jq -r '.[] | select(.settings.name == "Run Test-Notebook on Known Cluster course project") | .job_id'); \
	if [ -z "$$job_id" ]; then \
		echo "Creating new job..."; \
		job_id=$$(databricks jobs create --json '{ "name": "Run Test-Notebook on Known Cluster course project", "tasks": [{"task_key": "notebook_test-task","notebook_task": {"notebook_path": "/Workspace/Users/acikgozmm@gmail.com/.bundle/dev/marvelous-databricks-course-acikgozmehmet/files/tests/databricks_tests/run_tests_notebook"},"existing_cluster_id": "0201-062019-g0y4hlmn"}]}' | jq -r '.job_id'); \
		echo "New job created with ID: $$job_id"; \
	else \
		echo "Job already exists with ID: $$job_id"; \
	fi; \
	echo "Running test job..."; \
	databricks jobs run-now "$$job_id"


build:
	uv build

copy-whl-to-dbx:
	databricks fs cp ./dist/*.whl dbfs:/Volumes/mlops_dev/acikgozm/packages/hotel_reservations-latest-py3-none-any.whl --overwrite
	# databricks fs cp ./dist/*.whl ./notebooks/hotel_reservations-latest-py3-none-any.whl --overwrite
	rm -f ./notebooks/*.whl
	cp ./dist/*.whl ./notebooks/.

release: clean build copy-whl-to-dbx
