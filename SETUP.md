# Installation

### Clone app to your folder
```bash
git clone https://github.com/maxpryg/pet_project.git
```
### Go to app folder
```bash
cd pet_project
```
### Run Docker to build containers
```bash
docker-compose build
```
### Migrate database
```bash
docker-compose exec web python manage.py migrate
```
### Collect static files
```bash
docker-compose exec web python manage.py collectstatic
```
### Run tests to see if everything works
```bash
docker-compose exec web python manage.py test
```
### Start development server
```bash
docker-compose up
```
