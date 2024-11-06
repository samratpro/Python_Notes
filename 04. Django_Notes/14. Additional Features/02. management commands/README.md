## Example Structure
```markdown
myproject/
├── myapp/
│   ├── management/
│   │   ├── __init__.py
│   │   ├── commands/
│   │       ├── __init__.py
│   │       ├── mycommand.py
├── myproject/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── manage.py
```

## Example mycommand.py
```py
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Prints the provided argument'

    def add_arguments(self, parser):
        parser.add_argument('arg1', type=str, help='Argument 1 description')

    def handle(self, *args, **kwargs):
        arg1 = kwargs['arg1']
        self.stdout.write(self.style.SUCCESS(f'Successfully handled argument: {arg1}'))

```
## Running the Command
```bash
python manage.py mycommand "Hello, World!"
```
## Output
```
Successfully handled argument: Hello, World!
```


