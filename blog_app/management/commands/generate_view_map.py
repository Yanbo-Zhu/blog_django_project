import os
from django.core.management.base import BaseCommand
from django.urls import get_resolver, URLPattern, URLResolver
from graphviz import Digraph
from django.apps import apps

class Command(BaseCommand):
    help = 'Generate a relationship map of views for a specific Django application'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='The name of the Django application')

    def handle(self, *args, **options):
        app_name = options['app_name']
        app_config = apps.get_app_config(app_name)
        urlconf = get_resolver()
        dot = Digraph(comment=f'{app_name.capitalize()} Views Relationship Map')

        def process_urls(url_patterns, parent_name=None):
            for pattern in url_patterns:
                if isinstance(pattern, URLPattern):
                    callback = pattern.callback
                    if callback.__module__.startswith(app_config.name):
                        view_name = f"{callback.__module__}.{callback.__name__}"
                        dot.node(view_name)
                        if parent_name:
                            dot.edge(parent_name, view_name)
                elif isinstance(pattern, URLResolver):
                    namespace = pattern.namespace or pattern.pattern.regex.pattern
                    process_urls(pattern.url_patterns, namespace)

        process_urls(urlconf.url_patterns)

        output_path = os.path.join(os.getcwd(), f'{app_name}_view_map.dot')
        with open(output_path, 'w') as f:
            f.write(dot.source)

        self.stdout.write(self.style.SUCCESS(f'Successfully generated view map for {app_name} at {output_path}'))
