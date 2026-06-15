
# Add any additional apps here
ADDON_APPS = [
    "webapps.home",
    "webapps.search",
    "webapps.blog",

    "fontawesomefree",
    "wagtailfontawesomesvg",
    "wagtailmenus",
]

ADDON_TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                'wagtailmenus.context_processors.wagtailmenus',
            ]
        }
     }
]

# Merge complex template config
def merge_template_configs(base, addon):
    """Deep merge addon template configs into base templates list."""
    result = [dict(t) for t in base]

    for addon_tmpl in addon:
        # Find matching backend or use first entry as default
        backend = addon_tmpl.get("BACKEND")
        target = next(
            (t for t in result if t.get("BACKEND") == backend),
            result[0]  # fallback to first template config
        )

        for key, value in addon_tmpl.items():
            if key not in target:
                target[key] = value
            elif isinstance(value, dict) and isinstance(target[key], dict):
                # Recursively merge dicts (e.g. OPTIONS)
                for subkey, subvalue in value.items():
                    if subkey not in target[key]:
                        target[key][subkey] = subvalue
                    elif isinstance(subvalue, list) and isinstance(target[key][subkey], list):
                        # Merge lists, avoiding duplicates (e.g. context_processors)
                        target[key][subkey] = target[key][subkey] + [
                            item for item in subvalue
                            if item not in target[key][subkey]
                        ]

    return result

