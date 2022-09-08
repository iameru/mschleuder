import json

from testmark import parse


def add_development_help(app):
    def has_no_empty_params(rule):
        defaults = rule.defaults if rule.defaults is not None else ()
        arguments = rule.arguments if rule.arguments is not None else ()
        return len(defaults) >= len(arguments)

    from flask import render_template, url_for

    @app.route("/dev/site-map")
    def site_map():
        links = []
        for rule in app.url_map.iter_rules():
            # Filter out rules we can't navigate to in a browser
            # and rules that require parameters
            if "GET" in rule.methods and has_no_empty_params(rule):
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                links.append((url, rule.endpoint))
        # links is now a list of url, endpoint tuples
        return render_template("site_map.html", links=links)

    return app


def dev_data(option: str = None) -> dict:
    dev_data = parse("dev.md")  # DEV DATA

    _entry = dev_data.get(option)
    if _entry:
        return json.loads(_entry)

    return None
