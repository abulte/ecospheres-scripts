"""
Duplicate legacy extras' schema data prior to migration
"""
import json

from minicli import cli, run

from es_scripts.api import DatagouvfrAPI


api = DatagouvfrAPI()


@cli
def migrate(slug: str = "", dry_run: bool = False):
    bouquets = api.get_bouquets()
    bouquets = [b for b in bouquets if b["slug"] == slug] if slug else bouquets
    for bouquet in bouquets:
        print(f"--> Handling {bouquet['slug']}...")
        payload = {
            "tags": bouquet["tags"],
            "extras": {
                **bouquet["extras"],
                "ecospheres": {
                    **bouquet["extras"].get("ecospheres", {}),
                    "datasets_properties": bouquet["extras"].get(
                        "ecospheres:datasets_properties", []
                    ),
                    "theme": bouquet["extras"]["ecospheres:informations"][0]["theme"],
                    "subtheme": bouquet["extras"]["ecospheres:informations"][0][
                        "subtheme"
                    ],
                },
            }
        }
        if not dry_run:
            api.put(f"/api/1/topics/{bouquet['id']}/", data=payload)
        else:
            print("Would have updated with:")
            print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    run()
