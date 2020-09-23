from main import find_plugin
from main import plugin_cache, get_plugin_cache_length

plugins = """
- kubernetes:1.15.5
- workflow-job:2.32
- workflow-aggregator:2.6
- credentials-binding:1.18
- git:3.10.0
- saml:1.1.2
- blueocean:1.16.0
- artifactory:3.2.2
- bitbucket:1.1.8
- basic-branch-build-strategies:1.3.2
- cloudbees-credentials:3.3
- cloudbees-bitbucket-branch-source:2.4.4
- slack:2.23
- prometheus:2.0.0
- sonar:2.9"""


def test_scanner():

    data = wash_plugin_list()
    print(f"Found: {data}")

    found_plugins = []
    for plugin in data:
        current_plugin = find_plugin(plugin)
        found_plugins.append(current_plugin)

    print(f"{found_plugins}")
    assert len(found_plugins) > 0
    assert len(data) > 0
    assert len(found_plugins) == len(data)


def test_plugin_cache():



    data = wash_plugin_list()

    found_plugins = []
    for plugin in data:
        current_plugin = find_plugin(plugin)
        found_plugins.append(current_plugin)

    print(f"{found_plugins}")
    
    assert get_plugin_cache_length() > 0

    # Test cache size is same as last call
    last_cache_size = get_plugin_cache_length()
    found_plugins = []
    for plugin in data:
        current_plugin = find_plugin(plugin)
        found_plugins.append(current_plugin)


    assert get_plugin_cache_length() == last_cache_size





def wash_plugin_list():
    washed_list = []
    plugin_list = plugins.split("\n")
    print(plugin_list)
    for plugin in plugin_list:
        if len(plugin) > 1:
            washed_plugin = plugin.strip("-").strip()
            washed_plugin = washed_plugin[0:washed_plugin.index(":")]
            washed_list.append(washed_plugin)
    return washed_list
