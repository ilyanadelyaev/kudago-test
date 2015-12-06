/usr/bin/env python ./manage.py test -v 2

pep8 ./

pylint  --errors-only ./core/ ./parsers/ ./rssrender/ ./www/
